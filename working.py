from circulo_creator import Circulo
from mapa import Mapa_circular
import csv
import time
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
    time.sleep(1)
    fil = len(circulo)
    with open("ascii2.txt", "w", encoding='utf-8') as f:
        for _ in range(fil):
            circulo[_].append("\n")
            linea = ' '.join(circulo[_])
            f.writelines(linea)

    