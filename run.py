from communication.server.server import MountainServer
from communication.server.mountain.easy_mountain import EasyMountain
import subprocess
import os
s = MountainServer(EasyMountain(1, 23000), (0, 0), 50)
#file_path = os.path.join('/Users/juanfra/Documents/Facultad/Pensamiento computacional/TP_Final_PC', 'climber_instructions.py')
subprocess.Popen(['python3', 'climber_instructions.py'])

s.start()
