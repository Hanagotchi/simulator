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
import json
import logging

from data_packet import generate_data, create_packet, data_has_changed


def simulate_packets(config):
    last_sent_packet = None
    while True:
        try:
            temperature, humidity, light, watering = generate_data()
            current_packet = create_packet(temperature, humidity, light, watering)

            if not current_packet or not data_has_changed(current_packet, last_sent_packet, config["deviations"]):
                continue

            # TODO: Send packet to the RabbitMQ queue
            logging.info(f"Packet sent: {current_packet}")
            last_sent_packet = current_packet

        except Exception as err:
            logging.warning(err)
        finally:
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


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    config_path = "config.json"
    config = read_config_file(config_path)

    simulate_packets(config)
