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

    direction, speed = ivan.get_direction_and_vel_to_point(-1000,-1000)
    directives = {
                    ivan.name: {'direction': direction, 'speed': speed},
                }

    c.next_iteration('CLIFF', directives)
