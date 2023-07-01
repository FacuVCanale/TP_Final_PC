from communication.client.client import MountainClient
import time
import numpy as np
import math
from strategy.tpf_CLIFF_class_dataAnalyst import DataAnalyst
from strategy.tpf_CLIFF_class_hiker import Hiker

c = MountainClient()

# Initialize DataAnalyst
dataAnalyst = DataAnalyst()
dataAnalysts = [dataAnalyst]


# Initialize hikers
lucas = Hiker('CLIFF','lucas')  
facu = Hiker('CLIFF','facu')
fran = Hiker('CLIFF','fran')
ivan = Hiker('CLIFF','ivan')
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

    ivan_points_GA = ivan.get_next_point_MGA()
    ivan_direction, ivan_speed = ivan.get_direction_and_vel_to_point_JUSTO(ivan_points_GA[0], ivan_points_GA[1])

    fran_points_GA = fran.get_next_point_MGA()
    fran_direction, fran_speed = fran.get_direction_and_vel_to_point_fixed(fran_points_GA[0], fran_points_GA[1])

    directives = {
                    lucas.name: {'direction': lucas.get_direction_and_vel_to_point_JUSTO(100,100)[0], 'speed': lucas.get_direction_and_vel_to_point_JUSTO(100,100)[1]},
                    facu.name: {'direction': facu.get_direction_and_vel_to_point_JUSTO(100,100)[0], 'speed': facu.get_direction_and_vel_to_point_JUSTO(100,100)[1]},
                    fran.name: {'direction': fran_direction, 'speed': fran_speed},
                    ivan.name: {'direction': ivan_direction, 'speed': ivan_speed},
                }
    
    # ------------------Codigo de prueba------------------

    # Give directives to server
    c.next_iteration('CLIFF', directives)

