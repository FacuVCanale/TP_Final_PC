from communication.client.client import MountainClient
import numpy as np
import math
import facu_inter

# Calss for hikers of our team
class Hiker:
    def __init__(self, team:str, name:str, puntos:list, strat:str="follow_points", alpha:float = 0.1, beta:float = 0.8, alpha2:float = 0.1):
        self.team = team
        self.name = name
        self.data = {}
        self.puntos = puntos
        self.strat = strat
        self.vel = 0
        self.direc = 0
        
        # Gradient ascent 
        self.alpha2 = alpha2 #learning rate
        
        # Momentum Gradient ascent
        self.vel_x = 0
        self.vel_y = 0
        self.alpha = alpha #learning rate
        self.beta = beta #momentum
    
    def update_data(self, data):
        self.data = data[self.team][self.name]

    def get_data(self, choice:str):
        return self.data[choice]
    
    def get_direction_and_vel_to_point(self, xf:float, yf:float) -> tuple[float,float]:
        """
        le das el punto donde queres ir y te da la direccion y vel para llegar mas rapido (linea recta)
        """
        xo = self.get_data('x')
        yo = self.get_data('y')

        v = (xf - xo, yf - yo)
        v_direc = math.atan2(v[1], v[0])

        if v_direc < 0:
            v_direc += 2 * math.pi
        
        vel = 50
    
        self.vel = vel
        self.direc = v_direc
        return v_direc,vel
    
    def get_direction_and_vel_to_point_JUSTO(self, xf:float, yf:float) -> tuple[float,float]:
        """
        le das el punto donde queres ir y te da la direccion y vel para llegar mas rapido (linea recta)
        llega JUSTO al punto donde se le pide
        """
        xo = self.get_data('x')
        yo = self.get_data('y')

        v = (xf - xo, yf - yo)
        v_direc = math.atan2(v[1], v[0])

        if v_direc < 0:
            v_direc += 2 * math.pi
        
        if np.linalg.norm(v) < 50:           
           vel = np.linalg.norm(v)
        else: vel = 50

        self.vel = vel
        self.direc = v_direc

        return v_direc,vel

    def get_next_point_GA(self):
        x_new = self.get_data('x') + self.get_data('inclinacion_x') * self.alpha2
        y_new = self.get_data('y') + self.get_data('inclinacion_y') * self.alpha2

        return x_new,y_new

    def get_next_point_MGA(self) -> tuple[float,float]:
        vel_x_2 = self.beta * self.vel_x + (-1) * self.get_data('inclinacion_x')
        vel_y_2 = self.beta * self.vel_y + (-1) * self.get_data('inclinacion_y')
        
        self.vel_x = vel_x_2
        self.vel_y = vel_y_2

        x_new = self.get_data('x') - vel_x_2 * self.alpha
        y_new = self.get_data('y') - vel_y_2 * self.alpha

        return x_new, y_new
    
    # ---------------- PUEDE SER GA O MGA ------------------
    def direction_GA(self):
        next_point_GA = self.get_next_point_GA()
        return self.get_direction_and_vel_to_point(next_point_GA[0], next_point_GA[1])[0]

    def speed_GA(self):
        next_point_GA = self.get_next_point_GA()
        return self.get_direction_and_vel_to_point(next_point_GA[0], next_point_GA[1])[1]
    # -------------------------------------------------------

    # ---------------- PUEDE SER GA O MGA ------------------
    def direction_MGA(self):
        next_point_MGA = self.get_next_point_MGA()
        return self.get_direction_and_vel_to_point_JUSTO(next_point_MGA[0], next_point_MGA[1])[0]

    def speed_MGA(self):
        next_point_MGA = self.get_next_point_MGA()
        return self.get_direction_and_vel_to_point_JUSTO(next_point_MGA[0], next_point_MGA[1])[1]
    # -------------------------------------------------------
   
   
    # ---------------- PUEDE SER JUSTO O NO ----------------
    def direction_p(self, point:tuple[float,float]):
        return self.get_direction_and_vel_to_point_JUSTO(point[0],point[1])[0]
    
    def speed_p(self, point:tuple[float,float]):
        return self.get_direction_and_vel_to_point_JUSTO(point[0],point[1])[1]
    # -------------------------------------------------------

    def going_same_max(self, other, self_d, other_d):
        self_pos = (self.get_data("x"), self.get_data("y"))
        other_pos = (other.get_data("x"), other.get_data("y"))
        coords, is_same = facu_inter.heading_same_max(self_pos, self_d, other_pos, other_d)
        return coords, is_same

    def strategy(self, GA_o_MGA:str ="GA", n=50, n2=0.01):
        # tolerancia econtrar punto
        # tolerancia derivada parcial
        
        # check len of list
        next_point = self.puntos[0]

        x = self.get_data('x')
        y = self.get_data('y')
        z = self.get_data('z')

        dx = self.get_data('inclinacion_x')
        dy = self.get_data('inclinacion_y')


        if self.strat == 'follow_points':
            if np.sqrt((x-next_point[0])**2 + (y-next_point[1])**2) < n:
                print(self.name, end=" ")
                print("Estoy en el punto", self.puntos.pop(0))

                self.strat = "hike"

                direction = 0
                speed = 0
            
            else:
                direction = self.direction_p(next_point)
                speed = self.speed_p(next_point)
                print(self.name, end=" ")
                print("Buscando punto", self.puntos[0])


        elif self.strat == 'hike':
            if abs(dx) < n2 and abs(dy) < n2:
                print(self.name, end=" ")
                print('Estoy en un max local')
                self.strat = 'follow_points'

                direction = 0
                speed = 0

            else:
                print(self.name, end=" ")
                print("Escalando")
                if GA_o_MGA == "GA":
                    direction = self.direction_GA()
                    speed = self.speed_GA()
                elif GA_o_MGA == "MGA":
                    direction = self.direction_MGA()
                    speed = self.speed_MGA()
                    
            

        return direction,speed
    
    def change_strat(self, strat):
        self.strat = strat

    def get_next_point(self):
        """"
        returns next point that hiker ig going to go
        """
        x_next = self.get_data('x') + self.vel*math.cos(self.direc)
        y_next = self.get_data('y') + self.vel*math.sin(self.direc)
        
        return x_next,y_next

    def check_out_of_bounds(self,radius = 23000):
        """"
        checks if hikers next point is out of bounds
        """
        next_coords = self.get_next_point()
        x_next,y_next = next_coords[0], next_coords[1]
        distance_center = math.sqrt(x_next ** 2 + y_next ** 2)
        if distance_center < radius:
            return False
        else:
            return True