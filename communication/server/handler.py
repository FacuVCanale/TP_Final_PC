"""DO NOT MODIFY THIS FILE"""

import json

from socketserver import BaseRequestHandler

from communication.util.logger import logger

class TCPHandler(BaseRequestHandler):

    def handle(self) -> None:
        """
        A TCP handler responsible for addressing the TCP queries. The requests sent by a client are handled here.
        The client must send a JSON with a field called 'command' and other fields depending on the command.
        
        Commands:
            - add_team: adds a team to the competition. 
                Args: The JSON must contain the fields 'team' and 'hikers'.
                Returns: True if the team was added successfully, False otherwise.
                Example: {"command": "add_team", "team": "team1", "hikers": ["hiker1", "hiker2"]}
            
            - end_registration: ends the registration phase. 
                Args: The JSON does not need any other field.
                Returns: True if the registration phase was ended successfully, False otherwise.
                Example: {"command": "end_registration"}
            
            - walk: registers the directions and speeds directed by a team. 
                Args: The JSON must contain the fields 'team' and 'directions'.
                Returns: True if the directions were registered successfully, False otherwise.
                Example: 
                {
                    "command": "walk", 
                    "team": "team1", 
                    "directions": [
                        {"direction": 0, "speed": 50}, 
                        {"direction": 3.14, "speed": 50}
                    ]
                }
            
            - get_data: returns the data of the competition.
                Args: The JSON does not need any other field.
                Returns: A JSON with the following fields:
                    {
                        "team_name": {
                            "hiker1": {
                                "x": (float),
                                "y": (float),
                                "z": (float),
                                "inclinacion_x": (float),
                                "inclinacion_y": (float),
                                "cima": (bool)
                            }
                    }
                Example: {"command": "get_data"}

            - is_over: returns True if the competition is over.
                Args: The JSON does not need any other field.
                Returns: True if the competition is over, False otherwise.
                Example: {"command": "is_over"}

            - is_registering_teams: returns True if the competition is registering teams.
                Args: The JSON does not need any other field.
                Returns: True if the competition is registering teams, False otherwise.
                Example: {"command": "is_registering_teams"}

            - get_mountain: returns the mountain information.
                Args: The JSON does not need any other field.
                Returns: A JSON with the following fields:
                    {"mountain": (str)}
                Example: {"command": "get_mountain"}

        """


        self.data = bytes.decode(self.request.recv(1024).strip(), 'utf-8')
        try:
            self.data = json.loads(self.data)
        except:
            logger.warn('Invalid request. It may be too long. It will be ignored.')
            return 'NACK'
        
        logger.debug(f"Received request")
        logger.debug(f"Received data: {self.data}")
        
        if self.data['command'] == 'add_team':
            try:
                ans = self.server.base_station.add_team(self.data['team'], self.data['hikers'])
            except RuntimeError as e:
                ans = False
        elif self.data['command'] == 'end_registration':
            try:
                ans = self.server.base_station.finish_team_registration()
            except RuntimeError as e:
                ans = False
        elif self.data['command'] == 'walk':
            try:
                ans = self.server.base_station.register_team_directions(self.data['team'], self.data['directions'])
            except (RuntimeError, ValueError) as e:
                ans = False
        elif self.data['command'] == 'get_data':
            ans = self.server.base_station.get_data()
        elif self.data['command'] == 'is_over':
            ans = not self.server.base_station.is_competition_ongoing()
        elif self.data['command'] == 'is_registering_teams':
            ans = self.server.base_station.is_registering_teams()
        elif self.data['command'] == 'get_mountain':
            ans = self.server.base_station.get_mountain()
        else:
            logger.debug(f"Unknown command: {self.data['command']}")
            ans = 'NACK'

        logger.debug(f"Answer data: {ans}")
        if type(ans) == dict:
            self.request.sendall(bytes(json.dumps(ans), encoding='utf-8'))
        else:
            self.request.sendall(bytes(str(ans), encoding='utf-8'))

    def finish(self):
        self.server.shutdown_request(self.request)