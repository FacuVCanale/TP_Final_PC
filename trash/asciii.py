from classes.circulo_creator import Circulo
from classes.mapa import Mapa_circular
import time
import os
from communication.client.client import MountainClient
cliente = MountainClient("localhost",8080)
def ascii():
    while not cliente.is_over():
        circulo = Circulo(46)
        mapa = Mapa_circular(circulo)
        info = cliente.get_data()
        num_jugador = 32
        for equipo, escaladores in info.items():
            for escalador, infos in escaladores.items():
                x = infos['x']
                y = infos['y']
                if infos['cima'] is not True:
                     cima = ""
                else:
                     cima = True
                mapa.agregar_pj((x, y), num_jugador,cima)
                num_jugador += 1
        print(mapa)
        time.sleep(1)
        os.system("clear")

if __name__ == "__main__":
    ascii()
    

    