#El nombre del equipo es CopNieve
# codigo
from communication.client.client import MountainClient
import random
from teams import Team
cliente = MountainClient("localhost",8080)


directions ={}
directions['facu'] = {'speed': 50, 'direction': 45}
directions['lucas'] = {'speed': 50, 'direction': 50}
directions["fran"] = {"speed": 50, 'direction': 50}
directions["ivan"] = {"speed": 50, 'direction': 50}

cliente.add_team("LIFFT",['facu','lucas',"fran","ivan"])
    
cliente.finish_registration()

def mandar_data():
    while not cliente.is_over():
        info = cliente.get_data()
        if len(info) > 0:  # {'LIFFT': {'facu': {'x': 14000, 'y': 14000, 'z': -14109979074.0, 'inclinacion_x': -503966.0, 'inclinacion_y': -503962.0, 'cima': False}}
            tema = Team(info) #FALTA ESCALAR A MAS DE UN TEAM(OSEA FALTARIA LA CLASE "EQUIPOS" | "PARTIDA")
            for i in tema.get_players():
                print(i)
        cliente.next_iteration("LIFFT", directions)
        directions['facu']['direction'] += random.choice([i for i in range(300)])
        directions['lucas']['direction'] += random.choice([i for i in range(200)])
        directions['fran']['direction'] += random.choice([i for i in range(200)])
        directions['ivan']['direction'] += random.choice([i for i in range(200)])

mandar_data()
data = cliente.get_data()
print(data)


