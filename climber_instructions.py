from functools import wraps
from communication.client.client import MountainClient

""" 
PARA QUE MIS PANAS ENTIENDAN EL USO DE LOS DECORADORES: 
El decorador @staticmethod se utiliza en los métodos de clase para indicar que el método no necesita acceder a ningún atributo o método de instancia. En otras palabras, un método estático no requiere tener acceso a self (la instancia) ni a ningún otro atributo o método de la clase.

En el caso de los decoradores implementados en la clase Climbers, los métodos decorados con @staticmethod son update_direction, update_inclination y update_speed. Estos métodos están decorados de esta manera porque no necesitan acceder a los atributos de instancia (self.pos, self.speed, self.inclination), sino que actualizan directamente los valores en el diccionario directions.

Al declarar estos métodos como estáticos, indicamos que no necesitan ser invocados a través de una instancia de la clase Climbers y pueden ser llamados directamente desde la clase. Esto proporciona una forma más clara de entender que estos métodos son independientes de las instancias y se utilizan únicamente para actualizar los valores en el diccionario directions.
 
SIRVE PARA NO INSTANCIAR LAS CLASES. Y PARA NO USAR SELF. 
 """

class Climbers:
    def __init__(self, info):
        self.name = info['name']
        self.pos = info['pos']
        self.speed = 0
        self.inclination = 0

    def normalize_distance(self, v, w):
        return ((w[0] - v[0]) ** 2 + (w[1] - v[1]) ** 2) ** 0.5

    def calculate_correct_speed(self, target):
        distance = self.normalize_distance(self.pos, target)
        speed = distance / 1  # segundos (a implementar)
        return speed

    @staticmethod
    def update_direction(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            directions[self.name]['direction'] = self.pos
            return result
        return wrapper

    @staticmethod
    def update_inclination(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            directions[self.name]['inclination'] = self.inclination
            return result
        return wrapper

    @staticmethod
    def update_speed(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            directions[self.name]['speed'] = self.speed
            return result
        return wrapper

    @update_direction
    def change_pos(self, new_pos):
        self.pos = new_pos

    @update_speed
    def change_speed(self, new_speed):
        self.speed = new_speed

    @update_inclination
    def change_inclination(self, new_inclination):
        self.inclination = new_inclination

player1 = Climbers({'name': "facu", 'pos': (0, 0)})
player2 = Climbers({'name': "fran", 'pos': (0, 0)})
player3 = Climbers({'name': "ivan", 'pos': (0, 0)})
player4 = Climbers({'name': "lucas", 'pos': (0, 0)})

cliente = MountainClient()
climbers = [player1, player2, player3, player4]

directions = {}
speeds = [30, 20, 10, 4] #son las nuevas speeds dependiendo de la strat. # A IMPLEMENTAR
inclinations = [5, 12, 23, 12]
positions = [(1, 2), (3, 4), (5, 3), (6, 4)]

for index, climber in enumerate(climbers):
    speed = speeds[index]
    inclination = inclinations[index]
    direction = positions[index]

    directions[climber.name] = {'speed': speed, 'inclination': inclination, 'direction': direction}

cliente.add_team("LIFFT", [climber.name for climber in climbers])
cliente.next_iteration("LIFFT", directions)
print(cliente.finish_registration())

others_directions = {}  # Ver cómo extraer datos del servidor

#LEER - EJEMPLO DE USO

""" player1 = Climbers({'name': "facu", 'pos': (0, 0)})
player2 = Climbers({'name': "fran", 'pos': (0, 0)})

directions = {}
directions[player1.name] = {'speed': 0, 'inclination': 0, 'direction': (0, 0)}
directions[player2.name] = {'speed': 0, 'inclination': 0, 'direction': (0, 0)}

# Cambiar la posición del jugador 1 y actualizar la dirección en el diccionario
player1.change_pos((1, 2))

# Cambiar la velocidad del jugador 2 y actualizar la velocidad en el diccionario
player2.change_speed(30)
 """