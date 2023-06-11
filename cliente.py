#El nombre del equipo es CopNieve
# codigo
from communication.client.client import MountainClient
from communication.util.logger import logger
from climbers import Climbers
import time
import random

cliente = MountainClient("34.16.147.147",8080)


directions ={}
directions['facu'] = {'speed': 30, 'direction': 45}
directions['lucas'] = {'speed': 10, 'direction': 50}

cliente.add_team("LIFFT",['facu','lucas'])
    
cliente.finish_registration()

coord_set = set()
def mandar_data():
    while not cliente.is_over():
        info = cliente.get_data() #{'LIFFT': {'facu': {'x': 14000, 'y': 14000, 'z': -14109979074.0, 'inclinacion_x': -503966.0, 'inclinacion_y': -503962.0, 'cima': False}
        print(info)


        cliente.next_iteration("LIFFT", directions) #VER POR QUE FACU FALLECE Y NO SE PRINTEA EN GET.DATA(), ES DECIR, NO APARECE EN EL SV. 
        with open('coordenadas.txt', 'a') as file:
            for team in info.values():
                for climber in team.values():
                    x = climber['x']
                    y = climber['y']
                    z = climber['z']
                    coord = (x, y, z)
                    if coord not in coord_set:
                        line = f"{x} {y} {z}\n"
                        file.write(line)
                        coord_set.add(coord)

        directions['facu']['direction'] += random.choice([i for i in range(300)])
        directions['lucas']['direction'] += random.choice([i for i in range(200)])

mandar_data()
data = cliente.get_data()
print(data)


