from communication.client.client import MountainClient
import random

cliente = MountainClient("localhost", 8080)

directions = {}
directions['facu'] = {'speed': 50, 'direction': 45}
directions['lucas'] = {'speed': 50, 'direction': 50}
directions["fran"] = {"speed": 50, 'direction': 50}
directions["ivan"] = {"speed": 50, 'direction': 50}

directions1 = {}
directions1['fac'] = {'speed': 50, 'direction': 45}
directions1['luca'] = {'speed': 50, 'direction': 50}
directions1["fra"] = {"speed": 50, 'direction': 50}
directions1["iva"] = {"speed": 50, 'direction': 50}

cliente.add_team("LIFFT", ['facu', 'lucas', "fran", "ivan"])
cliente.add_team("LIFF", ['fac', 'luca', "fra", "iva"])

cliente.finish_registration()


def mandar_data():

    while not cliente.is_over():
        info = cliente.get_data()
        cliente.next_iteration("LIFFT", directions)
        cliente.next_iteration("LIFF", directions1)
        directions['facu']['direction'] += random.choice([i for i in range(300)])
        directions['lucas']['direction'] += random.choice([i for i in range(200)])
        directions['fran']['direction'] += random.choice([i for i in range(200)])
        directions['ivan']['direction'] += random.choice([i for i in range(200)])
        directions1['fac']['direction'] += random.choice([i for i in range(300)])
        directions1['luca']['direction'] += random.choice([i for i in range(200)])
        directions1['fra']['direction'] += random.choice([i for i in range(200)])
        directions1['iva']['direction'] += random.choice([i for i in range(200)])


mandar_data()
data = cliente.get_data()
print(data)
