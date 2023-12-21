'''
Leer archivo de configuracion

Cada N minutos:
    - Generar un paquete de datos
    - Decidir si el paquete es apto para ser enviado
        - Si no es apto, descartar y esperar al siguiente.
    - Agregar timestamp y device_id al paquete.
    - Enviar paquete a la queue.
'''

from threading import Thread, Lock
import time

def counter():
    global resto
    contador = 0
    while True:
        contador += 1
        with resto_lock:  
            print(f"COUNTER: {contador} - {resto} = {contador - resto}")
        time.sleep(1)


def user_input():
    global resto
    while True:
        user_input = input()
        if user_input.lower() == 'exit':
            break
        with resto_lock:
            resto = int(user_input)
        print(f"USER-INPUT: {resto}")

if __name__ == '__main__':
    resto = 0
    resto_lock = Lock()  

    hilo_incremento = Thread(target=counter)
    hilo_decremento = Thread(target=user_input)

    hilo_incremento.start()
    hilo_decremento.start()

    hilo_decremento.join()
    hilo_incremento.join()
    