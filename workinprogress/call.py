import argparse
from communication.client.client import MountainClient
from communication.util.logger import logger
parser = argparse.ArgumentParser()
parser.add_argument(
    '--ip',
    type=str,
    help='Dirección IP y puerto del servidor en formato IP:puerto')
args = parser.parse_args()
ip, port = args.ip.split(':')

class Climbers:
    def __init__(self, name, strat):
        self.name = name
        self.strat = strat


player1 = Climbers("facu", "bogo")
player2 = Climbers("fran", "bogo")
player3 = Climbers("ivan", "pro")
player4 = Climbers("lucas", "nashe")

cliente = MountainClient(ip,int(port))
climbers = [player1.name, player2.name, player3.name, player4.name]
cliente.add_team("LIFFT", climbers)

direction = {}
cliente.next_iteration("LIFFT", direction)
print(cliente.finish_registration())
data = cliente.get_data()
print(data)
logger.warning(f"Datos: {data}")
