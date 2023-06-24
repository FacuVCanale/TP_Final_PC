from communication.client.client import MountainClient
import time
import numpy as np
import math
c = MountainClient()

# Calss to analize data on all hykers on map
class DataAnalyst:
    def __init__(self, name:str = 'dataAnalyst'):
        self.name = name
        self.data = {}
        self.all_h_pos = []
        self.someone_won = False
        self.info = {}

    def update_data(self):
        """
        updates data using MountainClient()
        """
        self.data = c.get_data()
    
    def check_win(self)-> tuple[bool,tuple[float,float,float]]:
        """
        Se fija si algun Hiker gano
        """
        for team in self.data:
            for player in self.data[team]:
                if self.data[team][player]['cima'] == True:
                    self.someone_won = True
                    return True, self.get_max()
                    # ----------HACER QUE NUESTROS HIKERS VAYAN AL PUNTO---------------
        return False, None
    
    def get_all_pos(self):
        """
        Guarda las pos de todos los hikers en una lista de tuplas con x y z de cada uno
        """
        for team in self.data:
            for player in self.data[team]:
                self.all_h_pos.append((self.data[team][player]['x'],self.data[team][player]['y'],self.data[team][player]['z']))

    def get_max(self)-> tuple[float,float,float]:
        """
        rotorna la max pos en z encontrada por cualquier hiker en una tupla de (x,y,zMAX)
        """
        self.get_all_pos()
        self.all_h_pos = sorted(self.all_h_pos, key=lambda z: z[2])
        max_xyz = self.all_h_pos.pop()
        
        # achicar la lista de todas las pos para solo tener las n max
        n = 5
        self.all_h_pos = self.all_h_pos[-n:]

        return max_xyz
    
    def get_all_info(self)-> dict[bool,tuple,list]:
        self.info = {'win': self.check_win(), 'max_pos': self.get_max(), 'n_max_pos': self.all_h_pos}
        return self.info


# Calss for hikers of our team
class Hiker:
    def __init__(self, team:str, name:str):
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

        vel = 50
    
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
    
# Initialize DataAnalyst
dataAnalyst = DataAnalyst()
dataAnalysts = [dataAnalyst]


# Initialize hikers
lucas = Hiker('CLIFF','lucas')  
facu = Hiker('CLIFF','facu')
fran = Hiker('CLIFF','fran')
ivan = Hiker('CLIFF','ivan')
hikers = [lucas, facu, fran, ivan]


# Function to update data on all Hykers and DataAnalyst
def update_all_data(hikers:list[Hiker],dataAnalysts:list[DataAnalyst]):
    for hiker in hikers:
        hiker.update_data()
    for dataAnalyst in dataAnalysts:
        dataAnalyst.update_data()
    

# Add and register team
hikers_names = [hiker.name for hiker in hikers]
c.add_team('CLIFF', hikers_names)
c.finish_registration()


# Iterations
while not c.is_over():
    # Sleep server for testing
    time.sleep(3)

    # Ask for data of all hikers in map
    data = c.get_data()
    print("\n Server Info = ",data)

    # Update data of our hykers
    update_all_data(hikers,dataAnalysts)

    # Print usefull data of DataAnalyst
    dataAnalyst_info = dataAnalyst.get_all_info()
    print("\n DataAnalyst Info = ", dataAnalyst_info)
  

    # ------------------Codigo de prueba------------------

    ivan_points_GA = ivan.get_next_point_GA()
    ivan_direction, ivan_speed = ivan.get_direction_and_vel_to_point_JUSTO(ivan_points_GA[0], ivan_points_GA[1])

    fran_points_GA = fran.get_next_point_GA()
    fran_direction, fran_speed = fran.get_direction_and_vel_to_point(fran_points_GA[0], fran_points_GA[1])

    directives = {
                    lucas.name: {'direction': lucas.get_direction_and_vel_to_point_JUSTO(100,100)[0], 'speed': lucas.get_direction_and_vel_to_point_JUSTO(100,100)[1]},
                    facu.name: {'direction': facu.get_direction_and_vel_to_point_JUSTO(100,100)[0], 'speed': facu.get_direction_and_vel_to_point_JUSTO(100,100)[1]},
                    fran.name: {'direction': fran_direction, 'speed': fran_speed},
                    ivan.name: {'direction': ivan_direction, 'speed': ivan_speed},
                }
    
    # ------------------Codigo de prueba------------------

    # Give directives to server
    c.next_iteration('CLIFF', directives)

