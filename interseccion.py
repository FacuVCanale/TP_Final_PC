import math

def are_players_heading_same_point(player1_position, player1_direction, player2_position, player2_direction):
    # Verifica si alguna de las direcciones es un múltiplo de pi/2 (recta vertical)
    if is_direction_vertical(player1_direction) or is_direction_vertical(player2_direction):
        if round(player1_position[0], 0) == round(player2_position[0], 0):
            if (round(player1_direction, 3) == round(math.pi/2, 3) and round(player2_direction, 3) == round(3*math.pi/2, 3)) or (round(player2_direction, 3) == round(math.pi/2, 3) and round(player1_direction, 3) == round(3*math.pi/2, 3)):
                return True
            else:
                return False
        elif is_direction_vertical(player1_direction) and is_direction_vertical(player2_direction):
            return False
        elif is_direction_vertical(player1_direction):
            recta = player1_position[0]
            #SEGUIR
        elif is_direction_vertical(player2_direction):
            recta = player2_position[0]
            #SEGUIR
        return False            #POR AHORA


    # Calcula las pendientes de las rectas de movimiento de los jugadores
    m1 = round(math.tan(player1_direction), 3)
    m2 = round(math.tan(player2_direction), 3)

    # Verifica si las pendientes son iguales (rectas paralelas)
    if m1 == m2:
        return False

    # Calcula las intersecciones en x de las rectas
    x_intersect = (player2_position[1] - player1_position[1] + m1 * player1_position[0] - m2 * player2_position[0]) / (m1 - m2)

    # Calcula las intersecciones en y de las rectas
    y_intersect = m1 * (x_intersect - player1_position[0]) + player1_position[1]

    # Verifica si las intersecciones están dentro del rango de las posiciones actuales
    if (min(player1_position[0], player1_position[0] + math.cos(player1_direction)) <= x_intersect <= max(player1_position[0], player1_position[0] + math.cos(player1_direction))) and (min(player2_position[0], player2_position[0] + math.cos(player2_direction)) <= x_intersect <= max(player2_position[0], player2_position[0] + math.cos(player2_direction))) and (min(player1_position[1], player1_position[1] + math.sin(player1_direction)) <= y_intersect <= max(player1_position[1], player1_position[1] + math.sin(player1_direction))) and (min(player2_position[1], player2_position[1] + math.sin(player2_direction)) <= y_intersect <= max(player2_position[1], player2_position[1] + math.sin(player2_direction))):
        return True
    else:
        return False

def is_direction_vertical(direction):
    # Verifica si la dirección es un múltiplo de pi/2 (recta vertical)
    if round(math.cos(direction), 4) == 0:
        return True
    else:
        return False

# Ejemplo de uso
player1_position = (1, 2)  # Posición actual del jugador 1
player1_direction = math.pi/2  # Dirección del jugador 1 en radianes (recta vertical)

player2_position = (3, 4)  # Posición actual del jugador 2
player2_direction = 3*math.pi/2  # Dirección del jugador 2 en radianes (recta vertical)

same_point = are_players_heading_same_point(player1_position, player1_direction, player2_position, player2_direction)
if same_point:
    print("Los jugadores están yendo al mismo punto.")
else:
    print("Los jugadores no están yendo al mismo punto.")
