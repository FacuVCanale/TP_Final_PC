#El nombre del equipo es CopNieve
# codigo

from communication.client.client import MountainClient
from communication.util.logger import logger
# from climbers import Climbers
import time
import random
import numpy as np
def move_to_point_direction(pos_o ,pos_f,vel = 8):
    xo = pos_o[0]
    yo = pos_o[1]

    xf = pos_f[0]
    yf = pos_f[1]

    v = (xf - xo, yf - yo)
    v_direc = np.arctan(v[0]/v[1])

    if np.linalg.norm(v) < 50:
        vel = np.linalg.norm(v)
 
    return np.degrees(v_direc),vel

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
        time.sleep(2)
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
        data = cliente.get_data()
        print(data)
        print("XY", (data["LIFFT"]['facu']['x'],data["LIFFT"]['facu']['y']))
        print("MOVIMIENTO",move_to_point_direction((data["LIFFT"]['facu']['x'],data["LIFFT"]['facu']['y']), (100,100)))
        directions['facu']['direction'] = move_to_point_direction((data["LIFFT"]['facu']['x'],data["LIFFT"]['facu']['y']), (100,100))[0]
        directions['facu']['direction'] = move_to_point_direction((data["LIFFT"]['lucas']['x'],data["LIFFT"]['lucas']['y']), (100,100))[0]

mandar_data()
data = cliente.get_data()
# print(data)

# def move_to_point_direction(pos_o ,pos_f,vel = 50):
#     xo = pos_o[0]
#     yo = pos_o[1]

#     xf = pos_f[0]
#     yf = pos_f[1]

#     v = (xf - xo, yf - yo)
#     v_direc = np.arctan(v[0]/v[1])

#     if np.linalg.norm(v) < 50:
#         vel = np.linalg.norm(v)
 
#     return np.degrees(v_direc),vel