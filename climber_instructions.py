import time
import random
from communication.client.client import MountainClient

""" 
PARA QUE MIS PANAS ENTIENDAN EL USO DE LOS DECORADORES: 
El decorador @staticmethod se utiliza en los métodos de clase para indicar que el método no necesita acceder a ningún atributo o método de instancia. En otras palabras, un método estático no requiere tener acceso a self (la instancia) ni a ningún otro atributo o método de la clase.

En el caso de los decoradores implementados en la clase Climbers, los métodos decorados con @staticmethod son update_direction, update_inclination y update_speed. Estos métodos están decorados de esta manera porque no necesitan acceder a los atributos de instancia (self.pos, self.speed, self.inclination), sino que actualizan directamente los valores en el diccionario directions.

Al declarar estos métodos como estáticos, indicamos que no necesitan ser invocados a través de una instancia de la clase Climbers y pueden ser llamados directamente desde la clase. Esto proporciona una forma más clara de entender que estos métodos son independientes de las instancias y se utilizan únicamente para actualizar los valores en el diccionario directions.
 
SIRVE PARA NO INSTANCIAR LAS CLASES. Y PARA NO USAR SELF. 
 """

from communication.client.client import MountainClient

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




    def change_pos(self, new_pos):
        self.pos = new_pos

    def change_speed(self, new_speed):
        self.speed = new_speed

    def change_inclination(self, new_inclination):
        self.inclination = new_inclination

player1 = Climbers({'name': "facu", 'pos': (1, 1)})


cliente = MountainClient()
climbers = [player1]


cliente.add_team("LIFFT", [climber.name for climber in climbers])
#{'LIFFT': {'facu': {'x': 14000, 'y': 14000, 'z': -14109979074.0, 'inclinacion_x': -503966.0, 'inclinacion_y': -503962.0, 'cima': False}


directions = {}


directions[player1.name] = {'speed': 10, 'inclination': 0, 'direction': 45}

print(cliente.finish_registration())
coord_set = set()  # Conjunto para realizar un seguimiento de las coordenadas únicas

while not cliente.is_over():
    time.sleep(5)
    cliente.next_iteration("LIFFT", directions)
    info = cliente.get_data()

    with open('coordenadas.txt', 'a') as file:
        for team in info.values():
            for climber in team.values():
                x = climber['x']
                y = climber['y']
                z = climber['z']
                coord = (x, y, z)
                if coord not in coord_set:
                    line = f"{x} {y} {z}\n"
                    file.write(line)
                    coord_set.add(coord)

    directions[player1.name]['direction'] += random.choice([i for i in range(120)])
    
    print(directions[player1.name]['direction'])
    print(info)




#LEER - EJEMPLO DE USO

""" player1 = Climbers({'name': "facu", 'pos': (0, 0)})
player2 = Climbers({'name': "fran", 'pos': (0, 0)})



# Cambiar la posición del jugador 1 y actualizar la dirección en el diccionario
player1.change_pos((1, 2),'pos')

# Cambiar la velocidad del jugador 2 y actualizar la velocidad en el diccionario
player2.change_speed(30,'speed')
 """