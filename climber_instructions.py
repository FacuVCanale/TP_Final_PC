import random
import time
from equipos import team1,team2,cliente # peres, facu
import subprocess
import os

file_path = os.path.join('/Users/juanfra/Documents/Facultad/Pensamiento computacional/TP_Final_PC', 'interfaz.py')
subprocess.Popen(['python3', file_path])


directions_peres,juanma = team1()
directions_lift,facu = team2()
cliente.finish_registration()

coord_set = set()
while not cliente.is_over():
    
    info = cliente.get_data() #{'LIFFT': {'facu': {'x': 14000, 'y': 14000, 'z': -14109979074.0, 'inclinacion_x': -503966.0, 'inclinacion_y': -503962.0, 'cima': False}
    print(info)
    time.sleep(1)
    cliente.next_iteration("EQUIPO_PERES", directions_peres) 
    #time.sleep(5)
    cliente.next_iteration("LIFFT", directions_lift) #VER POR QUE FACU FALLECE Y NO SE PRINTEA EN GET.DATA(), ES DECIR, NO APARECE EN EL SV. 
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

    directions_peres[juanma]['direction'] += random.choice([i for i in range(120)])
        