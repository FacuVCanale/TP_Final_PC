import csv
import time

ESCALA = 1000 # 1:1000
def circle_gen():
    # Crear una lista vacía para almacenar el círculo
    circulo = []

    # Crear la matriz del círculo
    for fila in range(46):
        # Crear una lista vacía para cada fila
        nueva_fila = []
        for columna in range(46):
            # Verificar si el punto actual está dentro del círculo
            if (columna - 23)**2 + (fila - 23)**2 <= 23**2:
                nueva_fila.append('X')
            else:
                nueva_fila.append(' ')
        # Agregar la fila a la lista del círculo
        circulo.append(nueva_fila)
    return circulo
def agregar_pj(a, num_jugador, circulo):
    for i in circulo:
        for j in i:
            if j == num_jugador:
                circulo[i][j] = "X"

    x = int(a[0] / ESCALA)
    y = int(a[1] / ESCALA)

    x += 23
    y = 23 - y

    circulo[y][x] = str(num_jugador)
    return circulo

while True:
    circulo = circle_gen()
    # Leer los datos del archivo CSV y agregar los personajes al mapa
    with open('pos_act.csv', 'r') as archivo_csv:
        reader = csv.reader(archivo_csv)
        num_jugador = 1
        for row in reader:
            equipo = row[0]
            jugador = row[1]
            x = float(row[2])
            y = float(row[3])
            circulo = agregar_pj((x, y), num_jugador, circulo)
            num_jugador += 1
    time.sleep(1)
    fil = len(circulo)
    with open("ascii2.txt", "w") as f:
        for _ in range(fil):
            circulo[_].append("\n")
            linea = ' '.join(circulo[_])
            f.writelines(linea)
