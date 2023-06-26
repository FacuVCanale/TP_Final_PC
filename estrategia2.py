from class_hiker import Hiker

def strategy(hiker,list_of_points,estado):
    global puntos_ivan
    global estado_ivan

    estado = estado_ivan
    puntos_ivan = puntos_ivan

    # tolerancia econtrar punto
    n = 50 
    # tolerancia derivada parcial
    n2 = 0.001

    # check len of list
    next_point = list_of_points[0]

    x = hiker.get_data('x')
    y = hiker.get_data('y')
    z = hiker.get_data('z')

    dx = hiker.get_data('inclinacion_x')
    dy = hiker.get_data('inclinacion_y')


    if estado == 'buscar_punto':
        # ver en num negativos
        if  (x > (next_point[0] - n) and x < (next_point[1] + n)) \
            and (y > (next_point[0] - n) and y < (next_point[1] + n)):
            print("Estoy en el punto", x, y)
            
            puntos_ivan = puntos_ivan[1:]
            estado_ivan = 'escalar'

            direction = 0
            speed = 0
        
        else:
            direction = hiker.direction_p(next_point)
            speed = hiker.speed_p(next_point)
            print("buscando punto")


    elif estado == 'escalar':
        
        if abs(dx) < n2 and abs(dy) < n2:
            print('estoy en un max local')
            estado_ivan = 'buscar_punto'
            direction = 0
            speed = 0
        else:
            print("Escalando")
            direction = hiker.direction_GA()
            speed = hiker.speed_GA()

    return direction,speed