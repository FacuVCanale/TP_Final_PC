from communication.client import client
import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    '--ip', type=str, help='Dirección IP y puerto del servidor en formato IP:puerto')
args = parser.parse_args()

ip, port = args.ip.split(':')
#"LOCALHOST:8080"
