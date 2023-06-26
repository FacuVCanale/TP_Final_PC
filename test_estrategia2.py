from communication.client.client import MountainClient
import time
import numpy as np
import math
# Importar clases
from class_dataAnalyst import DataAnalyst
from class_hiker import Hiker
# Importar estrategia
# from estrategia1 import strategy

c = MountainClient()

# Initialize DataAnalyst
dataAnalyst = DataAnalyst(c)
dataAnalysts = [dataAnalyst]


# Initialize hikers
lucas = Hiker(c,'CLIFF','lucas')
facu = Hiker(c,'CLIFF','facu')
fran = Hiker(c,'CLIFF','fran')
ivan = Hiker(c,'CLIFF','ivan')
hikers = [lucas, facu, fran, ivan]


# Function to update data on all Hykers and DataAnalyst
def update_all_data(hikers:list[Hiker],dataAnalysts:list[DataAnalyst]):
    for hiker in hikers:
        hiker.update_data()
    for dataAnalyst in dataAnalysts:
        dataAnalyst.update_data()
    

# Add and register team
hikers_names = [hiker.name for hiker in hikers]
c.add_team('CLIFF', hikers_names)
c.finish_registration()


# Definir Puntos y Estado de cada escalador
puntos_ivan = [(13500,13500),(14000,14000)]
estado_ivan = 'buscar_punto'


# Instructions
while not c.is_over():
    # Sleep server for testing
    time.sleep(0)

    # Ask for data of all hikers in map
    data = c.get_data()
    print("\n Server Info = ",data)

    # Update data of our hykers
    update_all_data(hikers,dataAnalysts)

    # Print usefull data of DataAnalyst
    dataAnalyst_info = dataAnalyst.get_all_info()
    print("\n DataAnalyst Info = ", dataAnalyst_info)
  

    # ------------------Codigo de prueba: Aca va la estrategia------------------

    print("GLOBAL",estado_ivan)
    print("GLOBAL",puntos_ivan)
    
    # Esto es la estrategia:

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

    directives = {
                    lucas.name: {'direction': lucas.direction_p((988,18245)), 'speed': lucas.speed_p((988,18245))},
                    facu.name: {'direction': facu.direction_p((988,18245)), 'speed': facu.speed_p((988,18245))},
                    fran.name: {'direction': fran.direction_GA(), 'speed': fran.speed_GA()},
                    ivan.name: {'direction': strategy(ivan,puntos_ivan,'buscar_punto')[0], 'speed': strategy(ivan,puntos_ivan,'buscar_punto')[1]},
                }
    
    # ------------------Codigo de prueba: Aca va la estrategia------------------

    # Give directives to server
    c.next_iteration('CLIFF', directives)