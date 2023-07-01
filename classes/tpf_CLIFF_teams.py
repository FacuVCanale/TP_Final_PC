from classes.tpf_CLIFF_players import Player
from typing import Dict, List

class Team:
    """
    A class representing a team of players.

    Parameters
    ----------
    dic : dict
        A dictionary containing the players' information.

    Attributes
    ----------
    hikers : list
        A list of Player objects representing the team's players.

    Methods
    -------
    get_players() -> List[Player]
        Returns a list of all players in the team.
    """

    def __init__(self, dic: Dict[str, Dict[str, str]]) -> None:
        """
        Initializes the team by creating Player objects for each player.

        Parameters
        ----------
        dic : dict
            A dictionary containing the players' information.
        """
        self.hikers = []
        for self.name, players in dic.items():
            counter = 0
            for i,j in players.items():
                player = Player(j, self.name, i)
                self.hikers.append(player)
                counter += 1

    def get_players(self) -> List[Player]:
        """
        Returns a list of all players in the team.

        Returns
        -------
        list
            A list of Player objects representing the team's players.
        """
        temp = []
        cant = len(self.hikers)
        counter = 0
        while counter <= cant-1:
            temp.append(self.hikers[counter])
            counter += 1
        return temp
