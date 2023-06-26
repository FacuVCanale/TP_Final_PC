"""DO NOT MODIFY THIS FILE"""

from communication.server.mountain.abstract.mountain import Mountain
from typing import List
import math
import threading
import time

from communication.util.logger import logger

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
        self.minutes_passed = 0

    def add_team(self, team: str, hikers: List[str]) -> bool:
        """
        Adds a team to the competition.

        Args:
            team (str): the team name.
            hikers (List[str]): a list of hikers.

        Returns:
            bool: True if the team was added successfully.

        Raises:
            RuntimeError: if the competition is not in the 'registering_teams' state.
        """
        if self.state != 'registering_teams':
            msg = 'The competition is not in the registering_teams state. Current state: ' + self.state
            logger.warn(msg)
            raise RuntimeError(msg)
       
        self.teams[team] = {}
        base_pos = (self.base_position[0], self.base_position[1], self.mountain.get_height(self.base_position[0], self.base_position[1]))
        inclination = self.mountain.get_inclination(self.base_position[0], self.base_position[1])
        for hiker in hikers:
            self.teams[team][hiker] = {
                'x': base_pos[0], 
                'y': base_pos[1], 
                'z': base_pos[2], 
                'inclinacion_x': inclination[0], 
                'inclinacion_y': inclination[1], 
                'cima': False
            }
        logger.info('Team ' + team + ' added to the competition. Hikers: ' + str(hikers) + '.')
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
            msg = 'The competition is not in the registering_teams state. Current state: ' + self.state
            logger.warn(msg)
            raise RuntimeError(msg)
        self.state = 'waiting_for_directions'
        self.timer = time.time()
        self.thread = threading.Thread(target = self._check_timeout)
        self.thread.start()
        logger.info('Team registration finished.')
        return True
    
    def is_registering_teams(self) -> bool:
        """Check if the competition is registering teams.
        
        Returns:
            bool: True if the competition is registering teams, False otherwise."""
        return self.state == 'registering_teams'

    def register_team_directions(self, team: str, directions: dict) -> bool:
        """
        Registers the directions of a team.

        Args:
            team (str): the team name.
            directions (dict): a dictionary containing the directions of each
            hiker.
            
        Returns:
            bool: True if the directions were registered successfully.

        Raises:
            RuntimeError: if the competition is not in the 'waiting_for_directions'
            state or if the competition is over.
            ValueError: if the directions dictionary is not well formed.
        """
        msg = ''
        if not self.is_competition_ongoing():
            msg = 'The competition is already over.'
        elif self.state != 'waiting_for_directions':
            msg = 'The competition is not in the waiting_for_directions state. Current state: ' + self.state
        elif team not in self.teams:
            msg = 'The team ' + team + ' is not registered.'
       
        if msg:
            logger.warn(msg)
            raise RuntimeError(msg)
        
        self.next_directions[team] = {}
        for hiker in directions:
            msg = ''
            if hiker not in self.teams[team]:
                msg = 'The hiker ' + hiker + ' is not in the team ' + team + '.'
            elif type(directions[hiker]) != dict:
                msg = 'The sent dictionary is malformed.'
            elif 'speed' not in directions[hiker]:
                msg = 'The hiker ' + hiker + ' of the team ' + team + ' did not receive speed.'
            elif 'direction' not in directions[hiker]:
                msg = 'The hiker ' + hiker + ' of the team ' + team + ' did not receive direction.'
            
            if msg:
                logger.warn(msg)
                raise ValueError(msg)
            else:
                if directions[hiker]['speed'] > self.max_speed:
                    directions[hiker]['speed'] = min(max(0, directions[hiker]['speed']), self.max_speed)
                
                self.next_directions[team][hiker] = directions[hiker]
        logger.debug('Team ' + team + ' sent directions: ' + str(directions) + '.')
        return True

    def is_competition_ongoing(self) -> bool:
        """Check if the competition is ongoing.
        
        Returns:
            bool: True if the competition is ongoing, False otherwise."""
        if self.state == 'over':
            return False
        
        if self.minutes_passed >= 10080: # 1 semana
            self.state = 'over'
            logger.info('Competition is over. Hikers have already been 1 week in the mountain. We are calling them back')
            return False
        
        every_team_in_summit = True
        for team in list(self.teams.keys()):
            all_hikers_in_summit = True
            for hiker in self.teams[team]:
                all_hikers_in_summit = all_hikers_in_summit and self.teams[team][hiker]['cima']
            every_team_in_summit = every_team_in_summit and all_hikers_in_summit

        if every_team_in_summit:
            self.state = 'over'
            logger.info('Competition is over. Every (not disqualified) team reached the summit.')
            return False
        return True

    def get_data(self) -> dict:
        """Get the data of the hikers.

        Returns:
            dict: a dictionary containing the data of the hikers.
        """
        logger.debug('Sending data: ' + str(self.teams) + '.')
        return self.teams
    
    def get_minutes_passed(self) -> int:
        """Get the minutes passed since the competition started.
        
        Returns:
            int: the minutes passed since the competition started."""
        return self.minutes_passed
    
    def get_mountain(self) -> str:
        return str(self.mountain).split(' ')[0].split('.')[-1]

    def _set_server(self, server):
        self.server = server

    def _check_timeout(self) -> None:
        """
        Move the hikers if the timeout is reached or all teams have sent their directions.
        """
        while self.is_competition_ongoing():
            while (time.time() - self.timer < self.TIMEOUT) and (self.teams.keys() != self.next_directions.keys()):
                time.sleep(self.CHECK_DELAY)
            if self.teams.keys() == self.next_directions.keys():
                logger.debug('All teams sent directions.')
            else:
                logger.info(f'Timeout ({self.TIMEOUT} s) reached.')
            self._move_hikers()
        logger.info('Closing server.')
        time.sleep(5)
        self.server.shutdown()
        self.server.server_close()
                                     
    def _move_hikers(self) -> None:
        """
        Process the received directions and move the hikers.
        """
        if self.is_competition_ongoing():
            self.state = 'moving'

            for team in self.next_directions:
                for hiker in self.next_directions[team]:
                    if not self.teams[team][hiker]['cima']:
                        self.teams[team][hiker] = self._calculate_new_position(
                            (self.teams[team][hiker]['x'], self.teams[team][hiker]['y']), 
                            self.next_directions[team][hiker]['direction'],
                            self.next_directions[team][hiker]['speed']
                        )
                        if self.teams[team][hiker]['cima']:
                            logger.info('Hiker ' + hiker + ' of team ' + team + ' reached the summit. Time taken: ' + \
                                    str(self.minutes_passed) + ' minutes.')

            self._disqualify_missing_hikers()
            self.next_directions = {}
            self.minutes_passed += 1
            self.state = 'waiting_for_directions'
            logger.debug('Hikers moved.')
            if self.minutes_passed % 60 == 0:
                remaining_hikers = 0
                for team in self.teams:
                    for hiker in self.teams[team]:
                        if not self.teams[team][hiker]['cima']:
                            remaining_hikers += 1

                logger.info(f'{self.minutes_passed} minutes of competition passed. Remaining hikers: ' + \
                            f'{remaining_hikers}.')
            self.timer = time.time()

    def _disqualify_missing_hikers(self) -> None:
        """
        Disqualify hikers whose team has not sent directions or are out of bounds.
        hikers that have reached the summit are not disqualified.
        """
        for team in list(self.teams.keys()): # list() is used to avoid RuntimeError: dictionary changed size during iteration
            if not self._are_all_team_hikers_in_summit(team):
                if team not in self.next_directions:
                    del self.teams[team]
                    logger.info('Team ' + team + ' was disqualified because it did not send directions.')
                else:
                    for hiker in list(self.teams[team].keys()):
                        self._disqualify_hiker_if_missing(team, hiker)
                        
    def _are_all_team_hikers_in_summit(self, team: str) -> bool:
        are_all_team_hikers_in_summit = True
        hiker_idx = 0
        hikers = list(self.teams[team].keys())
        while are_all_team_hikers_in_summit and hiker_idx < len(hikers):
            hiker = hikers[hiker_idx]
            are_all_team_hikers_in_summit = are_all_team_hikers_in_summit and self.teams[team][hiker]['cima']
            hiker_idx += 1
        return are_all_team_hikers_in_summit

    def _disqualify_hiker_if_missing(self, team:str, hiker: str) -> None:
        if not self.teams[team][hiker]['cima']:
            if (hiker not in self.next_directions[team]):
                logger.info(self.next_directions)
                del self.teams[team][hiker]
                logger.info('Hiker ' + hiker + ' of team ' + team + ' was disqualified because it did not send directions.')
            elif self._is_out_of_bounds(self.teams[team][hiker]):
                del self.teams[team][hiker]
                logger.info('Hiker ' + hiker + ' of team ' + team + ' was disqualified because it is out of bounds.')

            if len(self.teams[team]) == 0:
                del self.teams[team]
                logger.info('Team ' + team + ' was disqualified because it has no hikers left.')
           
    def _is_out_of_bounds(self, hiker: dict) -> bool:
        """Check if a hiker is out of bounds.
        
        Args:
            hiker (dict): a dictionary containing the hiker's data.
            
        Returns:
            bool: True if the hiker is out of bounds, False otherwise."""
        return self.mountain.is_out_of_bounds(hiker['x'], hiker['y'])

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
