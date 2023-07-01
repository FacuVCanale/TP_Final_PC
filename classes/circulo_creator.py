class Circulo:
    def __init__(self, filas: int):
        """
        Initialize a circle object with a given number of rows.

        Parameters
        ----------
        filas : int
            The number of rows in the circle.

        Returns
        -------
        None
        """
        self.filas = filas
        # Create an empty list to store the circle
        self.circulo = []
        # Create the matrix of the circle
        for fila in range(self.filas):
            # Create an empty list for each row
            nueva_fila = []
            for columna in range(self.filas):
                # Check if the current point is inside the circle
                if (columna - 23) ** 2 + (fila - 23) ** 2 <= 23 ** 2:
                    nueva_fila.append(".")
                else:
                    nueva_fila.append(" ")
            # Add the row to the circle list
            self.circulo.append(nueva_fila)
        self.indice = 0

    @property
    def filas(self) -> int:
        """
        Get the number of rows in the circle.

        Returns
        -------
        int
            The number of rows in the circle.
        """
        return self.filas

    def __str__(self) -> str:
        """
        Return a string representation of the circle object.

        Returns
        -------
        str
            A string representation of the circle object.
        """
        return f"This circle has {self.filas} rows!"

    def __repr__(self) -> str:
        """
        Return a string representation of the circle object.

        Returns
        -------
        str
            A string representation of the circle object.
        """
        return f"circle = Circulo=(46)"

    def __iter__(self):
        """
        Return an iterator over the rows of the circle.

        Returns
        -------
        iterator
            An iterator over the rows of the circle.
        """
        return self

    def __next__(self):
        """
        Return the next row of the circle.

        Returns
        -------
        list
            The next row of the circle.
        """
        if self.indice >= self.filas:
            raise StopIteration
        fila_actual = self.circulo[self.indice]
        self.indice += 1
        return fila_actual

    def __getitem__(self, index):
        """
        Get the row of the circle at the given index.

        Parameters
        ----------
        index : int
            The index of the row to get.

        Returns
        -------
        list
            The row of the circle at the given index.
        """
        return self.circulo[index]

    def __len__(self):
        """
        Get the number of rows in the circle.

        Returns
        -------
        int
            The number of rows in the circle.
        """
        return len(self.circulo)
