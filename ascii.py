from classes.circulo_creator import Circulo
from classes.mapa import Mapa_circular
import time
import os
from communication.client.client import MountainClient

def ascii(letter_asig, client):
    #while not cliente.is_over():
    circulo = Circulo(46)
    mapa = Mapa_circular(circulo)
    info = client.get_data()
    for equipo, escaladores in info.items():
        for escalador, infos in escaladores.items():
            x = infos['x']
            y = infos['y']
            if infos['cima'] is not True:
                cima = ""
            else:
                cima = True
            mapa.agregar_pj((x, y), letter_asig[equipo],cima)
    return mapa

if __name__ == "__main__":
    ascii()
    

    
