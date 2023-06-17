import random
from getch import getch
import os

class Creature:
    def __init__(self, name="DEFAULT_NAME"):
        self.name = name
        self.symbol = '👾'
        self.pos = (0, 0)

    def set_loc(self, pos):
        self.pos = pos

    def get_loc(self):
        return self.pos
    
    def get_image(self):
        return self.symbol

class Mapa:
    def __init__(self, sizeX, sizeY):
        self.size = {"x": sizeX, "y": sizeY}
        self.map = [[0 for _ in range(sizeY)] for _ in range(sizeX)]
        self.obs = '+'
        self.border = '█'
        
        # Agregar borde al mapa
        for i in range(sizeX):
            self.map[i][0] = 1
            self.map[i][sizeY - 1] = 1
        for j in range(sizeY):
            self.map[0][j] = 1
            self.map[sizeX - 1][j] = 1

    def get_dims(self):
        return (self.size["x"], self.size["y"])
    
    def get_square(self, x, y, monster_loc):
        if (x, y) == monster_loc:
            return monster.get_image()
        elif self.map[x][y] == 1:
            return self.border
        else:
            return self.obs

    def render_map(self, monster: Creature = None):
        fil = self.size["x"]
        col = self.size["y"]
        M = [[self.get_square(i, j, monster.get_loc()) for j in range(col)] for i in range(fil)]
        for i in range(fil):
            print(''.join(M[i]))
    
    def check_limits(self, loc: tuple):
        return 0 <= loc[0] < self.size["x"] and 0 <= loc[1] < self.size["y"]
    
    def is_free(self, loc):
        if self.map[loc[0]][loc[1]]:
            return False
        else:
            return True
        
    def render_person(self, monster: Creature, keyboard):
        old_pos = monster.get_loc()
        if keyboard == 'w':
            new_pos = (old_pos[0] - 1, old_pos[1])
        elif keyboard == 'a':
            new_pos = (old_pos[0], old_pos[1] - 1)
        elif keyboard == 's':
            new_pos = (old_pos[0] + 1, old_pos[1])
        elif keyboard == 'd':
            new_pos = (old_pos[0], old_pos[1] + 1)
        else:
            new_pos = old_pos
        
        if self.check_limits(new_pos) and self.is_free(new_pos):
            monster.set_loc(new_pos)
        
        self.render_map(monster)

mi_mapa = Mapa(16, 26)
monster = Creature()
monster.set_loc((10, 5))
mi_mapa.render_map(monster)

key = ""
while key != "q":
    key = getch()
    os.system("clear")
    mi_mapa.render_person(monster, key)
