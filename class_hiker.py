from communication.client.client import MountainClient
import numpy as np
import math
c = MountainClient()


# Calss for hikers of our team
class Hiker:
    def __init__(self, team:str, name:str, alpha:float = 0.01, beta:float = 0.5):
        self.team = team
        self.name = name
        self.data = {}
        
        # Gradient ascent 
        self.alpha2 = 0.1 #learning rate
        
        # Momentum Gradient ascent
        self.vel_x = 0
        self.vel_y = 0
        self.alpha = alpha #learning rate
        self.beta = beta #momentum
    
    def update_data(self):
        self.data = c.get_data()[self.team][self.name]

    def get_data(self, choice:str):
        return self.data[choice]
    
    def get_direction_and_vel_to_point(self, xf:float, yf:float)-> tuple[float,float]:
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
    
        return v_direc,vel
    
    def get_direction_and_vel_to_point_JUSTO(self, xf:float, yf:float)-> tuple[float,float]:
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

    
        return v_direc,vel

    def get_next_point_GA(self):
        x_new = self.get_data('x') + self.get_data('inclinacion_x') * self.alpha2
        y_new = self.get_data('y') + self.get_data('inclinacion_y') * self.alpha2

        return x_new,y_new

    def get_next_point_MGA(self)-> tuple[float,float]:
        vel_x_2 = self.beta * self.vel_x + (-1) * self.get_data('inclinacion_x')
        vel_y_2 = self.beta * self.vel_y + (-1) * self.get_data('inclinacion_y')
        
        self.vel_x = vel_x_2
        self.vel_y = vel_y_2

        x_new = self.get_data('x') - vel_x_2 * self.alpha
        y_new = self.get_data('y') - vel_y_2 * self.alpha

        return x_new, y_new
