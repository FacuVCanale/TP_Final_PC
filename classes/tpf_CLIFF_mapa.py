
class Circular_map:
    def __init__(self, circle: list, ESCALA: int = 1000) -> None:
        """
        Initialize a circular map object with a given circle and scale.

        Parameters
        ----------
        circulo : list
            The circle to use for the map.
        ESCALA : int, optional
            The scale to use for the map. Default is 1000.

        Returns
        -------
        None
        """
        self.circle = circle
        self.ESCALA = ESCALA

    def agregar_pj(self, pos: tuple, num_jugador: int, flag: bool) -> None:
        """
        Add a player to the map at the given position.

        Parameters
        ----------
        pos : tuple
            The position of the player on the map.
        num_jugador : int
            The number of the player to add.
        flag : bool
            A flag indicating whether the player is on the blue team (True) or the red team (False).

        Returns
        -------
        None
        """
        for i in self.circle:
            for j in i:
                if j == num_jugador:
                    self.circle[i][j] = "."

        x = int(pos[0] / self.ESCALA)
        y = int(pos[1] / self.ESCALA)

        x += self.circle.filas // 2
        y = self.circle.filas // 2 - y
        
        self.circle[y][x] = chr(num_jugador)

    def __repr__(self) -> str:
        """
        Return a string representation of the circular map object.

        Returns
        -------
        str
            A string representation of the circular map object.
        """
        return f"import circulo.py\n {self.circle.str()}\n mapa = Mapa_circular(circle,1000)"

    def __str__(self) -> str:
        """
        Return a string representation of the circular map object.

        Returns
        -------
        str
            A string representation of the circular map object.
        """
        fil = len(self.circle)
        result = ""
        for _ in range(fil):
            linea = ' '.join(self.circle[_])
            result += linea + "\n"
        return result
