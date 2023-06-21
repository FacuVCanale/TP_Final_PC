from teams import Team
class Partida:
    def __init__(self,dic):
        self.dic = dic
        self.teams = []
        for i,j in self.dic.items():
            dictt = {}
            dictt["{i}"] = j
            team = Team(dictt)
            self.teams.append(team)
    def get_teams(self):
        temp = []
        cant = len(self.teams)
        counter = 0
        while counter <= cant-1:
            temp.append(self.teams[counter])
            counter += 1
        return temp