import math
import matplotlib.pyplot as plt
import numpy as np

def is_direction_vertical(direction):
    # Verifica si la dirección es un múltiplo de pi/2 (recta vertical)
    if round(math.cos(direction), 3) == 0:
        return True
    else:
        return False

def recta_creator(m:float, punto:list):
    b = punto[1] - punto[0] * m
    def recta(x):
        return m*x + b
    print(f"y={m}x + {b}")
    return recta

def heading_same_max(player1_position, player1_direction, player2_position, player2_direction):

    paralela_info = None

    if is_direction_vertical(player1_direction):
        if is_direction_vertical(player2_direction):
            if round(player1_position[0], 0) == round(player2_position[0], 0):
                if round(player1_direction, 3) == round(math.pi/2, 3):
                    if round(player2_direction, 3) == round(3*math.pi/2, 3):
                        if player1_position[1] < player2_position[1]:
                            return True
                        return False
                    return True
                if round(player2_direction, 3) == round(math.pi/2, 3):
                    if round(player1_direction, 3) == round(3*math.pi/2, 3):
                        if player2_position[1] < player1_position[1]:
                            return True
                        return False
                    return True
                return True
            return False

        if round(player1_direction, 3) == round(math.pi/2, 3):
            paralela_info = [round(player1_position[0], 0), math.pi/2, 1]
        else:
            paralela_info = [round(player1_position[0], 0), 3*math.pi/2, 1]


    if is_direction_vertical(player2_direction):
        if round(player1_direction, 3) == round(math.pi/2, 3):
            paralela_info = [round(player2_position[0], 0), math.pi/2, 1]
        else:
            paralela_info = [round(player2_position[0], 0), 3*math.pi/2, 1]

    
    if paralela_info != None:
        if paralela_info[2] == 1:
            m2 = round(math.tan(player2_direction), 3)
            recta2 = recta_creator(m2, player2_position)

            interseccion_y = recta2(paralela_info[0])

            if paralela_info[1] == math.pi/2:
                if interseccion_y > player1_position[1]:
                    if math.cos(player2_direction) > 0:
                        if player2_position[0] < player1_position[0]:
                            return True
                        return False
                    #sino,
                    if player2_position[0] > player1_position[0]:
                        return True
                    return False
                return False
            #sino,
            if interseccion_y < player1_position[1]:
                if math.cos(player2_direction) > 0:
                    if player2_position[0] < player1_position[0]:
                        return True
                    return False
                #sino,
                if player2_position[0] > player1_position[0]:
                    return True
                return False
            return False
        #sino,
        m1 = round(math.tan(player1_direction), 3)
        recta1 = recta_creator(m1, player1_position)

        interseccion_y = recta1(paralela_info[0])

        if paralela_info[1] == math.pi/2:
            if interseccion_y > player2_position[1]:
                if math.cos(player1_direction) > 0:
                    if player1_position[0] < player2_position[0]:
                        return True
                    return False
                #sino,
                if player1_position[0] > player2_position[0]:
                    return True
                return False
            return False
        #sino,
        if interseccion_y < player2_position[1]:
            if math.cos(player1_direction) > 0:
                if player1_position[0] < player2_position[0]:
                    return True
                return False
            #sino,
            if player1_position[0] > player2_position[0]:
                return True
            return False
        return False





    # Calcula las pendientes de las rectas de movimiento de los jugadores
    m1 = round(math.tan(player1_direction), 3)
    m2 = round(math.tan(player2_direction), 3)

    recta1 = recta_creator(m1, player1_position)
    recta2 = recta_creator(m2, player2_position)

    x1 = np.array([i for i in range(-500, 500)])
    y1 = recta1(x1)
    plt.plot(x1, y1)

    y2 = recta2(x1)

    plt.plot(x1, y2)

    plt.show()

    # Verifica si las pendientes son iguales (rectas paralelas)
    if m1 == m2:
        if round(player1_position[1], 0) == round(recta2(player1_position[0]), 0):      #CHEQUEO SI LAS RECTAS PARALELAS TIENEN ADEMÁS LA MISMA ORDENADA AL ORIGEN
            if m1 > 0:
                if player1_direction < math.pi:
                    if round(player1_direction + math.pi, 1) == round(player2_direction, 1):
                        if player1_position[0] <= player2_position[0]:
                            return True
                        return False
                    return True
                if player2_direction < math.pi:
                    if round(player2_direction + math.pi, 1) == round(player1_direction, 1):
                        if player2_position[0] <= player1_position[0]:
                            return True
                        return False
                    return True
                return True
            if m1 > 0:
                if player1_direction < math.pi:
                    if round(player1_direction + math.pi, 1) == round(player2_direction, 1):
                        if player1_position[0] >= player2_position[0]:
                            return True
                        return False
                    return True
                if player2_direction < math.pi:
                    if round(player2_direction + math.pi, 1) == round(player1_direction, 1):
                        if player2_position[0] >= player1_position[0]:
                            return True
                        return False
                    return True
                return True
            if m1 == 0:
                if round(player1_direction, 1) == 0:
                    if round(player1_direction + math.pi, 1) == round(player2_direction, 1):
                        if player1_position[0] <= player2_position[0]:
                            return True
                        return False
                    return True
                if round(player2_direction, 1) == 0:
                    if round(player2_direction + math.pi, 1) == round(player1_direction, 1):
                        if player2_position[0] <= player1_position[0]:
                            return True
                        return False
                    return True
    
    interseccion = round((-recta1(0) + recta2(0)) / (m1 - m2), 0)
    print(interseccion)

    if math.cos(player1_direction) > 0:
        if math.cos(player2_direction) > 0:
            if interseccion >= player1_position[0] and interseccion >= player2_position[0]:
                return True
            return False
        #sino,
        if interseccion >= player1_position[0] and interseccion <= player2_position[0]:
            return True
        return False
    #sino, 
    if math.cos(player2_direction) > 0:
        if interseccion <= player1_position[0] and interseccion >= player2_position[0]:
            return True
        return False
    #sino,
    if interseccion <= player1_position[0] and interseccion <= player2_position[0]:
        return True
    return False

player1_position = (1, 2)
player1_direction = math.pi/2

player2_position = (3, 4)
player2_direction = 5*math.pi/4

print(heading_same_max(player1_position, player1_direction, player2_position, player2_direction))
