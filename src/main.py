
'''
Leer archivo de configuracion

Cada N minutos:
    - Generar un paquete de datos
    - Decidir si el paquete es apto para ser enviado
        - Si no es apto, descartar y esperar al siguiente.
    - Agregar timestamp y device_id al paquete.
    - Enviar paquete a la queue.
'''