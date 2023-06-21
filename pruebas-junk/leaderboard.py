from communication.client.client import MountainClient
import random
from partida import Partida
import time
from tabulate import tabulate

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
    count = 1
    while not cliente.is_over():
        info = cliente.get_data()
        if len(info) > 0:
            match = Partida(info)
            teams = match.get_teams()
            players = []
            for team in teams:
                for player in team.get_players():
                    players.append(player)
            players.sort()
            player_names = [[count, player.name] for count, player in enumerate(players, start=1)]
            print(tabulate(player_names, headers=['#', 'Nombre'], tablefmt='fancy_grid'))
            print("\n")
            count += 1
            time.sleep(1)

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

        time.sleep(3)


mandar_data()
data = cliente.get_data()
print(data)
