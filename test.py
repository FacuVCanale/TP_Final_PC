import math

# Definir el tamaño del mapa ASCII
MAP_SIZE = 100  # Ajusta este valor para obtener el nivel de detalle deseado en el mapa

# Función para generar el mapa ASCII
def generar_mapa(jugadores):
    # Crear una matriz vacía para el mapa
    mapa = [[' ' for _ in range(MAP_SIZE)] for _ in range(MAP_SIZE)]

    # Calcular el centro del mapa
    centro = MAP_SIZE // 2

    # Dibujar el círculo del mapa
    for y in range(MAP_SIZE):
        for x in range(MAP_SIZE):
            distancia = math.sqrt((x - centro) ** 2 + (y - centro) ** 2)
            if distancia <= centro:
                mapa[y][x] = '#'

    # Colocar los jugadores en el mapa
    for jugador in jugadores:
        x, y = jugador
        x = int((x / 23000) * MAP_SIZE)
        y = int((y / 23000) * MAP_SIZE)
        if 0 <= x < MAP_SIZE and 0 <= y < MAP_SIZE:
            mapa[y][x] = 'P'

    # Convertir el mapa a una cadena y mostrarlo en la terminal
    for fila in mapa:
        print(''.join(fila))


# Ejemplo de uso
jugadores = [(11500, 8000), (5000, 15000), (20000, 12000)]  # Ejemplo de coordenadas de jugadores
generar_mapa(jugadores)
