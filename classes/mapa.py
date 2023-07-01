
class Mapa_circular:
    def __init__(self, circulo: list, ESCALA: int = 1000) -> None:
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
        self.circulo = circulo
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
        for i in self.circulo:
            for j in i:
                if j == num_jugador:
                    self.circulo[i][j] = "."

        x = int(pos[0] / self.ESCALA)
        y = int(pos[1] / self.ESCALA)

        x += self.circulo.filas // 2
        y = self.circulo.filas // 2 - y
        
        self.circulo[y][x] = chr(num_jugador)

    def __repr__(self) -> str:
        """
        Return a string representation of the circular map object.

        Returns
        -------
        str
            A string representation of the circular map object.
        """
        return f"import circulo.py\n {self.circulo.str()}\n mapa = Mapa_circular(circle,1000)"

    def __str__(self) -> str:
        """
        Return a string representation of the circular map object.

        Returns
        -------
        str
            A string representation of the circular map object.
        """
        fil = len(self.circulo)
        result = ""
        for _ in range(fil):
            linea = ' '.join(self.circulo[_])
            result += linea + "\n"
        return result
