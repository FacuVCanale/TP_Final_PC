
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



