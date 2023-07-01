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
from facu_inter import distance


c = MountainClient()

local_maxs = []

# Initialize DataAnalyst
dataAnalyst = DataAnalyst(c)
dataAnalysts = [dataAnalyst]

# Initialize hikers
lucas = Hiker('CLIFF','lucas', lucas_points, alpha=.5, beta=.7)
facu = Hiker('CLIFF','facu', facu_points, alpha=.5, beta= .8)
fran = Hiker('CLIFF','fran', fran_points, alpha=.5, beta=.5)
ivan = Hiker('CLIFF','ivan', ivan_points, alpha=.5, beta=.99)
hikers = [lucas, facu, fran, ivan]


# Function to update data on all Hykers and DataAnalyst
def update_all_data(hikers:list[Hiker],dataAnalysts:list[DataAnalyst], data):
    """
    Updates data of all hikers and DataAnlysts
    """
    for hiker in hikers:
        hiker.update_data(data)
    for dataAnalyst in dataAnalysts:
        dataAnalyst.update_data(data)

def update_directive(hiker, local_maxs, directives):
    hiker.change_strat("follow_points")
    direction, speed = hiker.strategy(local_maxs)
    directives[hiker.name]["direction"] = direction
    directives[hiker.name]["speed"] = speed

def check_hikers_intersect(hikers, local_maxs: list, directives: dict) -> None:
    for i in range(3):
        for j in range(i + 1, 4):
            hiker_i, hiker_j = hikers[i], hikers[j]
            direction_i = directives[hiker_i.name]["direction"]
            direction_j = directives[hiker_j.name]["direction"]
            coords, is_same_dir = hiker_i.going_same_max(hiker_j, direction_i, direction_j)
            if hiker_i.strat == "hike" and hiker_j.strat == "hike" and is_same_dir:
                if coords:
                    local_maxs.append(coords)
                    hiker_i_coords = (hiker_i.get_data("x"), hiker_i.get_data("y"))
                    hiker_j_coords = (hiker_j.get_data("x"), hiker_j.get_data("y"))
                    distance_i = distance(hiker_i_coords, coords)
                    distance_j = distance(hiker_j_coords, coords)
                    if distance_j > distance_i:
                        update_directive(hiker_j, local_maxs, directives)
                    else:
                        update_directive(hiker_i, local_maxs, directives)
                else:
                    update_directive(hiker_i, local_maxs, directives)


def check_hikers_local_max(local_maxs, hikers:list, directives:dict)->None:
    for hiker in hikers:
        if hiker.strat == "hike":
            for local_max in local_maxs:
                if hiker.is_near_point(local_max) is True:
                    hiker.change_strat("follow_points")
                    direction, speed = hiker.strategy(local_maxs)
                    directives[hiker.name]["direction"] = direction
                    directives[hiker.name]["speed"] = speed

def check_hikers_stopped(hikers, local_maxs:list, directives:dict):
    """
    This function is used after many iterations when the first strat doesnt work
    makes hikers search for golbal max in a random way
    """
    for hiker in hikers:
        if hiker.last_data == hiker.data:
            if len(hiker.puntos) == 0:
                hiker.puntos.append([random.randint(-14000, 14000), random.randint(-14000, 14000)])
            hiker.strat == "follow_points"
            hiker_dir_speed = hiker.strategy(local_maxs)
            directives[hiker.name] = {'direction': hiker_dir_speed[0], 'speed': hiker_dir_speed[1]}

def check_hikers_out_of_bounds(hikers, local_maxs:list, directives:dict)->None:
    """
    Detects if a hiker is going to go out of bounds and redirects it to other position
    using a strategy. Changes the directives of the hiker before they are sent to the server
    (direction and speed)

    Parameters
    ----------
    local_maxs : list

    directives : dict

    """ 
    for hiker in hikers:
        if hiker.check_out_of_bounds():
            # print(hiker.name)
            # print("ME ESTROY POR IR DEL MAPA")
            if len(hiker.puntos) != 0:
                hiker.change_strat('follow_points')
            elif hiker.strat == "descent":
                hiker.strat == "hike"
            elif hiker.strat == "hike":
                hiker.strat == "descent"
            # hiker.puntos = hiker.puntos[1:] PARA TESTEAR AGREGANDO UN PUNTO A LA LSITA
            hiker_dir_speed = hiker.strategy(local_maxs)
            directives[hiker.name] = {'direction': hiker_dir_speed[0], 'speed': hiker_dir_speed[1]}

def check_hikers(hikers:list, local_maxs:list, directives:dict):
    for hiker in hikers:
        pass

            
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