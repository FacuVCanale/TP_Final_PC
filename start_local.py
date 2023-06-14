from communication.server.server import MountainServer
from communication.server.mountain.easy_mountain import EasyMountain

s = MountainServer(EasyMountain(1, 23000), (0, 0), 50)
s.start()
