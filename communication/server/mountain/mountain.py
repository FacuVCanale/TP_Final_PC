"""DO NOT MODIFY THIS FILE"""

class Mountain:
    """STUDENTS: DO NOT USE THIS CLASS"""
    def __init__(self, function, df, flag, visual_radius) -> None:
        self.surface = function
        self.inclination = df
        self.flag = flag
        self.visual_radius = visual_radius

    def get_height(self, x: float, y: float) -> float:
        return self.surface(x, y)
    
    def get_inclination(self, x: float, y: float) -> float:
        return self.inclination(x, y)
    
    def see_flag(self, x: float, y: float) -> bool:
        return ((x-self.flag[0])**2 + (y-self.flag[1])**2) < self.visual_radius**2
    
    def is_out_of_bounds(self, x, y):
        raise NotImplementedError("This method should be implemented by a subclass")