from communication.client.client import MountainClient
import time
import random
import numpy as np
import math
c = MountainClient()

class Hiker:
    def __init__(self, team, name:str):
        self.team = team
        self.name = name
        self.data = {}
        
        # Gradient ascent 
        self.alpha2 = 0.1 #learning ratev
        
        # Momentum Gradient ascent
        self.vel_x = 0
        self.vel_y = 0
        self.alpha = 0.01 #learning rate
        self.beta = 0.5 #momentum
    
    def update_data(self):
        # print(self.data)
        self.data = c.get_data()[self.team][self.name]

    def get_data(self,d):
        return self.data[d]
    
    def get_direction_and_vel_to_point(self, xf, yf):
        """
        le das el punto donde queres ir y te da la direccion y vel para llegar mas rapido (linea recta)
        llega justo al punto donde se le pide
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
        x_new = self.get_data('x')+ self.get_data('inclinacion_x') * self.alpha2
        y_new = self.get_data('y')+ self.get_data('inclinacion_y') * self.alpha2

        return x_new,y_new

    def get_next_point_MGA(self):
        vel_x_2 = self.beta * self.vel_x + self.alpha * self.get_data('inclinacion_x')
        vel_y_2 = self.beta * self.vel_y + self.alpha * self.get_data('inclinacion_y')
        
        self.vel_x = vel_x_2
        self.vel_y = vel_y_2

        x_new = self.get_data('x') + vel_x_2
        y_new = self.get_data('y') + vel_y_2

        return x_new,y_new
    

def update_all_data():
    ivan.update_data()

ivan = Hiker('CLIFF','ivan')

c.add_team('CLIFF', [ivan.name])
c.finish_registration()

while not c.is_over():
    time.sleep(0.3)
    data = c.get_data()
    print("DATA: ",data)
    update_all_data()

    # direction, speed = ivan.get_direction_and_vel_to_point(ivan.get_next_point_MGA()[0],ivan.get_next_point_MGA()[1])
    ivan_direction, ivan_speed = ivan.get_direction_and_vel_to_point(ivan.get_next_point_GA()[0],ivan.get_next_point_GA()[1])
    directives = {
                    ivan.name: {'direction': ivan_direction, 'speed': ivan_speed},
                }

    c.next_iteration('CLIFF', directives)
