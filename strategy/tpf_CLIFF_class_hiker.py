import numpy as np
import strategy.tpf_CLIFF_intersection as intersection

class Hiker:
    """
    Class for hikers of our team
    """
    def __init__(self, team:str, name:str, points:list, strat:str="follow_points", alpha:float = 0.1, beta:float = 0.8, alpha2:float = 0.1) -> None:
        """
        Initializes an instance of the class with the specified parameters.

        Parameters
        ----------
        team : str
            The team name.
        name : str
            The name of the instance.
        points : list
            The list of points.
        strat : str, optional
            The strategy (default: "follow_points").
        alpha : float, optional
            The learning rate for gradient ascent (default: 0.1).
        beta : float, optional
            The momentum for gradient ascent (default: 0.8).
        alpha2 : float, optional
            The learning rate for gradient ascent (default: 0.1).
        """

        # Hiker team and name
        self.team = team
        self.name = name

        # Hiker data from this iteration and the previous one
        self.last_data = {"x": 14000, "y":14000, "z": 0, "inclinacion_x": 0, "inclinacion_y": 0}
        self.data = {"x": 14000, "y":14000, "z": 0, "inclinacion_x": 0, "inclinacion_y": 0}
        self.vel = 0
        self.direc = 0
        self.last_direc = 0

        # Initializes variables for the strategies:
        self.oscilando = False
        self.points = points
        self.strat = strat
        self.counter = 0
        
        # Gradient Ascent and Descent alpha (learning rate)
        self.alpha2 = alpha2
        
        # Momentum Gradient Ascent and Descent alpha and beta (learning rate and momentum multiplier)
        self.alpha = alpha
        self.beta = beta

        # Initializes accumulated momentum of Momentum Gradient Ascent
        self.vel_x = 0 
        self.vel_y = 0

        # Initializes accumulated momentum of Momentum Gradient Descent
        self.vel_x_down = 0
        self.vel_y_down = 0
    
    def update_data(self, data:dict[str, float]) -> None:
        """
        Updates data of hiker and saves it on attribute self.data

        Parameters
        ----------
        data : function
            function that returns data

        Returns
        -------
        None
        """
        if data != self.data:
            self.last_data = self.data
            self.data = data[self.team][self.name]

    def __getitem__(self, choice: str) -> float:
        """
        Returns a specific hiker data.

        Parameters
        ----------
        choice : str
            Type of data that is going to be returned.

        Returns
        -------
        float
            Specific data.
        """
        return self.data[choice]

    def get_direction_and_vel_to_point_fixed(self, xf: float, yf: float) -> tuple[float, float]:
        """
        Calculates the direction and velocity required to reach a fixed point (+- 50).

        Parameters
        ----------
        xf : float
            The x-coordinate of the point.
        yf : float
            The y-coordinate of the point.

        Returns
        -------
        tuple[float, float]
            A tuple containing the direction and velocity to reach the next point.
        """
        xo = self["x"]
        yo = self["y"]

        v = (xf - xo, yf - yo)
        v_direc = np.arctan2(v[1], v[0])

        vel = 50

        self.last_direc = self.direc

        self.vel = vel
        self.direc = v_direc
        return v_direc, vel

    
    def get_direction_and_vel_to_point_JUSTO(self, xf:float, yf:float) -> tuple[float,float]:
        """
        Receives the x, y coordinates of a point and returns the direction and velocity to get to that point exactly.
        vel is not always 50 because if the distance is less that 50, vel is going to be exact to get to
        the point

        Parameters
        ----------
        xf : float
            x coord of point
        xy : float
            y coord of point

        Returns
        -------
        tuple
            tuple with direction and vel to get to next point
        """
        xo = self["x"]
        yo = self["y"]
        v = (xf - xo, yf - yo)
        v_direc = np.arctan2(v[1], v[0])

        if v_direc < 0:
            v_direc += 2 * np.pi
        
        if np.linalg.norm(v) < 50:           
           vel = np.linalg.norm(v)
        else: vel = 50

        self.last_direc = self.direc

        self.vel = vel
        self.direc = v_direc

        return v_direc, vel

    def get_next_point_GA(self)-> tuple[float,float]:
        """
        Using data on hiker attributes gets the next position to climb mountain 
        with gradient ASCENT method

        Returns
        -------
        tuple
            tuple with x coord and y coord of next point to climb mountain
        """
        x_new = self["x"] + self["inclinacion_x"] * self.alpha2
        y_new = self["y"] + self["inclinacion_y"] * self.alpha2

        return x_new,y_new
    
    def get_next_point_GD(self)-> tuple[float,float]:
        """
        Using data on hiker attributes gets the next position to climb mountain 
        with gradient DECENT method

        Returns
        -------
        tuple
            tuple with x coord and y coord of next point to climb mountain
        """
        x_new = self["x"]- self["inclinacion_x"] * self.alpha2
        y_new = self["y"] - self["inclinacion_y"] * self.alpha2

        return x_new, y_new
    
    def direction_GD(self)-> float:
        """
        Faster way to call a function that returns direction to climb mountain 
        using Gradient DECENT

        Returns
        -------
        float
            direction
        """
        next_point_GD = self.get_next_point_GD()
        return self.get_direction_and_vel_to_point_fixed(next_point_GD[0], next_point_GD[1])[0]
    
    def speed_GD(self)-> float:
        """
        Faster way to call a function that returns speed to climb mountain 
        using Gradient DECENT
        Returns
        -------
        float
            speed
        """
        next_point_GD = self.get_next_point_GD()
        return self.get_direction_and_vel_to_point_fixed(next_point_GD[0], next_point_GD[1])[1]

    def get_next_point_MGA(self) -> tuple[float,float]:
        """
        Using data on hiker attributes gets the next position to climb mountain 
        with momentum gradient ASCENT method

        Returns
        -------
        tuple
            tuple with x coord and y coord of next point to climb mountain
        """

        dxdy_v = np.array([self["inclinacion_x"], self["inclinacion_y"]])

        dxdy_v = (dxdy_v * 25 * np.sqrt(2))/ np.linalg.norm(dxdy_v) 

        vel_x_2 = self.beta * self.vel_x + (-1) * dxdy_v[0]
        vel_y_2 = self.beta * self.vel_y + (-1) * dxdy_v[1] 
        
        self.vel_x = vel_x_2
        self.vel_y = vel_y_2

        x_new = self["x"] - vel_x_2 * self.alpha
        y_new = self["y"] - vel_y_2 * self.alpha

        return x_new, y_new
    
    def get_next_point_MGD(self) -> tuple[float,float]:
        """
        Using data on hiker attributes gets the next position to climb mountain 
        with momentum gradient DECENT method

        Returns
        -------
        tuple
            tuple with x coord and y coord of next point to climb mountain
        """
        vel_x_2_down = self.beta * self.vel_x_down + self["inclinacion_x"]
        vel_y_2_down = self.beta * self.vel_y_down + self["inclinacion_y"]
        
        self.vel_x_down = vel_x_2_down
        self.vel_y_down = vel_y_2_down

        x_new = self["x"] + vel_x_2_down * self.alpha
        y_new = self["y"] + vel_y_2_down * self.alpha

        return x_new, y_new

    def direction_MGD(self)-> float:
        """
        Faster way to call a function that returns direction to climb mountain 
        using Momentum Gradient DECENT
        Returns
        -------
        float
            direction
        """
        next_point_MGD = self.get_next_point_MGD()
        return self.get_direction_and_vel_to_point_JUSTO(next_point_MGD[0], next_point_MGD[1])[0]

    def speed_MGD(self)-> float:
        """
        Faster way to call a function that returns direction to climb mountain 
        using Momentum Gradient DECENT
        Returns
        -------
        float
            speed
        """
        next_point_MGD = self.get_next_point_MGD()
        return self.get_direction_and_vel_to_point_JUSTO(next_point_MGD[0], next_point_MGD[1])[1]
    

    def direction_GA(self)-> float:
        """
        Faster way to call a function that returns direction to climb mountain 
        using Gradient ASENT

        Returns
        -------
        float
            direction
        """
        next_point_GA = self.get_next_point_GA()
        return self.get_direction_and_vel_to_point_fixed(next_point_GA[0], next_point_GA[1])[0]

    def speed_GA(self)-> float:
        """
        Faster way to call a function that returns speed to climb mountain 
        using Gradient ASENT
        Returns
        -------
        float
            speed
        """
        next_point_GA = self.get_next_point_GA()
        return self.get_direction_and_vel_to_point_fixed(next_point_GA[0], next_point_GA[1])[1]

    def direction_MGA(self)-> float:
        """
        Faster way to call a function that returns direction to climb mountain 
        using Momentum Gradient ASENT
        Returns
        -------
        float
            direction
        """
        next_point_MGA = self.get_next_point_MGA()
        return self.get_direction_and_vel_to_point_JUSTO(next_point_MGA[0], next_point_MGA[1])[0]

    def speed_MGA(self)-> float:
        """
        Faster way to call a function that returns direction to climb mountain 
        using Momentum Gradient ASENT
        Returns
        -------
        float
            speed
        """
        next_point_MGA = self.get_next_point_MGA()
        return self.get_direction_and_vel_to_point_JUSTO(next_point_MGA[0], next_point_MGA[1])[1]

    def direction_p(self, point:tuple[float,float])->float:
        """
        Faster way to call a function that returns direction to go to a point EXACTLY
        
        Parameters
        ----------
        Point : tuple
            x and y coord of point       
        Returns
        -------
        float
            direction
        """
        return self.get_direction_and_vel_to_point_JUSTO(point[0],point[1])[0]
    
    def speed_p(self, point:tuple[float,float])->float:
        """
        Faster way to call a function that returns speed to go to a point EXACTLY
        
        Parameters
        ----------
        Point : tuple
            x and y coord of point       
        Returns
        -------
        float
            speed
        """
        return self.get_direction_and_vel_to_point_JUSTO(point[0],point[1])[1]

    def going_same_max(self, other:object, self_d:float, other_d:float)->tuple[list,bool]:
        self_pos = (self["x"], self["y"])
        other_pos = (other["x"], other["y"])
        print(self_pos, self_d, other_pos, other_d)
        coords, is_same = intersection.heading_same_max(self_pos, self_d, other_pos, other_d)
        return coords, is_same

    def strategy(self, local_maxs:list, G_o_MG:str ="G", n=50, n2=0.001)-> tuple[float,float]:
        """
        Strategy to find global max. 

        1 First go to next point in a list of points
        2 Then  climb to find a global or local max.
        3 If a local max was found (not win)- Repeat process

        Parameters
        ----------
        local_maxs : list
            x
        G_o_MG : str
            choice strat for climbion mountain, momengum GA or GA
        n : float
            radius of tolerance for being on a certain point
            (usually similar to visual radius)

        Returns
        -------
        tuple
            tuple with next direction and speed hiker has to go to follow strategy
        """
        
        x = self["x"]
        y = self["y"]

        if self.strat == 'follow_points':
            if len(self.points) == 0:
                print("No hay más puntos!")
                self.strat = "descent"
                self.counter = 0
                return self.strategy(local_maxs)
            
            next_point = self.points[0]
            
            if np.sqrt((x-next_point[0])**2 + (y-next_point[1])**2) < n:
                print(self.name, end=" ")
                print("Estoy en el punto", self.points.pop(0))

                self.counter = 0

                self.strat = "hike"

                direction = 0
                speed = 0
            
            else:
                direction = self.direction_p(next_point)
                speed = self.speed_p(next_point)
                print(self.name, end=" ")
                print("Buscando punto", self.points[0])
            
            self.counter += 1

        elif self.strat == 'hike':
            
            if self.counter > 2:
                if self.has_stept_extremum() is True:
                    if self.oscilando is False:
                        self.oscilando = True
                    else:
                        print(self.name, end=" ")
                        print('Estuve oscilando en un max local')

                        point = self.aproximate_local()
                        local_maxs.append(point)

                        self.strat = "descent"
                        self.vel_x, self.vel_y = 0, 0

                        self.counter = 0
                        direction = self.last_direc
                        speed = 50
                        return direction, speed
                
            self.counter += 1
            print(self.name, end=" ")
            print("Escalando")
            if G_o_MG == "G":
                direction = self.direction_GA()
                speed = self.speed_GA()
            elif G_o_MG == "MG":
                direction = self.direction_MGA()
                speed = self.speed_MGA()
        
        elif self.strat == "descent":
            if self.counter > 2:
                if self.has_stept_extremum():
                    if self.oscilando is False:
                        self.oscilando = True
                    else:
                        print(self.name, end=" ")
                        print('Estoy en un min local')
                        self.strat = 'hike'

                        self.counter = 0

                        self.vel_x_down, self.vel_y_down = 0, 0

                        direction = self.last_direc

                        speed = 50
                        return direction, speed

            self.counter += 1
            print(self.name, end=" ")
            print("Bajando")
            if G_o_MG == "G":
                direction = self.direction_GD()
                speed = self.speed_GD()
            elif G_o_MG == "MG":
                direction = self.direction_MGD()
                speed = self.speed_MGD()

        return direction, speed
    
    def change_strat(self, strat:str) -> None:
        """
        Changes hiker strat

        Parameters
        ----------
        strat : str
            type of strat

        Returns
        -------
        None
        """
        self.strat = strat

    def get_next_point(self) -> tuple[float,float]:
        """
        Using data on hiker attributes predicts the next position hiker is going to be in

        Returns
        -------
        tuple
            tuple with x coord and y coord of next point
        """
        x_next = self["x"] + self.vel*np.cos(self.direc)
        y_next = self["y"] + self.vel*np.sin(self.direc)
        
        return x_next,y_next

    def check_out_of_bounds(self, radius = 23000) -> bool:
        """
        Checks if hiker next position is going to bo out of bounds of a circle with
        radius = radius and center in (0,0)

        Parameters
        ----------
        radius : float
            radius of the circle

        Returns
        -------
        bool
            True if out of bounds False if not
        """
        next_coords = self.get_next_point()
        x_next,y_next = next_coords[0], next_coords[1]
        distance_center = np.sqrt(x_next ** 2 + y_next ** 2)
        if distance_center < radius:
            return False
        else:
            return True
        
    def is_near_point(self, point) -> bool:
        """
        Check if the current position is near a given point.

        Parameters
        ----------
        point : tuple
            The coordinates of the point to check.

        Returns
        -------
        bool
            True if the current position is within a distance of 100 units from the given point, False otherwise.
        """
        self_pos = (self["x"], self["y"])
        is_near = intersection.check_distance(self_pos, point, 100)
        return is_near

    def has_stept_extremum(self) -> bool:
        """
        Check if the instance has made a step into an extremum.

        Returns
        -------
        bool
            True if the strategy is "descent" and the current altitude is lower than the previous altitude,
            or if the strategy is "hike" and the current altitude is higher than the previous altitude.
            False otherwise.
        """
        if self.strat == "descent" and self.last_data["z"] < self["z"]:
            return True
        elif self.strat == "hike" and self.last_data["z"] > self["z"]:
            return True
        return False


    def aproximate_local(self) -> tuple:
        """
        Approximate the coordinates of a local_maximum.

        Returns
        -------
        tuple
            A tuple containing the average x and y coordinates between the current and previous positions.
        """
        if self.has_stept_extremum() is True:
            return ((self.last_data["x"] + self["x"]) / 2, (self.last_data["y"] + self["y"]) / 2)
