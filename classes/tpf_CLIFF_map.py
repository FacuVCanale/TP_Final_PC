from classes.tpf_CLIFF_circle_creator import Circle

class Circular_map:
    def __init__(self, circle: Circle, SCALE: int = 1000) -> None:
        """
        Initialize a circular map object with a given circle and scale.

        Parameters
        ----------
        circulo : list
            The circle to use for the map.
        SCALE : int, optional
            The scale to use for the map. Default is 1000.

        Returns
        -------
        None
        """
        self.circle = circle
        self.SCALE = SCALE

    def add_player(self, pos: tuple, num_player: int) -> None:
        """
        Add a player to the map at the given position.

        Parameters
        ----------
        pos : tuple
            The position of the player on the map.
        num_player : int
            The number of the player to add.

        Returns
        -------
        None
        """
        for i in self.circle:
            for j in i:
                if j == num_player:
                    self.circle[i][j] = "."

        x = int(pos[0] / self.SCALE)
        y = int(pos[1] / self.SCALE)

        x += self.circle.rowss // 2
        y = self.circle.rowss // 2 - y
        
        self.circle[y][x] = chr(num_player)

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
