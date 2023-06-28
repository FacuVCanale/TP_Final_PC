from communication.client.client import MountainClient
import time
import numpy as np
import math
from class_dataAnalyst import DataAnalyst
from class_hiker import Hiker

c = MountainClient()

# Initialize DataAnalyst
dataAnalyst = DataAnalyst()
dataAnalysts = [dataAnalyst]


# Initialize hikers
lucas = Hiker(c,'CLIFF','lucas',0.4,0.5,0.1)
facu = Hiker(c,'CLIFF','facu',0.5,0.5,0.3)
fran = Hiker(c,'CLIFF','fran',0.7,0.5,0.7)
ivan = Hiker(c,'CLIFF','ivan',0.9,0.5,0.9)
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


# Iterations
while not c.is_over():
    # Sleep server for testing
    # time.sleep(3)

    # Ask for data of all hikers in map
    data = c.get_data()
    print("\n Server Info = ",data)

    # Update data of our hykers
    update_all_data(hikers,dataAnalysts)

    # Print usefull data of DataAnalyst
    dataAnalyst_info = dataAnalyst.get_all_info()
    print("\n DataAnalyst Info = ", dataAnalyst_info)
  

    # ------------------Codigo de prueba------------------

    lucas_direction, lucas_speed = lucas.get_direction_and_vel_to_point_fixed(lucas.get_next_point_GA()[0], lucas.get_next_point_GA()[1])

    facu_direction, facu_speed = facu.get_direction_and_vel_to_point_fixed(facu.get_next_point_GA()[0], facu.get_next_point_GA()[1])

    fran_direction, fran_speed = fran.get_direction_and_vel_to_point_fixed(fran.get_next_point_GA()[0], fran.get_next_point_GA()[1])

    ivan_direction, ivan_speed = ivan.get_direction_and_vel_to_point_fixed(ivan.get_next_point_GA()[0], ivan.get_next_point_GA()[1])

    directives = {
                    lucas.name: {'direction': lucas_direction, 'speed': lucas_speed},
                    facu.name: {'direction': facu_direction, 'speed': facu_speed},
                    fran.name: {'direction': fran_direction, 'speed': fran_speed},
                    ivan.name: {'direction': ivan_direction, 'speed': ivan_speed},
                }
    
    # ------------------Codigo de prueba------------------

    # Give directives to server
    c.next_iteration('CLIFF', directives)

