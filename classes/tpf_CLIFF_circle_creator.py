class Circle:
    def __init__(self, rows:int):
        self.rowss = rows
        # Create an empty list to store the circle
        self.circle = []
        # Create the matrix of the circle
        for row in range(self.rowss):
            # Create an empty list for each row
            new_row = []
            for column in range(self.rowss):
                # Check if the current point is inside the circle
                if (column - 23) ** 2 + (row - 23) ** 2 <= 23 ** 2:
                    new_row.append(".")
                else:
                    new_row.append(" ")
            # Add the row to the circle list
            self.circle.append(new_row)
        self.index = 0

    
    def rows(self) -> int:
        """
        Get the number of rows in the circle.

        Returns
        -------
        int
            The number of rows in the circle.
        """
        return self.rowss

    def __str__(self) -> str:
        """
        Return a string representation of the circle object.

        Returns
        -------
        str
            A string representation of the circle object.
        """
        return f"This circle has {self.rowss} rows!"

    def __repr__(self) -> str:
        """
        Return a string representation of the circle object.

        Returns
        -------
        str
            A string representation of the circle object.
        """
        return f"circle = Circle(46)"

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
        if self.index >= self.rowss:
            raise StopIteration
        current_row = self.circle[self.index]
        self.index += 1
        return current_row

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
        return self.circle[index]

    def __len__(self):
        """
        Get the number of rows in the circle.

        Returns
        -------
        int
            The number of rows in the circle.
        """
        return len(self.circle)