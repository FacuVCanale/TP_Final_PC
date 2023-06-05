#!/usr/bin/env python

from typing import Tuple, List
from socketserver import BaseRequestHandler, TCPServer

from communication.server.handler import TCPHandler
from communication.server.mountain.mountain import Mountain
from communication.server.base_station import BaseStation
from communication.util.logger import logger

class CustomTCPServer(TCPServer):
    def __init__(self, host_port: Tuple[str, int], handler: BaseRequestHandler, mountain: Mountain, base_position: Tuple[float, float], max_speed: float):
        """Instantiates a custom TPC server.

        Args:
            host_port (Tuple[str, int]): a tuple containing both host and port
            of the server.
            handler: a TCP handler configured to address queries.
            mountain: a Mountain instance to inject to the server.
        """
        super().__init__(host_port, handler)
        self.base_station = BaseStation(mountain, base_position, max_speed)

class BaseMountainServer:

    def __init__(self, host: str, port: int):
        """Don't use this method from outside another __init__ method.

        This class should be considered as an abstract class.

        Args:
            host (str): Hostname or IP address to bind the server.
            port (int): Port number to listen to.

        Raises:
            If port is not an integer it will fail.
        """

        if not isinstance(port, int):
            raise TypeError("Port must be an integer")
        
        self.host = host
        self.port = port

    def _start(self, handler: BaseRequestHandler, mountain: Mountain, base_position: Tuple[float, float], max_speed: float):
        """Binds and starts the server.

        Args:
            handler (BaseRequestHandler): a TCP handler to be used.
            mountain (Mountain): the mountain instance to be used by the TCP handler.
        """

        with CustomTCPServer((self.host,self.port), handler, mountain, base_position, max_speed) as server:
            server.serve_forever()



class MountainServer(BaseMountainServer):
    """Instantiates a server.

        Args:
            host (str): Host or IP address to bind to.
            port (int): Port number to listen to.
    """

    def __init__(self, mountain: Mountain, base_position: Tuple, max_speed, host: str='localhost', port: int=8080):
        super().__init__(host=host, port=port)
        self.base_position = base_position
        self.max_speed = max_speed
        self.mountain = mountain


    def start(self):
        """Starts the server"""
        self._start(TCPHandler, self.mountain, self.base_position, self.max_speed) 