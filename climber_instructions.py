
from communication.client.client import MountainClient

#La posicion del climber esta dada por una tupla (x,y). La inclinacion esta dada por un float, y la speed tambien. Cuando tenga que pasarle la posicion, lo hago en fomrato de (x,y)


class Climbers:
    def __init__(self, info):
        self.name = info['name']
        self.pos = info['pos']
        

    def change_pos(self, new_pos):
        self.pos = new_pos

player1 = Climbers({'name': "facu", 'pos': (0, 0)})
player2 = Climbers({'name': "fran", 'pos': (0, 0)})
player3 = Climbers({'name': "ivan", 'pos': (0, 0)})
player4 = Climbers({'name': "lucas", 'pos': (0, 0)})

cliente = MountainClient()
climbers = [player1, player2, player3, player4]


directions = {}

speeds = [30, 20, 10, 4] #son las nuevas speeds dependiendo de la strar. # A IMPLEMENTAR
inclinations = [5, 12, 23, 12]
positions = [(1, 2), (3, 4), (5, 3), (6, 4)]

for index, climber in enumerate(climbers): #Idea de como cambiar la info de cada climber (dependiendo la strat) -# A IMPLEMENTAR
    speed = speeds[index]
    inclination = inclinations[index]
    direction = positions[index]

    directions[climber] = {'speed': speed, 'inclination': inclination, 'direction': direction}

def normalize_distance(v, w):
    return ((w[0] - v[0]) ** 2 + (w[1] - v[1]) ** 2) ** 0.5 #Idea para calcular la distancia entre dos puntos

def calculate_correct_speed(target, current_pos, climber): #idea para calcular la velocidad que se debe ir para llegar a dicho punto lo mas rapido posible. La idea del parametro climber es que se sepa de que climber hablamos. PONERLO COMO ATRIBUTO? quizas deco...
    distance = normalize_distance(current_pos, target)
    speed = distance / 1  # segundos (a implementar)
    return speed

def change_speed(player):
    # new_speed = calculate_correct_speed(new_pos, player.pos, player) #CLARAMENTE MANDARLO A ATRIBTUOS DE LA CLASE.
    # directions[player]['speed'] = new_speed
    pass

def change_direction(player): #LO MISMO
    pass

def change_inclination(player): #Lo mismo
    pass

cliente.add_team("LIFFT", climbers)
cliente.next_iteration("LIFFT", directions)
print(cliente.finish_registration())

others_directions = {}  # Ver cómo extraer datos del servidor
