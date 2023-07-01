"""DO NOT MODIFY THIS FILE"""

from communication.server.mountain.abstract.mountain import Mountain
import math
import random

class CircularBaseMountain(Mountain):
    """STUDENTS: DO NOT USE THIS CLASS"""

    def __init__(self, function, df, flag, visual_radius, base_radius, x_range, y_range) -> None:
        self.base_radius = base_radius
        self.x_range = x_range
        self.y_range = y_range
        flag = self._unmap_xy(flag[0], flag[1])
        max_rotation = (2) * math.pi
        self.rotation = random.random() * max_rotation
        while self.is_out_of_bounds(*self.rotate_coordinates(flag[0], flag[1], 14000, 14000, self.rotation)):
            self.rotation = random.random() * max_rotation
        flag = self.rotate_coordinates(flag[0], flag[1], 14000, 14000, self.rotation)
        super().__init__(function, df, flag, visual_radius)
        
    def _unmap_xy(self, x, y):
        x = x - (self.x_range[1] + self.x_range[0]) / 2 # (-x_range/2, x_range/2)
        x = x / ((self.x_range[1] - self.x_range[0]) / 2) # (-1, 1)
        x = x * self.base_radius # (-base_radius, base_radius)

        y = y - (self.y_range[1] + self.y_range[0]) / 2
        y = y / ((self.y_range[1] - self.y_range[0]) / 2)
        y = y * self.base_radius

        return x, y

    def _map_xy(self, x, y):
        x, y = self.rotate_coordinates(x, y, 14000, 14000, -self.rotation)
        
        x = x / self.base_radius # (-1, 1)
        x = x * (self.x_range[1] - self.x_range[0]) / 2 # (-x_range/2, x_range/2)
        x = x + (self.x_range[1] + self.x_range[0]) / 2 # (x_range[0], x_range[1])
        
        y = y / self.base_radius
        y = y * (self.y_range[1] - self.y_range[0]) / 2
        y = y + (self.y_range[1] + self.y_range[0]) / 2
        
        return x, y

    def get_height(self, x: float, y: float) -> float:
        x, y = self._map_xy(x, y)
        return self.surface(x, y)
    
    def get_inclination(self, x: float, y: float) -> float:
        x, y = self._map_xy(x, y)
        dx, dy = self.inclination(x, y)
        dx, dy = self.rotate_coordinates(dx, dy, 0, 0, self.rotation)
        return dx, dy
    
    def see_flag(self, x: float, y: float) -> bool:
        return ((x-self.flag[0])**2 + (y-self.flag[1])**2) < self.visual_radius**2
    
    def is_out_of_bounds(self, x, y):
        return x**2 + y**2 > self.base_radius**2
    
    def rotate_coordinates(self, x, y, x0, y0, angle_rad):
        # Translate the coordinates by -x0 and -y0
        translated_x = x - x0
        translated_y = y - y0

        # Perform the rotation using the rotation matrix
        rotated_x = translated_x * math.cos(angle_rad) - translated_y * math.sin(angle_rad)
        rotated_y = translated_x * math.sin(angle_rad) + translated_y * math.cos(angle_rad)

        # Translate the coordinates back by x0 and y0
        i = rotated_x + x0
        j = rotated_y + y0

        return i, j
