from communication.client.client import MountainClient

c = MountainClient()
c.add_team('T1', ['E1', 'E2'])
c.add_team('T2', ['E1', 'E2'])
c.finish_registration()
while not c.is_over():
    print(c.get_data())

{'T1': 
 {
'E1': 
  {'x': 14000, 'y': 14000, 'z': 3134.8468809073725, 'inclinacion_x': -185.1304347826087, 'inclinacion_y': -181.1304347826087, 'cima': False}, 
'E2': {'x': 14000, 'y': 14000, 'z': 3134.8468809073725, 'inclinacion_x': -185.1304347826087, 'inclinacion_y': -181.1304347826087, 'cima': False}}, 'T2': {'E1': {'x': 14000, 'y': 14000, 'z': 3134.8468809073725, 'inclinacion_x': -185.1304347826087, 'inclinacion_y': -181.1304347826087, 'cima': False}, 'E2': {'x': 14000, 'y': 14000, 'z': 3134.8468809073725, 'inclinacion_x': -185.1304347826087, 'inclinacion_y': -181.1304347826087, 'cima': False}}}