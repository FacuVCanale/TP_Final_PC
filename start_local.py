from communication.server.server import MountainServer
from communication.server.mountain.easy_mountain import EasyMountain

s = MountainServer(EasyMountain(50, 23000), (14000, 14000), 50)
s.start()