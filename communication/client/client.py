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


    def add_team(self, team_name: str, climbers_names: List[str]) -> bool:
        """Sends the add_team command to the MountainServer.

        Args:
            team_name (str): The name of the team.
            climbers_names (List[str]): The names of the climbers.

        Returns:
            bool: True if the team was added successfully, False otherwise.
        """
        data = {'command': 'add_team', 'team': team_name, 'climbers': climbers_names}
        data = json.dumps(data) 
        ans = self._socket_send(data)
        return ans == 'True'

    def next_iteration(self, team: str, directions: dict) -> bool:
        """Sends the directions the climbers will follow.

        Args:
            team (str): The name of the team.
            directions (dict): The directions the climbers will follow. Key: climber name, value: direction.

        Returns:
            bool: True if the directions were communicated successfully, False otherwise.
        """

        data = {'command': 'walk', 'team': team, 'directions': directions}
        data = json.dumps(data) 
        ans = self._socket_send(data)
        return ans == 'True'

    def finish_registration(self) -> bool:
        """Sends the end_registration command to the MountainServer.

        Returns:
            bool: True if the registration was finished successfully, False otherwise.
        """

        data = {'command': 'end_registration'}
        data = json.dumps(data) 
        ans = self._socket_send(data)
        return ans == 'True'
    
    def get_data(self) -> dict:
        """Sends the get_data command to the MountainServer.

        Returns:
            dict: The data of each climber.
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
        """

        data = {'command': 'is_over'}
        data = json.dumps(data) 
        ans = self._socket_send(data)
        return ans == 'True'

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
                chunk = str(s.recv(4096), "utf-8")
                received += chunk
                if len(chunk) < 4096:
                    last_received = True
            logger.debug(f"Received data: {received}")
        return received

