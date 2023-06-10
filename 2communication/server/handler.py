import json

from socketserver import BaseRequestHandler

from communication.util.logger import logger

class TCPHandler(BaseRequestHandler):

    def handle(self) -> None:
        """A TCP handler responsible for addressing the TCP queries."""
        self.data = bytes.decode(self.request.recv(1024).strip(), 'utf-8')
        self.data = json.loads(self.data)
        
        logger.debug(f"Received data: {self.data}")
        
        if self.data['command'] == 'add_team':
            try:
                ans = self.server.base_station.add_team(self.data['team'], self.data['climbers'])
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
            except RuntimeError as e:
                ans = False
        elif self.data['command'] == 'get_data':
            ans = self.server.base_station.get_data()
        elif self.data['command'] == 'is_over':
            ans = not self.server.base_station.is_competition_ongoing()
        else:
            ans = 'NACK'

        if type(ans) == str:
            self.request.sendall(bytes(ans, encoding='utf-8'))
        elif type(ans) == bool:
            self.request.sendall(bytes(str(ans), encoding='utf-8'))
        else:
            self.request.sendall(bytes(json.dumps(ans), encoding='utf-8'))

