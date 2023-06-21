from classes.circulo_creator import Circulo
from classes.mapa import Mapa_circular
import csv
import time
import os
while True:
    circulo = Circulo(46)
    mapa = Mapa_circular(circulo)
    # Leer los datos del archivo CSV y agregar los personajes al mapa
    with open('pos_act.csv', 'r') as archivo_csv:
        reader = csv.reader(archivo_csv)
        num_jugador = 32
        for row in reader:
            equipo = row[0]
            jugador = row[1]
            x = float(row[2])
            y = float(row[3])
            flag = row[4]
            mapa.agregar_pj((x, y), num_jugador,flag)
            num_jugador += 1
    print(mapa)
    time.sleep(1)
    os.system("clear")
    

    