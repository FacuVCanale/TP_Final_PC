from dungeon import gen_matrix, render_map

class Mapa():
    def __init__(self, fil, col, c_obs, c_libr, p = 20):
        self.fila = fil
        self.col = col
        self.c_obs = c_obs
        self.c_libr = c_libr
        self.p = p
        self.matriz = gen_matrix(self.fila, self.col, self.p)

    def get_dims(self):
        return (self.fila, self.col)
    
    def symb_coord(self, coords):
        val = self.matriz[coords[0]][coords[1]]
        if val:
            return self.c_obs
        else:
            return self.c_libr 
    
    def print_map(self, persona, keyboard):
        assert keyboard in ['w','a','s','d'], 'Las direcciones posibles son "w" (arriba), "s" (abajo), "a" (izquierda) y "d" (derecha)'
        pos_vieja = persona.get_loc()
        if keyboard == 'w':
            pos = (pos_vieja[0]-1,pos_vieja[1])
        elif keyboard == 's':
            pos = (pos_vieja[0]+1,pos_vieja[1])
        elif keyboard == 'a':
            pos = (pos_vieja[0],pos_vieja[1]-1)
        else:
            pos = (pos_vieja[0],pos_vieja[1]+1)
        self.matriz[pos_vieja[0]][pos_vieja[1]] = persona.car_p
        if self.check_lim(pos) and self.is_free(pos) and pos[0] >= 0 and pos[1] >= 0:
            self.matriz[pos[0]][pos[1]] = persona.car_p
            self.matriz[pos_vieja[0]][pos_vieja[1]] = 0
        render_map(self.matriz, self.c_obs, self.c_libr, persona.car_p)


    def check_lim(self, loc):
        if loc[0] < self.fila and loc[1] < self.col:
            return True
        else:
            return False
    
    def is_free(self, loc):
        if self.matriz[loc[0]][loc[1]] == 0 and self.check_lim(loc):
            return True
        else:
            return False



class Creature:
    
    def __init__(self, nombre, car_p, loc):
        self.name = nombre
        self.car_p = car_p
        self.loc = loc

    def set_loc(self, loc_n):
        self.loc = loc_n
    def get_loc(self):
        return self.loc
    def get_image(self):
        return self.car_p

if __name__ == '__main__':
    fil = 50
    col = 60
    p = 10
    mat = Mapa(fil,col,'██','▒▒',p)
    dims = mat.get_dims()
    symb_c = mat.symb_coord((0,0))
    c = Creature('pepe', '\U0001F603', (3,4))
    c.set_loc((0,0))
    mat.print_map(c,'a')
    matriz = mat.matriz
