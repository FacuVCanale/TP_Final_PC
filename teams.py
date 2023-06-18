from players import Player
class Team:
    def __init__(self,dic):
        self.hikers = []
        for self.name, players in dic.items():
            counter = 0
            for i,j in players.items():
                player = Player(j, self.name, i)
                self.hikers.append(player)
                counter += 1
        self.hikers.sort()
    def get_players(self):
        temp = []
        cant = len(self.hikers)
        counter = 0
        while counter < cant-1:
            temp.append(self.hikers[counter].name)
        return temp #NO FUNCIONA CORRECTAMENTE | FALTA UNA VUELTA DE TUERCA | SON LAS 5AM       
        