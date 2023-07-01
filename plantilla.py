
import time
import numpy as np
import math
# Import client:
from communication.client.client import MountainClient
# Import classes:
from strategy.class_dataAnalyst import DataAnalyst
from strategy.class_hiker import Hiker

# Import strategy:
# FIJARSE COMO IMPORTAR LA FUNCION DE ESTRATEGIA QUE USA GLOBAL

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
def update_all_data(hikers: list[Hiker],dataAnalysts: list[DataAnalyst], data):
    for hiker in hikers:
        hiker.update_data(data)
    for dataAnalyst in dataAnalysts:
        dataAnalyst.update_data(data)
    

# Add and register team
hikers_names = [hiker.name for hiker in hikers]
c.add_team('CLIFF', hikers_names)
c.finish_registration()

# Definir Puntos y Estado de cada escalador
    # POR EJEMPLO:
    # puntos_ivan = [(13500,13500),(14000,14000)]
    # estado_ivan = 'buscar_punto'


# Instructions
while not c.is_over():
    # Sleep server for testing
    # time.sleep(3)

    # Ask for data of all hikers in map
    data = c.get_data()
    print("\n Server Info = ",data)

    # Update data of our hykers
    update_all_data(hikers, dataAnalysts, data)

    # Print usefull data of DataAnalyst
    dataAnalyst_info = dataAnalyst.get_all_info()
    print("\n DataAnalyst Info = ", dataAnalyst_info)
  

    # ------------------Codigo de prueba: Aca va la estrategia------------------

    ivan_direction, ivan_speed = ivan.get_direction_and_vel_to_point_fixed(ivan.get_next_point_GA()[0], ivan.get_next_point_GA()[1])

    fran_direction, fran_speed = fran.get_direction_and_vel_to_point_fixed(fran.get_next_point_GA()[0], fran.get_next_point_GA()[1])

    directives = {
                    lucas.name: {'direction': lucas.direction_p((988,18245)), 'speed': lucas.speed_p((988,18245))},
                    facu.name: {'direction': facu.direction_p((988,18245)), 'speed': facu.speed_p((988,18245))},
                    fran.name: {'direction': fran.direction_GA(), 'speed': fran.speed_GA()},
                    ivan.name: {'direction': ivan_direction, 'speed': ivan_speed},
                }
    
    # ------------------Codigo de prueba: Aca va la estrategia------------------

    # Give directives to server
    c.next_iteration('CLIFF', directives)

