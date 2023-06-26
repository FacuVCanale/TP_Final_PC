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

#Set points for every hiker
lucas_points = [[8000, 15500], [-5000, 18750], [-12000, 13100]]
facu_points = [[270, 7500], [-14000, 744]]
fran_points = [[7500, 270], [744, -14000]]
ivan_points = [[15500, 8000], [18750, -5000], [13100, -12000]]

# Initialize hikers
lucas = Hiker('CLIFF','lucas', lucas_points)
facu = Hiker('CLIFF','facu', facu_points)
fran = Hiker('CLIFF','fran', fran_points)
ivan = Hiker('CLIFF','ivan', ivan_points)
hikers = [lucas, facu, fran, ivan]

# Function to update data on all Hykers and DataAnalyst
def update_all_data(hikers:list[Hiker],dataAnalysts:list[DataAnalyst], data):
    for hiker in hikers:
        hiker.update_data(data)
    for dataAnalyst in dataAnalysts:
        dataAnalyst.update_data(data)
    

# Add and register team
hikers_names = [hiker.name for hiker in hikers]
c.add_team('CLIFF', hikers_names)
c.finish_registration()

# Instructions
while not c.is_over():
    # Sleep server for testing
    time.sleep(0.1)

    # Ask for data of all hikers in map
    data = c.get_data()

    # Update data of our hykers
    update_all_data(hikers, dataAnalysts, data)

    # Print usefull data of DataAnalyst
    dataAnalyst_info = dataAnalyst.get_all_info()

    print("\n DataAnalyst Info = ")
    for item in dataAnalyst_info:
        if item != "n_max_pos":
            print(item)
            print(dataAnalyst_info[item])

    print("\n Server Info = ")
    for hiker in data["CLIFF"]:
        print(hiker)
        print(data["CLIFF"][hiker])


    lucas_new_d_and_s = lucas.strategy()
    facu_new_d_and_s = facu.strategy()
    fran_new_d_and_s = fran.strategy()
    ivan_new_d_and_s = ivan.strategy()

    
    directives = {
                    lucas.name: {'direction': lucas_new_d_and_s[0], 'speed': lucas_new_d_and_s[1]},
                    facu.name: {'direction': facu_new_d_and_s[0], 'speed': facu_new_d_and_s[1]},
                    fran.name: {'direction': fran_new_d_and_s[0], 'speed': fran_new_d_and_s[1]},
                    ivan.name: {'direction': ivan_new_d_and_s[0], 'speed': ivan_new_d_and_s[1]},
                }
    
    # Give directives to server
    c.next_iteration('CLIFF', directives)