#El nombre del equipo es CopNieve
# codigo
from communication.client.client import MountainClient
from communication.util.logger import logger
# from climbers import Climbers
import time
import random

cliente = MountainClient("localhost",8080)


directions ={}
directions['facu'] = {'speed': 30, 'direction': 45}
directions['lucas'] = {'speed': 10, 'direction': 50}

cliente.add_team("LIFFT",['facu','lucas'])
    
cliente.finish_registration()

coord_set = set()
def mandar_data():
    while not cliente.is_over():
        info = cliente.get_data()  # {'LIFFT': {'facu': {'x': 14000, 'y': 14000, 'z': -14109979074.0, 'inclinacion_x': -503966.0, 'inclinacion_y': -503962.0, 'cima': False}}
        time.sleep(4)
        print(info) 

        cliente.next_iteration("LIFFT", directions)  # VER POR QUE FACU FALLECE Y NO SE PRINTEA EN GET.DATA(), ES DECIR, NO APARECE EN EL SV.
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

        directions['facu']['direction'] += random.choice([i for i in range(300)])
        directions['lucas']['direction'] += random.choice([i for i in range(200)])



mandar_data()
data = cliente.get_data()
print(data)