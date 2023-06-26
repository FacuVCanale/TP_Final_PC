#!/usr/bin/env python3

import socket
from typing import List
import json

from communication.util.logger import logger


class MountainClient:
    def __init__(self, host: str='localhost', port: int=8080):
        """Initializes the MountainClient object.

        Args:
            host (str): The host name or IP address of the listening server.
            port (int): The port number in which the server is listening on. 
        """
        self.host = host
        self.port = port


    def add_team(self, team_name: str, hikers_names: List[str]) -> bool:
        """Sends the add_team command to the MountainServer.

        Args:
            team_name (str): The name of the team.
            hikers_names (List[str]): The names of the hikers.

        Returns:
            bool: True if the team was added successfully, False otherwise.

        Example:
            >>> client.add_team('team1', ['hiker1', 'hiker2'])
            True
        """
        data = {'command': 'add_team', 'team': team_name, 'hikers': hikers_names}
        data = json.dumps(data) 
        ans = self._socket_send(data)
        return ans == 'True'

    def next_iteration(self, team: str, directives: dict) -> bool:
        """Sends the directions the hikers will follow.

        Args:
            team (str): The name of the team.
            directives (dict): A dictionary containing the directions and speeds of each hiker.

        Returns:
            bool: True if the directions were communicated successfully, False otherwise.

        Example:
            directives = {
                'hiker1': {'direction': 0, 'speed': 50},
                'hiker2': {'direction': 3.14, 'speed': 50}
            }
            >>> client.next_iteration('team1', directives)
            True
        """

        data = {'command': 'walk', 'team': team, 'directions': directives}
        data = json.dumps(data) 
        ans = self._socket_send(data)
        return ans == 'True'

    def finish_registration(self) -> bool:
        """Sends the end_registration command to the MountainServer.

        Returns:
            bool: True if the registration was finished successfully, False otherwise.
        
        Example:
            >>> client.add_team('team1', ['hiker1', 'hiker2'])
            >>> client.finish_registration()
            True
        """

        data = {'command': 'end_registration'}
        data = json.dumps(data) 
        ans = self._socket_send(data)
        return ans == 'True'
    
    def get_data(self) -> dict[str, dict[str, dict[str, float]]]:
        """Sends the get_data command to the MountainServer.

        Returns:
            dict: The data of each hiker.

        Example:
            >>> client.get_data()
            {
                'team1': {
                    'hiker1.1': {
                        'x': 0,
                        'y': 0,
                        'z': 0,
                        'inclinacion_x': 0,
                        'inclinacion_y': 0,
                        'cima': False
                    },
                    'hiker1.2': {
                        'x': 0,
                        'y': 0,
                        'z': 0,
                        'inclinacion_x': 0,
                        'inclinacion_y': 0,
                        'cima': False
                    }
                },
                'team2': {
                    'hiker2.1': {
                        'x': 0,
                        'y': 0,
                        'z': 0,
                        'inclinacion_x': 0,
                        'inclinacion_y': 0,
                        'cima': False
                    }
                }
            }
        """

        data = {'command': 'get_data'}
        data = json.dumps(data) 
        ans = self._socket_send(data)
        ans = json.loads(ans)
        return ans
    
    def is_over(self) -> bool:
        """Sends the is_over command to the MountainServer.

        Returns:
            bool: True if the competition is over, False otherwise.

        Example:
            >>> client.is_over()
            False
        """

        data = {'command': 'is_over'}
        data = json.dumps(data) 
        ans = self._socket_send(data)
        return ans == 'True'
    
    def is_registering_teams(self) -> bool:
        """Sends the is_registering_teams command to the MountainServer.

        Returns:
            bool: True if the registration is still open, False otherwise.

        Example:
            >>> client.is_registering_teams()
            True
        """

        data = {'command': 'is_registering_teams'}
        data = json.dumps(data) 
        ans = self._socket_send(data)
        return ans == 'True'
    
    def get_mountain(self) -> str:
        """Sends the get_mountain command to the MountainServer.

        Returns:
            str: The name of the mountain.

        Example:
            >>> client.get_mountain()
            'EasyMountain'
        """

        data = {'command': 'get_mountain'}
        data = json.dumps(data) 
        ans = self._socket_send(data)
        return ans

    def _socket_send(self, data: str) -> str:
        """Sends the data to the server using a socket.

        This method sends the bytes representation of the data in utf-8
        using TCP as the L4 protocol.

        Args:
            data (str): the raw data in string format.

        Returns:
            str: the raw data received from the server in string format.
        """
        # Create a socket (SOCK_STREAM means a TCP socket)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Connect to server and send data
            s.connect((self.host, self.port))
            logger.debug(f"Sending data: {data}")
            s.sendall(bytes(data + "\n", "utf-8"))

            # Receive data from the server and shut down
            last_received = False
            received = ""
            while not last_received:
                b = s.recv(1024)
                
                if b == b'':
                    last_received = True
                else:
                    
                    chunk = str(b, "utf-8")
                    received += chunk
            logger.debug(f"Received data: {received}")
            s.close()

        return received


