class Mapa_circular:
    def __init__(self,circulo,ESCALA=1000):
        self.circulo = circulo
        self.ESCALA = ESCALA
    def agregar_pj(self,pos, num_jugador, flag):
        for i in self.circulo:
            for j in i:
                if j == num_jugador:
                    self.circulo[i][j] = "X"

        x = int(pos[0] / self.ESCALA)
        y = int(pos[1] / self.ESCALA)

        x += self.circulo.filas // 2
        y = self.circulo.filas // 2 - y

        self.circulo[y][x] = f"{chr(num_jugador)}"

        #if type(flag) == bool:
        #    self.circulo[y][x] = f"\033[92m{chr(num_jugador)}\033[0m"
        #else:
        #    self.circulo[y][x] = "\033[94m" + "chr(num_jugador)"+"\033[0m"
        #no es compatible con archivos .txt

    def __repr__(self) -> str:
        return f"import circulo.py\n {self.circulo.str()}\n mapa = Mapa_circular(circle,1000)"
    def __str__(self) -> str: #NOT WORKING
        result = ""
        for fila in self.circulo:
            result += " ".join(fila) + "\n"
        return result