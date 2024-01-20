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
import random
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
            print(current_packet)
            time.sleep(config["packet_period"])


def read_config_file(path):
    '''
    Reads the config file. At this moment, it is mocked.
    '''
    # TODO
    return {
        "packet_period": 1,
        "device_id": str(random.getrandbits(128)),
        "deviations": {
            "temperature": 3,
            "humidity": 5,
            "light": 25,
            "watering": 5
        }
    }


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    config = read_config_file("")

    simulate_packets(config)
