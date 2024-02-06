'''
Leer archivo de configuracion

Cada N segundos:
    - Generar un paquete de datos
    - Decidir si el paquete es apto para ser enviado
        - Si no es apto, descartar y esperar al siguiente.
    - Agregar timestamp y device_id al paquete.
    - Enviar paquete a la queue.
'''

import time
import logging
import json
import os
from common.middleware import Middleware

from data_packet import generate_data, create_packet, data_has_changed


def simulate_packets(config):
    middleware = Middleware()
    queue_name = os.environ.get("QUEUE_NAME")
    middleware.create_queue(queue_name)
    last_sent_packet = None
    current_packet = None
    while True:
        try:
            temperature, humidity, light, watering = generate_data()
            current_packet = create_packet(temperature, humidity, light,
                                           watering)

            if not current_packet or not data_has_changed(
                current_packet,
                last_sent_packet,
                config["deviations"]
            ):
                continue
            middleware.send_message(queue_name, json.dumps(current_packet))
            logging.info(f"Packet sent: {current_packet}")
            last_sent_packet = current_packet

        except Exception as err:
            logging.warning(f"{err}")
        finally:
            print(current_packet)
            time.sleep(config["packet_period"])


def read_config_file(path):
    try:
        with open(path, 'r') as file:
            config_data = json.load(file)
        return config_data
    except FileNotFoundError:
        logging.error(f"Config file not found at: {path}")
        raise
    except json.JSONDecodeError as json_err:
        logging.error(f"Error decoding config file: {json_err}")
        raise


def main():
    logging_level = os.environ.get("LOGGING_LEVEL")
    initialize_log(logging_level)
    config_path = "config.json"
    config = read_config_file(config_path)
    simulate_packets(config)


def initialize_log(logging_level):
    """
    Python custom logging initialization

    Current timestamp is added to be able to identify in docker
    compose logs the date when the log has arrived
    """
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging_level,
        datefmt='%Y-%m-%d %H:%M:%S',
    )
    logging.getLogger("pika").setLevel(logging.WARNING)


if __name__ == '__main__':
    main()
