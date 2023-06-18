from communication.client.client import MountainClient
import time
import random
import numpy as np

cliente = MountainClient("localhost", 8080)

directions = {}
escaladores = ['facu', 'lucas', 'juan', 'emilio', 'diana', 'raul', 'marta', 'roberto', 'valentina', 'sergio', 'laura', 'oscar']

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

cliente.add_team("CopNieve", escaladores)
cliente.finish_registration()

coord_set = set()

def mandar_data():
    while not cliente.is_over():
        info = cliente.get_data()
        time.sleep(2)
        print(info)

        cliente.next_iteration("CopNieve", directions)
        with open('coordenadas.tsv', 'a') as file:
            for team, climbers in info.items():
                for climber, data in climbers.items():
                    x = data['x']
                    y = data['y']
                    z = data['z']
                    coord = (x, y, z)
                    if coord not in coord_set:
                        line = f"EQUIPO: {team.ljust(10)}\tESCALADOR: {climber.ljust(10)}\tPOSICION: {x}, {y}, {z}\n"
                        file.write(line)
                        coord_set.add(coord)

mandar_data()

data = cliente.get_data()
print(data)
