import math

def recta_creator(m:float, punto:list):
    b = punto[1] - punto[0] * m
    def recta(x):
        return m*x + b
    return recta

def heading_same_max(player1_position, player1_direction, player2_position, player2_direction):

    # Calcula las pendientes de las rectas de movimiento de los jugadores
    m1 = round(math.tan(player1_direction), 3)
    m2 = round(math.tan(player2_direction), 3)

    recta1 = recta_creator(m1, player1_position)
    recta2 = recta_creator(m2, player2_position)

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
    
    interseccion = (-recta1(0) + recta2(0)) / (m1 - m2)

    if math.cos(player1_direction) > 0:
        
     
                
