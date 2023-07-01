class Player:
    def __init__(self, dic: dict = {}, team: str = "", name: str = "", direction: int = 50, speed: int = 50, x: int = 14000, y: int = 14000, z: int = 0, inclinacion_x: int = 0, inclinacion_y: int = 0, cima: bool = False) -> None:
        """
        A class representing a player in a game.

        Parameters
        ----------
        dic : dict, optional
            A dictionary containing the player's position and orientation, by default {}.
        team : str, optional
            The player's team, by default "".
        name : str, optional
            The player's name, by default "".
        direction : int, optional
            The player's direction, by default 50.
        speed : int, optional
            The player's speed, by default 50.
        x : int, optional
            The player's x-coordinate, by default 14000.
        y : int, optional
            The player's y-coordinate, by default 14000.
        z : int, optional
            The player's z-coordinate, by default 0.
        inclinacion_x : int, optional
            The player's x-inclination, by default 0.
        inclinacion_y : int, optional
            The player's y-inclination, by default 0.
        cima : bool, optional
            Whether the player has reached the top of a mountain, by default False.
        """
        self.team = team
        self.name = name.capitalize()
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

    def __getitem__(self, key: str) -> any:
        """
        Get an attribute of the player.

        Parameters
        ----------
        key : str
            The name of the attribute to get.

        Returns
        -------
        any
            The value of the attribute.

        Raises
        ------
        KeyError
            If the attribute name is not valid.
        """
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

    def __setitem__(self, key: str, value: any) -> None:
        """
        Set an attribute of the player.

        Parameters
        ----------
        key : str
            The name of the attribute to set.
        value : any
            The value to set the attribute to.

        Raises
        ------
        KeyError
            If the attribute name is not valid.
        """
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
            raise KeyError(f"Key '{key}' is not valid")

    def __gt__(self, otro: 'Player') -> bool:
        """
        Compare the player to another player.

        Parameters
        ----------
        otro : Player
            The other player to compare to.

        Returns
        -------
        bool
            True if the player is greater than the other player, False otherwise.
        """
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

    def __eq__(self, otro: 'Player') -> bool:
        """
        Compare the player to another player for equality.

        Parameters
        ----------
        otro : Player
            The other player to compare to.

        Returns
        -------
        bool
            True if the player is equal to the other player, False otherwise.
        """
        return self.z == otro.z and self.cima == otro.cima

    def __lt__(self, otro: 'Player') -> bool:
        """
        Compare the player to another player.

        Parameters
        ----------
        otro : Player
            The other player to compare to.

        Returns
        -------
        bool
            True if the player is less than the other player, False otherwise.
        """
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
