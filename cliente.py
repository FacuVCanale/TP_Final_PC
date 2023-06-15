from communication.client.client import MountainClient
from communication.util.logger import logger
import random
import math

cliente = MountainClient("34.16.147.147", 8080)

directions = {}
directions1 = {}
directions['facu'] = {'speed': 50, 'direction': 75* math.pi /180}
directions['lucas'] = {'speed': 50, 'direction': 50 * math.pi /180}
directions['joaco'] = {'speed': 50, 'direction': 85 * math.pi /180}
directions['test'] = {'speed': 30, 'direction': 20 * math.pi /180}
directions1['jugador1'] = {'speed': 50, 'direction': -math.pi /2}  # Agrega los jugadores del equipo CopNieve al diccionario directions
directions1['jugador2'] = {'speed': 50, 'direction': math.pi /2}
directions1['jugador3'] = {'speed': 50, 'direction': math.pi }
directions1['jugador4'] = {'speed': 50, 'direction': 0}

cliente.add_team("LIFFT", ['facu', 'lucas', 'joaco', 'test'])
cliente.add_team("CopNieve", ['jugador1', 'jugador2', 'jugador3', 'jugador4'])

cliente.finish_registration()

coord_set = set()


def mandar_data():
    global directions,directions1
    while not cliente.is_over():
        info = cliente.get_data()
        print(info)

        cliente.next_iteration("LIFFT", directions)
        cliente.next_iteration("CopNieve", directions1)

        with open('coordenadas.txt', 'a') as file:
            for team in info.values():
                for climber in team.values():
                    x = round(climber['x'], 2)
                    y = round(climber['y'], 2)
                    z = round(climber['z'], 5)
                    coord = (x, y, z)

                    line = f"{x} {y} {z}\n"
                    file.write(line)
                    coord_set.add(coord)

    directions['facu'] = {'speed': 50, 'direction': - math.pi /2}
    directions['lucas'] = {'speed': 50, 'direction': math.pi/2}
    directions['joaco'] = {'speed': 50, 'direction': 0}
    directions['test'] = {'speed': 30, 'direction': 20 * math.pi /180}
    directions1['jugador1'] = {'speed': 50, 'direction': 0}  # Agrega los jugadores del equipo CopNieve al diccionario directions
    directions1['jugador2'] = {'speed': 50, 'direction': math.pi /2}
    directions1['jugador3'] = {'speed': 50, 'direction': math.pi }
    directions1['jugador4'] = {'speed': 50, 'direction': 180}


mandar_data()
data = cliente.get_data()
print(data)
