from climbers import Climbers
from communication.client.client import MountainClient

cliente = MountainClient()

def team2():
    player = Climbers({'name': "facu", 'pos': (0,0)})
    

    directions ={}
    directions[player.name] = {'speed': 10, 'direction': 45}
    climber2 = [player]
    cliente.add_team("lifft",[climber.name for climber in climber2])
    
    

    return directions, player.name



def team1():
    player = Climbers({'name': "peres", 'pos': (0,0)})


    directions2 ={}
    directions2[player.name] = {'speed': 10, 'direction': 45}


    climber2 = [player]
    cliente.add_team("EQUIPO_PERES",[climber.name for climber in climber2])
    


    return directions2,  player.name


  

