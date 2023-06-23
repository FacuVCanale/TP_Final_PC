from communication.client.client import MountainClient
import time
import random
import numpy as np

cliente = MountainClient("localhost", 8080)

directions = {}
directions2 = {}
escaladores = ['facu', 'lucas', 'juan', 'emilio', 'diana', 'raul', 'marta', 'roberto', 'valentina', 'sergio', 'laura', 'oscar']
escaladores2 = ['ramon', 'ivan', 'cami']

# Configurar las instrucciones para cada escalador
angle_forward = np.deg2rad(30)  # Ángulo de avance hacia adelante
angle_backward = np.deg2rad(150)  # Ángulo de avance hacia atrás

for i, escalador in enumerate(escaladores):
    speed = random.randint(10, 50)

    if i < len(escaladores) // 2:
        # Primer mitad de los escaladores va hacia adelante
        direction = i * angle_forward
    else:
        # Segunda mitad de los escaladores va hacia atrás
        direction = (i - len(escaladores) // 2) * angle_backward

    directions[escalador] = {'speed': speed, 'direction': direction}

# Configurar las instrucciones para cada escalador de Lifft
for i, escalador in enumerate(escaladores2):
    speed = random.randint(10, 50)
    direction = np.deg2rad(0)  # Ángulo de avance en línea recta (0 grados)

    directions2[escalador] = {'speed': speed, 'direction': direction}



cliente.add_team("CopNieve", escaladores)
cliente.add_team("Lifft", escaladores2)  # Agregar equipo "Lifft" con instrucción de ir en línea recta

cliente.finish_registration()

coord_set = set()

def mandar_data():
    while not cliente.is_over():
        info = cliente.get_data()
        time.sleep(2)
        print(info)

        cliente.next_iteration("CopNieve", directions)
        cliente.next_iteration("Lifft", directions2)

mandar_data()

data = cliente.get_data()
print(data)
