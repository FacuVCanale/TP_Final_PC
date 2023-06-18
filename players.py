class Player:
    def __init__(self,dic={},team="",name="",direction=50,speed=50,x=14000,y=14000,z=0,inclinacion_x= 0,inclinacion_y= 0,cima= False):
        self.team = team
        self.name = name
        self.direction = direction
        self.speed = speed
        self.x = x
        self.y = y
        self.z = z
        self.inclinacion_x = inclinacion_x
        self.inclinacion_y = inclinacion_y
        self.cima = cima
        if len(dic) > 0:
            self.x = dic["x"]
            self.y = dic["y"]
            self.z = dic["z"]
            self.inclinacion_x = dic["inclinacion_x"]
            self.inclinacion_y = dic["inclinacion_y"]
            self.cima = dic["cima"]
    def __getitem__(self, key):
        if key == "team":
            return self.team
        elif key == "name":
            return self.name
        elif key == "direction":
            return self.direction
        elif key == "speed":
            return self.speed
        elif key == "x":
            return self.x
        elif key == "y":
            return self.y
        elif key == "z":
            return self.z
        elif key == "inclinacion_x":
            return self.inclinacion_x
        elif key == "inclinacion_y":
            return self.inclinacion_y
        elif key == "cima":
            return self.cima
        else:
            raise KeyError(f"Key '{key}' is not valid")
    def __setitem__(self, key, value):
        if key == "team":
            self.team = value
        elif key == "name":
            self.name = value
        elif key == "direction":
            self.direction = value
        elif key == "speed":
            self.speed = value
        elif key == "x":
            self.x = value
        elif key == "y":
            self.y = value
        elif key == "z":
            self.z = value
        elif key == "inclinacion_x":
            self.inclinacion_x = value
        elif key == "inclinacion_y":
            self.inclinacion_y = value
        elif key == "cima":
            self.cima = value
        else:
            raise KeyError(f"Clave '{key}' no valida")
    def __gt__(self,otro):
        if ((self.cima is True) and (otro.cima is True)):
            return False
        elif ((self.cima is False) and (otro.cima is True)):
            return False
        elif ((self.cima is True) and (otro.cima is False)):
            return True
        elif self.z > otro.z:
            return True
        elif self.z <= otro.z:
            return False
        else:
            return False
    def __eq__(self, otro):
        return self.z == otro.z and self.cima == otro.cima

    def __lt__(self, otro):
        if self.cima and otro.cima:
            return False
        elif not self.cima and otro.cima:
            return False
        elif self.cima and not otro.cima:
            return True
        elif self.z < otro.z:
            return True
        else:
            return False

        
