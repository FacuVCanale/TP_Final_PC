import time
import random

from strategy.facu_inter import distance
from strategy.constants import *

from communication.client.client import MountainClient
from strategy.class_dataAnalyst import DataAnalyst
from strategy.class_hiker import Hiker

def update_all_data(hikers: list[Hiker], dataAnalyst: DataAnalyst, data:dict[str, dict][str, dict][str, float]) -> None:
    """
    Updates data of all hikers and the DataAnalyst.

    Parameters:
    - hikers: List of Hiker objects.
    - dataAnalysts: DataAnalyst object.
    - data: Data received from the server.

    Returns:
        None
    """
    for hiker in hikers:
        hiker.update_data(data)
    dataAnalyst.update_data(data)

def check_hiker_local_max(hiker: Hiker, local_maxs: list[list][float, float], directives: dict[str, dict][str, float]) -> None:
    """
    Checks if a hiker is near any local maximum and updates its strategy and directives accordingly.

    Parameters:
    - hiker: Hiker object.
    - local_maxs: list of local maximum coordinates.
    - directives: dictionary containing the directives for each hiker.

    Returns:
        None
    """
    if hiker.strat == "hike":
        for local_max in local_maxs:
            if hiker.is_near_point(local_max):
                hiker.change_strat("follow_points")
                direction, speed = hiker.strategy(local_maxs)
                directives[hiker.name]["direction"] = direction
                directives[hiker.name]["speed"] = speed

def check_hiker_stopped(hiker: Hiker, local_maxs: list[list][float, float], directives: dict[str, dict][str, float]) -> None:
    """
    Checks if a hiker has stopped and updates its strategy and directives accordingly.

    Parameters:
    - hiker: Hiker object.
    - local_maxs: List of local maximum coordinates.
    - directives: Dictionary containing the directives for each hiker.

    Returns:
        None
    """
    if hiker.last_data == hiker.data:
        if len(hiker.points) == 0:
            hiker.points.append([random.randint(-14000, 14000), random.randint(-14000, 14000)])
        hiker.strat = "follow_points"
        hiker_dir_speed = hiker.strategy(local_maxs)
        directives[hiker.name] = {'direction': hiker_dir_speed[0], 'speed': hiker_dir_speed[1]}

def update_directive(hiker: Hiker, local_maxs: list[list][float, float], directives: dict[str, dict][str, float], strat: str) -> None:
    """
    Updates the strategy and directives for a hiker.

    Parameters:
    - hiker: Hiker object.
    - local_maxs: List of local maximum coordinates.
    - directives: Dictionary containing the directives for each hiker.
    - strat: New strategy for the hiker.

    Returns:
        None
    """
    hiker.change_strat(strat)
    direction, speed = hiker.strategy(local_maxs)
    directives[hiker.name]["direction"] = direction
    directives[hiker.name]["speed"] = speed

def check_hiker_intersect(hiker1: Hiker, hikers: list[Hiker], local_maxs: list[list][float, float], directives: dict[str, dict][str, float]) -> None:
    """
    Checks if a hiker intersects with any other hiker and updates their directives accordingly.

    Parameters:
    - hiker1: Hiker object.
    - hikers: List of Hiker objects.
    - local_maxs: List of local maximum coordinates.
    - directives: Dictionary containing the directives for each hiker.

    Returns:
        None
    """
    for hiker2 in hikers:
        if hiker2 == hiker1:
            continue
        direction1 = directives[hiker1.name]["direction"]
        direction2 = directives[hiker2.name]["direction"]
        coords, is_same_dir = hiker1.going_same_max(hiker2, direction1, direction2)
        if hiker1.strat == "hike" and hiker2.strat == "hike" and is_same_dir:
            if len(coords) > 0:
                local_maxs.append(coords)
                hiker1coords = (hiker1["x"], hiker1["y"])
                hiker2coords = (hiker2["x"], hiker2["y"])
                distance_i = distance(hiker1coords, coords)
                distance_j = distance(hiker2coords, coords)
                if distance_j > distance_i:
                    update_directive(hiker2, local_maxs, directives, "follow_points")
                else:
                    update_directive(hiker1, local_maxs, directives, "follow_points")
            else:
                update_directive(hiker1, local_maxs, directives, "follow_points")

def check_hiker_out_of_bounds(hiker: Hiker, local_maxs: list[list][float, float], directives: dict[str, dict][str, float]) -> None:
    """
    Checks if a hiker is going out of bounds and updates its strategy and directives accordingly.

    Parameters:
    - hiker: Hiker object.
    - local_maxs: List of local maximum coordinates.
    - directives: Dictionary containing the directives for each hiker.

    Returns:
        None
    """
    if hiker.check_out_of_bounds():
        if len(hiker.points) != 0:
            hiker.change_strat('follow_points')
        elif hiker.strat == "descent":
            hiker.strat = "hike"
        elif hiker.strat == "hike":
            hiker.strat = "descent"
        hiker_dir_speed = hiker.strategy(local_maxs)
        directives[hiker.name] = {'direction': hiker_dir_speed[0], 'speed': hiker_dir_speed[1]}

def check_hikers(hikers: list[Hiker], local_maxs: list[list][float, float], directives: dict[str, dict][str, float]) -> None:
    """
    Checks the behavior of all hikers and updates their directives if needed.

    Parameters:
    - hikers: List of Hiker objects.
    - local_maxs: List of local maximum coordinates.
    - directives: Dictionary containing the directives for each hiker.

    Returns:
        None
    """
    for hiker in hikers:
        check_hiker_local_max(hiker, local_maxs, directives)
        check_hiker_stopped(hiker, local_maxs, directives)
        check_hiker_intersect(hiker, hikers, local_maxs, directives)
        check_hiker_out_of_bounds(hiker, local_maxs, directives)


def main() -> None:
    """
    The main function is the entry point of the program and controls the execution flow.
    It initializes the necessary objects, such as the MountainClient, DataAnalyst, and a list of Hiker objects.

    The function enters a while loop that continues until the game is over.
    Within the loop, it retrieves data from the server using the get_data method of the MountainClient object.

    It then prints useful information from the DataAnalyst and the server.
    
    If no team has won yet, the hikers follow their strategy.
    If a team has won, the hikers are directed towards the win coordinates.

    Next, the function checks the behavior of the hikers and updates the directives if necessary.

    Finally, the function gives the directives to the server.

    Returns:
        None
    """

    # Initialize the Client
    c = MountainClient()

    # Initialize DataAnalyst
    dataAnalyst = DataAnalyst(c)
    dataAnalysts = [dataAnalyst]

    # Initialize hikers
    lucas = Hiker('CLIFF', 'lucas', lucas_points, alpha=0.5, beta=0.7)
    facu = Hiker('CLIFF', 'facu', facu_points, alpha=0.5, beta=0.8)
    fran = Hiker('CLIFF', 'fran', fran_points, strat="follow_points", alpha=0.5, beta=0.5)
    ivan = Hiker('CLIFF', 'ivan', ivan_points, alpha=0.5, beta=0.99)
    hikers = [lucas, facu, fran, ivan]

    # Initialize empty list for saving the local maximums
    local_maxs = []

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

        # Update data of our hikers
        update_all_data(hikers, dataAnalysts, data)

        # Print useful data of DataAnalyst
        dataAnalyst_info = dataAnalyst.get_all_info()
        print("\n DataAnalyst Info = ")
        for item in dataAnalyst_info:
            if item != "n_max_pos":
                print(item)
                print(dataAnalyst_info[item])

        # Print useful data received from the server
        print("\n Server Info = ")
        for hiker in data["CLIFF"]:
            print(hiker)
            print(data["CLIFF"][hiker])
        
        # If no team won, players follow their strategy.
        if not dataAnalyst.check_win()[0]:

            lucas_new_d_and_s = lucas.strategy(local_maxs, "G")
            facu_new_d_and_s = facu.strategy(local_maxs, "G")
            fran_new_d_and_s = fran.strategy(local_maxs, "G")
            ivan_new_d_and_s = ivan.strategy(local_maxs, "G")

            directives = {
                lucas.name: {'direction': lucas_new_d_and_s[0], 'speed': lucas_new_d_and_s[1]},
                facu.name: {'direction': facu_new_d_and_s[0], 'speed': facu_new_d_and_s[1]},
                fran.name: {'direction': fran_new_d_and_s[0], 'speed': fran_new_d_and_s[1]},
                ivan.name: {'direction': ivan_new_d_and_s[0], 'speed': ivan_new_d_and_s[1]},
            }

        # If a team wins, all our hikers go to the win coordinates
        else:  
            print(f'Alguien gano escaladores yendo a pos {dataAnalyst.check_win()[1]}')
            x_y_win = (dataAnalyst.check_win()[1][0], dataAnalyst.check_win()[1][1])
            directives = {
                lucas.name: {'direction': lucas.direction_p(x_y_win), 'speed': lucas.speed_p(x_y_win)},
                facu.name: {'direction': facu.direction_p(x_y_win), 'speed': facu.speed_p(x_y_win)},
                fran.name: {'direction': fran.direction_p(x_y_win), 'speed': fran.speed_p(x_y_win)},
                ivan.name: {'direction': ivan.direction_p(x_y_win), 'speed': ivan.speed_p(x_y_win)},
            }

        # Check hikers behavior and update directives if needed
        check_hikers(hikers, local_maxs, directives)

        # Give directives to server
        c.next_iteration('CLIFF', directives)

if __name__ == "__main__":
    main()