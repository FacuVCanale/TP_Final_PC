from communication.server.mountain.mountain import Mountain
from typing import List
import math
import threading
import time

class BaseStation:
    
    TIMEOUT = 5 # seconds
    CHECK_DELAY = 0.05 # seconds

    def __init__(self, mountain: Mountain, base_position, max_speed) -> None:
        self.base_position = base_position
        self.mountain = mountain
        self.state = 'registering_teams'
        self.max_speed = max_speed
        self.teams = {}
        self.next_directions = {}

    def add_team(self, team: str, climbers: List[str]) -> bool:
        """
        Adds a team to the competition.

        Args:
            team (str): the team name.
            climbers (List[str]): a list of climbers.

        Returns:
            bool: True if the team was added successfully.

        Raises:
            RuntimeError: if the competition is not in the 'registering_teams' state.
        """
        if self.state != 'registering_teams':
            raise RuntimeError('The competition is not in the registering_teams state. Current state: ' + self.state)
       
        self.teams[team] = {}
        base_pos = (self.base_position[0], self.base_position[1], self.mountain.get_height(self.base_position[0], self.base_position[1]))
        inclination = self.mountain.get_inclination(self.base_position[0], self.base_position[1])
        for climber in climbers:
            self.teams[team][climber] = {
                'x': base_pos[0], 
                'y': base_pos[1], 
                'z': base_pos[2], 
                'inclinacion_x': inclination[0], 
                'inclinacion_y': inclination[1], 
                'cima': False
            }
        return True
    
    def finish_team_registration(self) -> bool:
        """
        Finishes the team registration phase.
        
        Returns:
            bool: True if the competition was finished successfully.

        Raises:
            RuntimeError: if the competition is not in the 'registering_teams' state.
        """
        if self.state != 'registering_teams':
            raise RuntimeError('The competition is not in the registering_teams state. Current state: ' + self.state)
        self.state = 'waiting_for_directions'
        self.thread = threading.Thread(target = self._check_timeout)
        self.timer = time.time()
        self.thread.start()
        return True

    def register_team_directions(self, team: str, directions: dict) -> bool:
        """
        Registers the directions of a team.

        Args:
            team (str): the team name.
            directions (dict): a dictionary containing the directions of each
            climber.
            
        Returns:
            bool: True if the directions were registered successfully.

        Raises:
            RuntimeError: if the competition is not in the 'waiting_for_directions'
            state or if the competition is over.
        """
        if not self.is_competition_ongoing():
            raise RuntimeError('The competition is already over.')
        elif self.state != 'waiting_for_directions':
            raise RuntimeError('The competition is not in the waiting_for_directions state. Current state: ' + self.state)
        elif team not in self.teams:
            raise RuntimeError('The team ' + team + ' is not registered.')
        
        self.next_directions[team] = {}
        for climber in directions:
            if climber not in self.teams[team]:
                raise RuntimeError('The climber ' + climber + ' is not in the team ' + team)
            else:
                if directions[climber]['speed'] > self.max_speed:
                    directions[climber]['speed'] = min(max(0, directions[climber]['speed']), self.max_speed)
                
                self.next_directions[team][climber] = directions[climber]
        return True

    def is_competition_ongoing(self) -> bool:
        """Check if the competition is ongoing.
        
        Returns:
            bool: True if the competition is ongoing, False otherwise."""
        if self.state == 'over':
            return False
        
        every_team_in_summit = True
        for team in list(self.teams.keys()):
            all_climbers_in_summit = True
            for climber in self.teams[team]:
                all_climbers_in_summit = all_climbers_in_summit and self.teams[team][climber]['cima']
            every_team_in_summit = every_team_in_summit and all_climbers_in_summit

        if every_team_in_summit:
            self.state = 'over'
            return False
        return True

    def get_data(self) -> dict:
        """Get the data of the climbers.

        Returns:
            dict: a dictionary containing the data of the climbers.
        """
        return self.teams

    def _check_timeout(self) -> None:
        """
        Move the climbers if the timeout is reached or all teams have sent their directions.
        """
        while self.is_competition_ongoing():
            while (time.time() - self.timer < self.TIMEOUT) and (self.teams.keys() != self.next_directions.keys()):
                time.sleep(self.CHECK_DELAY)
            self._move_climbers()
                                     
    def _move_climbers(self) -> None:
        """
        Process the received directions and move the climbers.
        """
        if self.is_competition_ongoing():
            self.state = 'moving'

            for team in self.next_directions:
                for climber in self.next_directions[team]:
                    if not self.teams[team][climber]['cima']:
                        self.teams[team][climber] = self._calculate_new_position(
                            (self.teams[team][climber]['x'], self.teams[team][climber]['y']), 
                            self.next_directions[team][climber]['direction'],
                            self.next_directions[team][climber]['speed']
                        )

            self._disqualify_missing_climbers()
            self.next_directions = {}
            self.state = 'waiting_for_directions'
            self.timer = time.time()

    def _disqualify_missing_climbers(self) -> None:
        """
        Disqualify climbers whose team has not sent directions or are out of bounds.
        Climbers that have reached the summit are not disqualified.
        """
        for team in list(self.teams.keys()): # list() is used to avoid RuntimeError: dictionary changed size during iteration
            if not self._are_all_team_climbers_in_summit(team):
                if team not in self.next_directions:
                    del self.teams[team]
                else:
                    for climber in list(self.teams[team].keys()):
                        self._disqualify_climber_if_missing(team, climber)
                        
    def _are_all_team_climbers_in_summit(self, team: str) -> bool:
        are_all_team_climbers_in_summit = True
        climber_idx = 0
        climbers = list(self.teams[team].keys())
        while are_all_team_climbers_in_summit and climber_idx < len(climbers):
            climber = climbers[climber_idx]
            are_all_team_climbers_in_summit = are_all_team_climbers_in_summit and self.teams[team][climber]['cima']
            climber_idx += 1
        return are_all_team_climbers_in_summit

    def _disqualify_climber_if_missing(self, team:str, climber: str) -> None:
        if not self.teams[team][climber]['cima']:
            if (climber not in self.next_directions[team]) or self._is_out_of_bounds(self.teams[team][climber]):
                del self.teams[team][climber]
                if len(self.teams[team]) == 0:
                    del self.teams[team]
           
    def _is_out_of_bounds(self, climber: dict) -> bool:
        """Check if a climber is out of bounds.
        
        Args:
            climber (dict): a dictionary containing the climber's data.
            
        Returns:
            bool: True if the climber is out of bounds, False otherwise."""
        return self.mountain.is_out_of_bounds(climber['x'], climber['y'])

    def _calculate_new_position(self, curr_pos: tuple, angle: float, speed: float) -> dict:
        x = curr_pos[0] + speed * math.cos(angle)
        y = curr_pos[1] + speed * math.sin(angle)
        z = self.mountain.get_height(x, y)
        summit = self.mountain.see_flag(x, y)
        dx, dy = self.mountain.get_inclination(x, y)
        data = {
                'x': x, 
                'y': y, 
                'z': z, 
                'inclinacion_x': dx, 
                'inclinacion_y': dy, 
                'cima': summit
            }
        return data
