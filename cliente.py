#El nombre del equipo es CopNieve
# codigo
from communication.client.client import MountainClient
from communication.util.logger import logger


cliente1 = MountainClient("34.16.147.147",8080)

cliente1.add_team("ROJO",["Juan","Valen","Santi","Fede"])

cliente1.finish_registration()
data = cliente1.get_data()
print(data)
logger.warning(f"Datos: {data}")
