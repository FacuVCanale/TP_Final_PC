class Circulo:
    def __init__(self,filas:int):
        self.filas = filas
        # Crear una lista vacía para almacenar el círculo
        self.circulo = []
        # Crear la matriz del círculo
        for fila in range(self.filas):
            # Crear una lista vacía para cada fila
            nueva_fila = []
            for columna in range(self.filas):
                # Verificar si el punto actual está dentro del círculo
                if (columna - 23)**2 + (fila - 23)**2 <= 23**2:
                    nueva_fila.append('X')
                else:
                    nueva_fila.append(' ')
            # Agregar la fila a la lista del círculo
            self.circulo.append(nueva_fila)
        self.indice = 0
    def filas(self) ->int:
        return self.filas
    def __str__(self) -> str:
        return f"Este circulo es de {self.filas} filas!"
    def __repr__(self) -> str:
        return f"circle = Circulo=(46)"
    def __iter__(self):
        return self
    def __next__(self):
        if self.indice >= self.filas:
            raise StopIteration
        fila_actual = self.circulo[self.indice]
        self.indice += 1
        return fila_actual
    def __getitem__(self, index):
        return self.circulo[index]
    def __len__(self):
        return len(self.circulo)