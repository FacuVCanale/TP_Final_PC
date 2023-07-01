import math
import numpy as np

def distance(point1, point2) -> float:
    """
    Calculate the Euclidean distance between two points.

    Parameters:
        point1 (list): The coordinates of the first point. [x1, y1]
        point2 (list): The coordinates of the second point. [x2, y2]

    Returns:
        float: The Euclidean distance between the two points.
    """
    return np.sqrt((point2[0]-point1[0]) ** 2 + (point2[1]-point1[1]) ** 2)

def is_direction_vertical(direction:float) -> bool:
    """
    Check if the direction is a multiple of pi/2 (vertical line).

    Parameters:
        direction (float): The direction angle in radians.

    Returns:
        bool: True if the direction is vertical, False otherwise.
    """
    if round(math.cos(direction), 3) == 0:
        return True
    else:
        return False

def linear_creator(m:float, punto:list):
    """
    Create a linear function (recta) based on the slope and a point on the line.

    Parameters:
        m (float): The slope of the line.
        punto (list): The coordinates of a point on the line. [x, y]

    Returns:
        function: A linear function (recta) that calculates y for a given x.
    """
    b = punto[1] - punto[0] * m
    def recta(x):
        return round(m*x + b, 0)
    return recta

def check_distance(point1:list, point2:list, max_distance:float=18000*np.sqrt(2)) -> bool:
    """
    Check if the distance between two points is within a maximum threshold.

    Parameters:
        point1 (list): The coordinates of the first point. [x1, y1]
        point2 (list): The coordinates of the second point. [x2, y2]
        max_distance (float): The maximum allowed distance. Default is 18000 * sqrt(2).

    Returns:
        bool: True if the distance is within the threshold, False otherwise.
    """
    distance_calc = distance(point1, point2)
    return True if distance_calc <= max_distance else False

def check_vertical_intersection(player1_position:list, player1_direction:float, player2_position:list, player2_direction:float) -> tuple[list, bool]:
    """
    Check if two lines defined by a point and direction have a vertical intersection.

    Parameters:
        player1_position (list): The coordinates of the first line's point. [x1, y1]
        player1_direction (float): The direction angle of the first line in radians.
        player2_position (list): The coordinates of the second line's point. [x2, y2]
        player2_direction (float): The direction angle of the second line in radians.

    Returns:
        tuple: A pair of lists representing the coordinates of the intersection point
            and a boolean indicating if the lines are heading towards each other.
            If there is no intersection or the calculation is not possible, returns (None, None).
    """
    if player1_direction == round(math.pi/2, 3):
        if player2_direction == round(player1_direction + math.pi, 3):
            if player1_position[1] < player2_position[1]:
                return [], True
            return [], False
        return [], True
    return None, None

def calculate_parallel_info(player_position:list, player_direction:float, player_num:int) -> list[float, float, int]:
    """
    Calculate the parallel information for a player's position and direction.

    Parameters:
        player_position (list): The coordinates of the player's position. [x, y]
        player_direction (float): The direction angle of the player in radians.
        player_num (int): The number asigned to the player.

    Returns:
        list: The parallel information in the format [x, direction, mode].
            - x: The x-coordinate of the parallel line.
            - direction: The direction angle of the parallel line.
            - player: indicates if it is player 1 or 2.
    """
    if round(player_direction, 3) == round(math.pi/2, 3):
        parallel_info = [round(player_position[0], 0), math.pi/2, player_num]
    else:
        parallel_info = [round(player_position[0], 0), 3*math.pi/2, player_num]
    return parallel_info

def calculate_coords(coords:list, player1_position:list, player2_position:list, radius:float) -> tuple[list, bool]:
    """
    Calculate the possible intersection coordinates based on player positions and radius.

    Parameters:
        coords (list): The coordinates of the potential intersection point. [x, y]
        player1_position (list): The coordinates of the first player's position. [x1, y1]
        player2_position (list): The coordinates of the second player's position. [x2, y2]
        radius (float): The radius of the intersection area.

    Returns:
        tuple: A pair of the intersection coordinates and a boolean indicating if it's possible.
            If the coordinates are not possible, returns ([], False).
    """
    is_possible = check_distance(player1_position, coords, radius) and check_distance(player2_position, coords, radius)
    if not is_possible:
        coords = []
        return coords, False
    return coords, True

def check_positive_slope_intersection(player1_position:list, player1_direction:float, player2_position:list, player2_direction:float) -> tuple[list, bool]:
    """
    Check if two lines with positive slope have an intersection.

    Parameters:
        player1_position (list): The coordinates of the first player's position. [x1, y1]
        player1_direction (float): The direction angle of the first player in radians.
        player2_position (list): The coordinates of the second player's position. [x2, y2]
        player2_direction (float): The direction angle of the second player in radians.

    Returns:
        tuple: A pair of lists representing the coordinates of the intersection point
            and a boolean indicating if the lines are heading towards each other.
            If there is no intersection or the calculation is not possible, returns (None, None).
    """
    if player1_direction < math.pi:
        if round(player1_direction + math.pi, 1) == round(player2_direction, 1):
            if player1_position[0] < player2_position[0]:
                return [], True
            return [], False
        return [], True
    return None, None

def check_negative_slope_intersection(player1_position:list, player1_direction:float, player2_position:list, player2_direction:float) -> tuple[list, bool]:
    """
    Check if two lines with negative slope have an intersection.

    Parameters:
        player1_position (list): The coordinates of the first player's position. [x1, y1]
        player1_direction (float): The direction angle of the first player in radians.
        player2_position (list): The coordinates of the second player's position. [x2, y2]
        player2_direction (float): The direction angle of the second player in radians.

    Returns:
        tuple: A pair of lists representing the coordinates of the intersection point
            and a boolean indicating if the lines are heading towards each other.
            If there is no intersection or the calculation is not possible, returns (None, None).
    """
    if player1_direction < math.pi:
        if round(player1_direction + math.pi, 1) == round(player2_direction, 1):
            if player1_position[0] > player2_position[0]:
                return [], True
            return [], False
        return [], True
    return None, None

def check_zero_slope_intersection(player1_position:list, player1_direction:float, player2_position:list, player2_direction:float) -> tuple[list, bool]:
    """
    Check if two lines with zero slope have an intersection.

    Parameters:
        player1_position (list): The coordinates of the first player's position. [x1, y1]
        player1_direction (float): The direction angle of the first player in radians.
        player2_position (list): The coordinates of the second player's position. [x2, y2]
        player2_direction (float): The direction angle of the second player in radians.

    Returns:
        tuple: A pair of lists representing the coordinates of the intersection point
            and a boolean indicating if the lines are heading towards each other.
            If there is no intersection or the calculation is not possible, returns (None, None).
    """
    if round(player1_direction, 1) == 0:
        if round(player1_direction + math.pi, 1) == round(player2_direction, 1):
            if player1_position[0] < player2_position[0]:
                return [], True
            return [], False
        return [], True
    return None, None


def heading_same_max(player1_position:list, player1_direction:float, player2_position:list, player2_direction:float, radius:float=400):
    """
    Check if two players are heading to the same maximum.

    Parameters:
        player1_position (list): The coordinates of the first player's position. [x1, y1]
        player1_direction (float): The direction angle of the first player in radians.
        player2_position (list): The coordinates of the second player's position. [x2, y2]
        player2_direction (float): The direction angle of the second player in radians.
        radius (float): The radius within which the intersection is checked. Default is 400.

    Returns:
        tuple: A pair of the intersection coordinates and a boolean indicating if it's possible.
            If the intersection is not possible, returns ([], False).
    """
    coords = []
    parallel_info = None

    is_possible = check_distance(player1_position, player2_position, radius*0.5)
    if not is_possible:
        return coords, False

    if is_direction_vertical(player1_direction):
        player1_direction = round(player1_direction, 3)
        if is_direction_vertical(player2_direction):
            player2_direction = round(player2_direction, 3)
            if round(player1_position[0], 0) == round(player2_position[0], 0):
                coords, are_heading = check_vertical_intersection(player1_position, player1_direction, player2_position, player2_direction)
                if coords != None and are_heading != None:
                    return coords, are_heading
                coords, are_heading = check_vertical_intersection(player2_position, player2_direction, player1_position, player1_direction)
                if coords != None and are_heading != None:
                    return coords, are_heading
                return coords, True
            return coords, False

        parallel_info = calculate_parallel_info(player1_position, player1_direction, 1)

    if is_direction_vertical(player2_direction):
        parallel_info = calculate_parallel_info(player2_position, player2_direction, 2)

    if parallel_info != None:
        if parallel_info[2] == 1:
            m2 = round(math.tan(player2_direction), 3)
            linear2 = linear_creator(m2, player2_position)
            interseccion_y = linear2(parallel_info[0])

            if parallel_info[1] == math.pi/2 and interseccion_y > player1_position[1]:
                if math.cos(player2_direction) > 0 and player2_position[0] < player1_position[0]:
                    coords = [parallel_info[0], interseccion_y]
                    return calculate_coords(coords, player1_position, player2_position, parallel_info, interseccion_y, radius)
                elif player2_position[0] > player1_position[0]:
                    coords = [parallel_info[0], interseccion_y]
                    return calculate_coords(coords, player1_position, player2_position, parallel_info, interseccion_y, radius)
            elif interseccion_y < player1_position[1]:
                if math.cos(player2_direction) > 0 and player2_position[0] < player1_position[0]:
                    coords = [parallel_info[0], interseccion_y]
                    return calculate_coords(coords, player1_position, player2_position, parallel_info, interseccion_y, radius)
                elif player2_position[0] > player1_position[0]:
                    coords = [parallel_info[0], interseccion_y]
                    return calculate_coords(coords, player1_position, player2_position, parallel_info, interseccion_y, radius)
            return coords, False

        m1 = round(math.tan(player1_direction), 3)
        linear1 = linear_creator(m1, player1_position)
        interseccion_y = linear1(parallel_info[0])

        if parallel_info[1] == math.pi/2 and interseccion_y > player2_position[1]:
            if math.cos(player1_direction) > 0 and player1_position[0] < player2_position[0]:
                coords = [parallel_info[0], interseccion_y]
                return calculate_coords(coords, player1_position, player2_position, parallel_info, interseccion_y)
            elif player1_position[0] > player2_position[0]:
                coords = [parallel_info[0], interseccion_y]
                return calculate_coords(coords, player1_position, player2_position, parallel_info, interseccion_y)
        elif interseccion_y < player2_position[1]:
            if math.cos(player1_direction) > 0 and player1_position[0] < player2_position[0]:
                coords = [parallel_info[0], interseccion_y]
                return calculate_coords(coords, player1_position, player2_position, parallel_info, interseccion_y)
            elif player1_position[0] > player2_position[0]:
                coords = [parallel_info[0], interseccion_y]
                return calculate_coords(coords, player1_position, player2_position, parallel_info, interseccion_y)

        return coords, False



    # Calculate the slopes of the players' movement lines
    m1 = round(math.tan(player1_direction), 3)
    m2 = round(math.tan(player2_direction), 3)

    linear1 = linear_creator(m1, player1_position)
    linear2 = linear_creator(m2, player2_position)

    # Check if the slopes are equal (parallel lines).
    if m1 == m2 and round(player1_position[1], 0) == round(linear2(player1_position[0]), 0):
        if m1 > 0:
            coords, are_heading = check_positive_slope_intersection(player1_position, player1_direction, player2_position, player2_direction)
            if coords != None and are_heading != None:
                return coords, are_heading
            coords, are_heading = check_positive_slope_intersection(player2_position, player2_direction, player1_position, player1_direction)
            if coords != None and are_heading != None:
                return coords, are_heading
            return coords, True
        if m1 < 0:
            coords, are_heading = check_negative_slope_intersection(player1_position, player1_direction, player2_position, player2_direction)
            if coords != None and are_heading != None:
                return coords, are_heading
            coords, are_heading = check_negative_slope_intersection(player2_position, player2_direction, player1_position, player1_direction)
            if coords != None and are_heading != None:
                return coords, are_heading
            return coords, True
        if m1 == 0:
            coords, are_heading = check_zero_slope_intersection(player1_position, player1_direction, player2_position, player2_direction)
            if coords != None and are_heading != None:
                return coords, are_heading
            coords, are_heading = check_zero_slope_intersection(player2_position, player2_direction, player1_position, player1_direction)
            if coords != None and are_heading != None:
                return coords, are_heading
            return coords, True
    
    interseccion = round((-linear1(0) + linear2(0)) / (m1 - m2), 0)
    is_possible = False

    if math.cos(player1_direction) > 0:
        if math.cos(player2_direction) > 0:
            if interseccion >= player1_position[0] and interseccion >= player2_position[0]:
                coords = [interseccion, linear1(interseccion)]
        else:
            if interseccion >= player1_position[0] and interseccion <= player2_position[0]:
                coords = [interseccion, linear1(interseccion)]
    else:
        if math.cos(player2_direction) > 0:
            if interseccion <= player1_position[0] and interseccion >= player2_position[0]:
                coords = [interseccion, linear1(interseccion)]
        else:
            if interseccion <= player1_position[0] and interseccion <= player2_position[0]:
                coords = [interseccion, linear1(interseccion)]

    if coords != []:
        is_possible = check_distance(player1_position, coords, radius) and check_distance(player2_position, coords, radius)

    return coords, is_possible

