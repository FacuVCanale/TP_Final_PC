from constants import *

from communication.client.client import MountainClient
import time
import numpy as np
import math
# Importar clases
from class_dataAnalyst import DataAnalyst
from class_hiker import Hiker
# Importar estrategia
# from estrategia1 import strategy

import random


c = MountainClient()

local_maxs = []

# Initialize DataAnalyst
dataAnalyst = DataAnalyst(c)
dataAnalysts = [dataAnalyst]

# Initialize hikers
lucas = Hiker('CLIFF','lucas', lucas_points, alpha=.5, beta=.7)
facu = Hiker('CLIFF','facu', facu_points, alpha=.5, beta= .8)         #ESTE TIENE GA
fran = Hiker('CLIFF','fran', fran_points, alpha=.5, beta=.5)
ivan = Hiker('CLIFF','ivan', ivan_points, alpha=.5, beta=.99)
hikers = [lucas, facu, fran, ivan]


# Function to update data on all Hykers and DataAnalyst
def update_all_data(hikers:list[Hiker],dataAnalysts:list[DataAnalyst], data):
    for hiker in hikers:
        hiker.update_data(data)
    for dataAnalyst in dataAnalysts:
        dataAnalyst.update_data(data)


def check_hikers_intersect(hikers, local_maxs, directives):
    for i in range(len(hikers)-1):
        for j in range(1, len(hikers)):
            if hikers[i].strat == "hike" and hikers[j] == "hike":
                direction_i = directives[hikers[i].name]["direction"]
                direction_j = directives[hikers[j].name]["direction"]
                coords, is_same_dir = hikers[i].going_same_max(hikers[j], direction_i, direction_j)
                if is_same_dir is True:
                    if len(coords) > 0:
                        local_maxs.append(coords)
                        distance_i = np.sqrt((hikers[i].get_data("x") - coords[0]) ** 2 + (hikers[i].get_data("y") - coords[1]) ** 2)
                        distance_j = np.sqrt((hikers[j].get_data("x") - coords[0]) ** 2 + (hikers[j].get_data("y") - coords[1]) ** 2)
                        if distance_j > distance_i:
                            hikers[j].change_strat("follow_points")
                            direction_j, speed_j = hikers[j].strategy(local_maxs)
                            directives[hikers[j].name]["direction"] = direction_j
                            directives[hikers[j].name]["speed"] = speed_j
                        else:
                            hikers[i].change_strat("follow_points")
                            direction_i, speed_i = hikers[i].strategy(local_maxs)
                            directives[hikers[i].name]["direction"] = direction_i
                            directives[hikers[i].name]["speed"] = speed_i
                    else:
                        hikers[i].change_strat("follow_points")
                        direction_i, speed_i = hikers[i].strategy(local_maxs)
                        directives[hikers[i].name]["direction"] = direction_i
                        directives[hikers[i].name]["speed"] = speed_i
                print("ENTRE\nENTRE\nENTRE\nintersección\nENTRE\nENTRE\nENTRE\n")

def check_hikers_local_max(local_maxs, hikers, directives):
    for hiker in hikers:
        if hiker.strat == "hike":
            for local_max in local_maxs:
                if hiker.is_near_point(local_max) is True:
                    #CAMBIAR A GRADIENT DESCENT, QUE VAYA A CUALQUIER DIRECCIÓN OPUESTA (DIR + PI/2 + PI*RANDOMENTRE0Y1)
                    hiker.change_strat("follow_points")
                    direction, speed = hiker.strategy(local_maxs)
                    directives[hiker.name]["direction"] = direction
                    directives[hiker.name]["speed"] = speed
                    print("ENTRE\nENTRE\nENTRE\nlocalmax\nENTRE\nENTRE\nENTRE\n")

def check_hikers_out_of_bounds(hikers, local_maxs, directives):
    # Check if a hyker is going out of bounds   
    for hiker in hikers:
        if hiker.check_out_of_bounds():
            print(hiker.name)
            print("ME ESTROY POR IR\nME ESTROY POR IR\nME ESTROY POR IR\nME ESTROY POR IR\nME ESTROY POR IR\n")
            if len(hiker.puntos) != 0:
                hiker.change_strat('follow_points')
            elif hiker.strat == "descent":
                hiker.strat == "hike"
            elif hiker.strat == "hike":
                hiker.strat == "descent"
            # hiker.puntos = hiker.puntos[1:] PARA TESTEAR AGREGANDO UN PUNTO A LA LSITA
            hiker_dir_speed = hiker.strategy(local_maxs)
            directives[hiker.name] = {'direction': hiker_dir_speed[0], 'speed': hiker_dir_speed[1]}

def check_hikers_stopped(hikers, local_maxs, directives):
    for hiker in hikers:
        if hiker.last_data == hiker.data:
            if len(hiker.puntos) == 0:
                hiker.puntos.append([random.randint(-14000, 14000), random.randint(-14000, 14000)])
            hiker.strat == "follow_points"
            hiker_dir_speed = hiker.strategy(local_maxs)
            directives[hiker.name] = {'direction': hiker_dir_speed[0], 'speed': hiker_dir_speed[1]}
            
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

    
    if not dataAnalyst.check_win()[0]:# If no team won

        fran.change_strat("hike")

        lucas_new_d_and_s = lucas.strategy(local_maxs, "GA")
        facu_new_d_and_s = facu.strategy(local_maxs, "GA")
        fran_new_d_and_s = fran.strategy(local_maxs, "GA")
        ivan_new_d_and_s = ivan.strategy(local_maxs, "GA")

        directives = {
                        lucas.name: {'direction': lucas_new_d_and_s[0], 'speed': lucas_new_d_and_s[1]},
                        facu.name: {'direction': facu_new_d_and_s[0], 'speed': facu_new_d_and_s[1]},
                        fran.name: {'direction': fran_new_d_and_s[0], 'speed': fran_new_d_and_s[1]},
                        ivan.name: {'direction': ivan_new_d_and_s[0], 'speed': ivan_new_d_and_s[1]},
                    }

        

    else: # If a team wins, all our hikers go to win pos
        print(f'Alguien gano escaladores yendo a pos {dataAnalyst.check_win()[1]}')
        x_y_win = (dataAnalyst.check_win()[1][0],dataAnalyst.check_win()[1][1])
        directives = {
                lucas.name: {'direction': lucas.direction_p(x_y_win), 'speed': lucas.speed_p(x_y_win)},
                facu.name: {'direction': facu.direction_p(x_y_win), 'speed': facu.speed_p(x_y_win)},
                fran.name: {'direction': fran.direction_p(x_y_win), 'speed': fran.speed_p(x_y_win)},
                ivan.name: {'direction': ivan.direction_p(x_y_win), 'speed': ivan.speed_p(x_y_win)},
            }


    #Checks if hikers are going to the same place in GA.
    check_hikers_intersect(hikers, local_maxs, directives)

    check_hikers_local_max(local_maxs, hikers, directives)

    check_hikers_stopped(hikers, local_maxs, directives)

    check_hikers_out_of_bounds(hikers, local_maxs, directives)

    print(fran.last_data["z"])
    print(fran.data["z"])
    print(fran.data["z"] - fran.last_data["z"])

    # Give directives to server
    c.next_iteration('CLIFF', directives)