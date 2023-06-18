from dungeon2 import gen_matrix, render_map
from getch import getch
from os import system


class Mapa:
    def __init__(self, rows, columns, obstacle='█', empty='▒', p=0.1):
        self.matrix = gen_matrix(rows, columns, int(p * 100))
        self.p = p
        self.obstacle = obstacle
        self.empty = empty
        self.columns = columns
        self.rows = rows

    def get_dimensions(self):
        return self.rows, self.columns

    def get_symbol(self, x, y):
        if x < self.rows and y < self.columns:
            return self.obstacle if self.matrix[x][y] else self.empty
        else:
            return None

    def print_map(self, persona, keyboard):
        old_pos = persona.get_loc()
        pos = old_pos
        if keyboard == 'w':
            pos = (old_pos[0] - 1, old_pos[1])
        elif keyboard == 's':
            pos = (old_pos[0] + 1, old_pos[1])
        elif keyboard == 'a':
            pos = (old_pos[0], old_pos[1] - 1)
        elif keyboard == 'd':
            pos = (old_pos[0], old_pos[1] + 1)
        print(pos)
        if self.check_limits(pos) and self.is_free(pos):
            persona.set_loc(pos)
            self.matrix[pos[0]][pos[1]] = 'c'
            self.matrix[old_pos[0]][old_pos[1]] = 0
        else:
            self.matrix[old_pos[0]][old_pos[1]] = 'c'
        print(persona.get_loc())

        render_map(self.matrix, self.obstacle, self.empty, persona.get_image())


    def check_limits(self, pos):
        if 0 <= pos[0] < self.rows and 0 <= pos[1] < self.columns:
            return True
        return False

    def is_free(self, pos):
        if self.check_limits(pos):
            if self.get_symbol(pos[0], pos[1]) == self.empty:
                return True
        return False

class Creature:
    def __init__(self, initial_position, name, character='@'):
        self.pos = initial_position
        self.name = name
        self.character = character

    def set_loc(self, pos):
        self.pos = pos

    def get_loc(self):
        return self.pos

    def get_image(self):
        return self.character




def main():
    m1 = Mapa(10, 20)
    juan = Creature((0, 0), 'Juan', '@')
    user_key = ''
    system('clear')
    m1.print_map(juan, 'w')
    while user_key != 'q':
        user_key = getch()
        system('clear')
        m1.print_map(juan, user_key)

if __name__ == '__main__':
    main()
