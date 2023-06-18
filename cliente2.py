#El nombre del equipo es CopNieve
# codigo
from communication.client.client import MountainClient
import random
import csv
cliente = MountainClient("34.16.147.147",8080)


directions ={}
directions['facu'] = {'speed': 50, 'direction': 45}
directions['lucas'] = {'speed': 50, 'direction': 50}
directions["fran"] = {"speed": 50, 'direction': 50}
directions["ivan"] = {"speed": 50, 'direction': 50}

cliente.add_team("LIFFT",['facu','lucas',"fran","ivan"])
    
cliente.finish_registration()

coord_set = set()
with open('coordenadas.csv', 'w') as archivo_csv:
        writer = csv.writer(archivo_csv)
        
        # Escribir encabezados
        writer.writerow(['Equipo', 'Escalador', 'X', 'Y', 'Z', 'Inclinacion X', 'Inclinacion Y', 'Cima'])

def mandar_data():
    while not cliente.is_over():
        info = cliente.get_data()  # {'LIFFT': {'facu': {'x': 14000, 'y': 14000, 'z': -14109979074.0, 'inclinacion_x': -503966.0, 'inclinacion_y': -503962.0, 'cima': False}}
        print(info)
        cliente.next_iteration("LIFFT", directions)
        with open('coordenadas.csv', 'a') as archivo_csv:
            writer = csv.writer(archivo_csv)
            for equipo, escaladores in info.items():
                for escalador, info in escaladores.items():
                    x = info['x']
                    y = info['y']
                    z = info['z']
                    inclinacion_x = info['inclinacion_x']
                    inclinacion_y = info['inclinacion_y']
                    if info['cima'] is not True:
                         cima = ""
                    else:
                         cima = True
                    writer.writerow([equipo, escalador, x, y, round(z,1), round(inclinacion_x,3), round(inclinacion_y,3), cima])
        info = cliente.get_data()
        with open('pos_act.csv', 'w') as archivo_csv:
            writer = csv.writer(archivo_csv)
            for equipo, escaladores in info.items():
                for escalador, info in escaladores.items():
                    x = info['x']
                    y = info['y']
                    if info['cima'] is not True:
                         cima = ""
                    else:
                         cima = True
                    writer.writerow([equipo, escalador, round(x,2), round(y,2), cima])
        directions['facu']['direction'] += random.choice([i for i in range(300)])
        directions['lucas']['direction'] += random.choice([i for i in range(200)])
        directions['fran']['direction'] += random.choice([i for i in range(200)])
        directions['ivan']['direction'] += random.choice([i for i in range(200)])


mandar_data()
data = cliente.get_data()
print(data)


