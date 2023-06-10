from communication.server.mountain.mountain import Mountain

class CircularBaseMountain(Mountain):
    def __init__(self, function, df, flag, visual_radius, base_radius) -> None:
        super().__init__(function, df, flag, visual_radius)
        self.base_radius = base_radius

    def get_height(self, x: float, y: float) -> float:
        return self.surface(x, y)
    
    def get_inclination(self, x: float, y: float) -> float:
        return self.inclination(x, y)
    
    def see_flag(self, x: float, y: float) -> bool:
        return ((x-self.flag[0])**2 + (y-self.flag[1])**2) < self.visual_radius**2
    
    def is_out_of_bounds(self, x, y):
        return x**2 + y**2 > self.base_radius**2