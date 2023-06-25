from communication.client.client import MountainClient
import time
import random
import numpy as np
import math
c = MountainClient()

class DataAnalyst:
    def __init__(self, name:str):
        self.name = name
        self.data = {}
        self.all_h_pos = []
        self.someone_won = False

    def update_data(self):
        self.data = c.get_data()
    
    def check_win(self):
        """
        Se fija si algun Hiker gano
        """
        for team in self.data:
            for player in self.data[team]:
                if self.data[team][player]['cima'] == True:
                    self.someone_won = True
                    print('ALGUIEN GANO')
                    # ----------HACER QUE NUESTROS HIKERS VAYAN AL PUNTO---------------

    def get_all_pos(self):
        """
        Guarda las pos de todos los hikers en una lista de tuplas con x y z de cada uno
        """
        for team in self.data:
            for player in self.data[team]:
                self.all_h_pos.append((self.data[team][player]['x'],self.data[team][player]['y'],self.data[team][player]['z']))

    def get_max(self):
        """
        rotorna la max pos en z encontrada por cualquier hiker en una tupla de (x,y,zMAX)
        """
        self.get_all_pos()
        self.all_h_pos = sorted(self.all_h_pos, key=lambda z: z[2])
        max_xyz = self.all_h_pos.pop()
        print("MAX LIST=",max_xyz)

        # achicar la lista de todas las pos para solo tener las 100 max
        self.all_h_pos[-100:]


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
        print(self.data)

    def get_data(self, d):
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
        
        #if np.linalg.norm(v) < 50:                      NO CONVIENE BAJARLE LA VELOCIDAD
        #    vel = np.linalg.norm(v)
        #else: vel = 50

        vel = 50
    
        return v_direc,vel

    def get_next_point_GA(self):
        x_new = self.get_data('x') + self.get_data('inclinacion_x') * self.alpha2
        y_new = self.get_data('y') + self.get_data('inclinacion_y') * self.alpha2

        return x_new,y_new

    def get_next_point_MGA(self):
        vel_x_2 = self.beta * self.vel_x + (-1) * self.get_data('inclinacion_x')
        vel_y_2 = self.beta * self.vel_y + (-1) * self.get_data('inclinacion_y')
        
        self.vel_x = vel_x_2
        self.vel_y = vel_y_2

        x_new = self.get_data('x') - vel_x_2 * self.alpha
        y_new = self.get_data('y') - vel_y_2 * self.alpha

        return x_new, y_new

def update_all_data(hikers:list[Hiker]):
    for hiker in hikers:
        hiker.update_data()

#       REFERENCE POINTS

point_lucas = [-5000, 18750]
point_facu = [-19702, -1955]
point_fran = [-1955, -19702]
point_ivan = [18750, -5000]

lucas = Hiker('CLIFF','lucas')  
facu = Hiker('CLIFF','facu')
fran = Hiker('CLIFF','fran')
ivan = Hiker('CLIFF','ivan')
dataAnalyst = DataAnalyst('dataAnalyst')

c.add_team('CLIFF', [lucas.name,facu.name,fran.name,ivan.name])
c.finish_registration()

hikers = [lucas, facu, fran, ivan]

while not c.is_over():
    time.sleep(2)
    data = c.get_data()
    update_all_data(hikers)
    dataAnalyst.get_max()
    dataAnalyst.check_win()

    lucas_vel_points = lucas.get_direction_and_vel_to_point(point_lucas[0], point_lucas[1])
    facu_vel_points = facu.get_direction_and_vel_to_point(point_facu[0], point_facu[1])
    fran_vel_points = fran.get_direction_and_vel_to_point(point_fran[0], point_fran[1])

    ivan_points_GA = ivan.get_next_point_GA()
    ivan_direction, ivan_speed = ivan.get_direction_and_vel_to_point(ivan_points_GA[0], ivan_points_GA[1])

    directives = {
                    lucas.name: {'direction': lucas_vel_points[0], 'speed': lucas_vel_points[1]},
                    facu.name: {'direction': facu_vel_points[0], 'speed': facu_vel_points[1]},
                    fran.name: {'direction': fran_vel_points[0], 'speed': fran_vel_points[1]},
                    ivan.name: {'direction': ivan_direction, 'speed': ivan_speed},
                }

    c.next_iteration('CLIFF', directives)
