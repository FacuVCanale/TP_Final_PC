from communication.client.client import MountainClient
# c = MountainClient()

# Calss to analize data on all hykers on map
class DataAnalyst:
    def __init__(self, cliente, name:str = 'dataAnalyst'):
        self.c = cliente
        self.name = name
        self.data = {}
        self.all_h_pos = []
        self.someone_won = False
        self.info = {}

    def update_data(self):
        """
        updates data using MountainClient()
        """
        self.data = self.c.get_data()
    
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

