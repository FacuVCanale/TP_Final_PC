import threading
import time

from communication.client.client import MountainClient

class Dashboard:
    def __init__(self, client: MountainClient):
        self.client = client
        self.data = client.get_data()
        self.time_step = 500  # ms
        self.map_size = 100  # Tamaño del mapa (100x100)
        self.map = [[' ' for _ in range(self.map_size)] for _ in range(self.map_size)]  # Inicializa el mapa vacío

    def start(self):
        t = threading.Thread(target=self.update_data)
        t.start()
        self.print_map()  # Imprime el mapa inicial
        while not self.client.is_over():
            time.sleep(self.time_step / 1000)  # Espera el tiempo especificado antes de la próxima actualización
            self.print_map()  # Imprime el mapa actualizado

    def update_data(self):
        while not self.client.is_over():
            self.data = self.client.get_data()  # Actualiza los datos del cliente
            self.update_map()  # Actualiza el mapa con los datos de los jugadores

    def update_map(self):
        # Limpia el mapa
        self.map = [[' ' for _ in range(self.map_size)] for _ in range(self.map_size)]
        
        # Actualiza el mapa con la posición de los jugadores
        for player in self.data['players']:
            x, y = player['position']
            self.map[y][x] = 'P'  # 'P' representa a un jugador en el mapa

    def print_map(self):
        # Imprime el mapa en la terminal
        for row in self.map:
            print(' '.join(row))
        print()

    def stop(self):
        self.client.close()

if __name__ == "__main__":
    client = MountainClient('34.16.147.147', 8080)
    d = Dashboard(client)
    d.start()
