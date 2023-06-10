from communication.server.mountain.easy_mountain import EasyMountain
from communication.server.server import MountainServer
while True:
    s = MountainServer(EasyMountain(1,10),(14000,14000),50,"10.182.0.3",8080)
    s.start()