from communication.client.client import MountainClient
from classes.partida import Partida
from tabulate import tabulate
import time
import os
cliente1 = MountainClient("localhost", 8080)


def mandar_data():
    count = 1
    while not cliente1.is_over():
        info = cliente1.get_data()
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
            os.system("clear")


mandar_data()
data = cliente1.get_data()
print(data)
