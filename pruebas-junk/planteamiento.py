""" register_team_directions(self, team: str, directions: dict): Registra las direcciones de un equipo. Recibe el nombre del equipo y un diccionario que contiene las direcciones de cada escalador del equipo. Estas direcciones incluyen la dirección de movimiento y la velocidad.

El archivo handler.py se utiliza para enviar indicaciones al servidor. Contiene la clase TCPHandler, que es un controlador de solicitudes TCP responsable de abordar las consultas TCP. En el método handle, se procesa la solicitud recibida y se envía una respuesta al cliente.

Dentro del método handle, se verifica el campo 'command' de los datos recibidos para determinar la acción que se debe realizar en el servidor. Dependiendo del valor de 'command', se ejecutan diferentes operaciones en el objeto self.server.base_station, que es una instancia de la clase BaseStation.
 """

""" server.py: Este archivo contiene la implementación principal del servidor. Define la clase CustomTCPServer, que es una subclase de TCPServer y se utiliza para crear una instancia del servidor personalizado. Esta clase se encarga de inicializar la base de datos de la estación base y manejar las solicitudes TCP entrantes.

handler.py: Este archivo define la clase TCPHandler, que es una subclase de BaseRequestHandler. El TCPHandler se utiliza como manejador para las solicitudes TCP entrantes. En el método handle(), se procesan las solicitudes recibidas y se toman acciones en función del comando recibido.

base_station.py: Este archivo contiene la implementación de la clase BaseStation, que representa la estación base del servidor. La estación base administra los equipos, los movimientos de los escaladores y el estado general de la competencia. Contiene métodos para agregar equipos, finalizar el registro de equipos, registrar direcciones de equipo, verificar si la competencia está en curso, obtener los datos de los escaladores, etc. """
import socket
import json

# Datos de conexión al servidor
server_host = 'localhost'  # Dirección IP o nombre de host del servidor
server_port = 8080  # Puerto del servidor

# Datos de la indicación a enviar
indicacion = {
    'command': 'add_team',  # Comando para agregar un equipo (puedes cambiarlo según la operación que desees realizar)
    'team': 'equipo1',  # Nombre del equipo
    'climbers': ['climber1', 'climber2']  # Lista de escaladores
}

# Convertir los datos a formato JSON
data = json.dumps(indicacion)

# Establecer conexión con el servidor
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((server_host, server_port))

    # Enviar los datos al servidor
    sock.sendall(bytes(data, encoding='utf-8'))

    # Esperar la respuesta del servidor
    response = sock.recv(1024)

# Decodificar la respuesta del servidor
response = response.decode('utf-8')

print(f'Respuesta del servidor: {response}')

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
import json
import socket

# Datos de conexión al servidor
server_host = 'localhost'  # Dirección IP o nombre de host del servidor
server_port = 8080  # Puerto del servidor

# Datos de la indicación a enviar
indicacion = {
    'command': 'walk',  # Comando para indicar que el equipo debe caminar
    'team': 'equipo1',  # Nombre del equipo
    'directions': {
        'x': 3  # Distancia a caminar en el eje x
    }
}

# Convertir los datos a formato JSON
data = json.dumps(indicacion)

# Establecer conexión con el servidor
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((server_host, server_port))

    # Enviar los datos al servidor
    sock.sendall(bytes(data, encoding='utf-8'))

    # Esperar la respuesta del servidor
    response = sock.recv(1024)

# Decodificar la respuesta del servidor
response = response.decode('utf-8')

print(f'Respuesta del servidor: {response}')

