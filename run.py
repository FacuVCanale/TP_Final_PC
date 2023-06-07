from communication.server.server import MountainServer
from communication.server.mountain.easy_mountain import EasyMountain
import subprocess


s = MountainServer(EasyMountain(1,23000),(0,0),50)
subprocess.Popen(['python', 'climber_instructions.py'])


s.start()



