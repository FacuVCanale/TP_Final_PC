from communication.client.client import MountainClient
import math

MAX_SPEED = 50  # learning rate
MOMENTUM = 0.5
momentum = [0, 0] # momentum, beta

c = MountainClient('34.16.147.147', 8080)
c.add_team('LIFFT', ['FACU', 'FRAN', 'IVAN', 'LUQUI'])
c.finish_registration()
while True:
    directions_lifft = {'FACU': {'speed': 50, 'direction': 0},
                        'FRAN': {'speed': 50, 'direction': 0},
                        'IVAN': {'speed': 50, 'direction': 0},
                        'LUQUI': {'speed': 50, 'direction': 0}}
    data = c.get_data()
    for climber in data["LIFFT"]:
        momentum[0] = MOMENTUM * momentum[0] + climber['inclinacion_x']
        momentum[1] = MOMENTUM * momentum[1] + climber['inclinacion_y']
        
        x_new, y_new = climber['x'] - MAX_SPEED * momentum[0], climber['y'] - MAX_SPEED * momentum[1]

        delta_x = x_new - climber['x']
        delta_y = y_new - climber['y']

        angle = math.atan2(delta_x, delta_y) * (180/math.pi)
        print(angle)

        directions_lifft[climber]['direction'] = angle

    c.next_iteration('LIFFT', directions_lifft)
    print(data)
        
    
    

{'T1': 
 {
'E1': 
  {'x': 14000, 'y': 14000, 'z': 3134.8468809073725, 'inclinacion_x': -185.1304347826087, 'inclinacion_y': -181.1304347826087, 'cima': False}, 
'E2': {'x': 14000, 'y': 14000, 'z': 3134.8468809073725, 'inclinacion_x': -185.1304347826087, 'inclinacion_y': -181.1304347826087, 'cima': False}}, 'T2': {'E1': {'x': 14000, 'y': 14000, 'z': 3134.8468809073725, 'inclinacion_x': -185.1304347826087, 'inclinacion_y': -181.1304347826087, 'cima': False}, 'E2': {'x': 14000, 'y': 14000, 'z': 3134.8468809073725, 'inclinacion_x': -185.1304347826087, 'inclinacion_y': -181.1304347826087, 'cima': False}}}