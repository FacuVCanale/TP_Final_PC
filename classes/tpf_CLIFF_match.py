from classes.tpf_CLIFF_teams import Team
from typing import List, Any, Dict

class Match:
    def __init__(self, dic: Dict[Any, Any]) -> None:
        """
        Initializes a Match object.

        Parameters:
        - dic (Dict[Any, Any]): A dictionary representing the teams and players.

        Returns:
        None
        """
        self.dic = dic
        self.teams: List[Team] = []
        for i, j in self.dic.items():
            dictt = {}
            dictt[str(i)] = j
            team = Team(dictt)
            self.teams.append(team)
    
    def get_teams(self) -> List[Team]:
        """
        Returns a list of Team objects.

        Parameters:
        None

        Returns:
        List[Team]: A list of Team objects.
        """
        temp: List[Team] = []
        cant: int = len(self.teams)
        counter: int = 0
        while counter <= cant - 1:
            temp.append(self.teams[counter])
            counter += 1
        return temp
