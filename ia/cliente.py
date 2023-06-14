#El nombre del equipo es CopNieve
# codigo
from communication.client.client import MountainClient
from communication.util.logger import logger
import random
import math




from typing import Any, Callable, Dict, List, NamedTuple, Tuple, Union

import gymnasium
import numpy as np

from stable_baselines3.common.env_checker import check_env
GymObs = Union[Tuple, Dict, np.ndarray, int]

PI = 3.14159265356979

class MountainEnv(gymnasium.Env):
  """
  Minimal custom environment to demonstrate the Gym interface.
  """
  def __init__(self, function:function, dxdy:function, base_pos:tuple=(14000, 14000), radius:float=23000., min_height:float=20., max_height:float=250., max_speed:float=50.):   # AGREGUÉ ARGUMENTOS PARA CUANDO LLAMEMOS A MOUNTAIN_ENV
    super().__init__()
    self.observation_space = gymnasium.spaces.Box(low=np.array([-1 * radius, -1 * radius, min_height, 0., 0., 0.], dtype='float32'), high=np.array([radius, radius, max_height, np.inf, np.inf, 1.], dtype='float32'), shape=(6,), dtype ="float32")
    self.action_space = gymnasium.spaces.Box(low=np.array([0., 0.], dtype='float32'), high=np.array([2.*PI, 50.]), shape=(2,))
    self._state = (base_pos[0], base_pos[1], self.function(base_pos[0], base_pos[1]), dxdy(base_pos[0], base_pos[1])[0], dxdy(base_pos[0], base_pos[1])[1])
    self._episode_ended = False
    self.function = function
    self.dxdy = dxdy
    self.base_pos = base_pos

  def reset(self, seed=0) -> Tuple[GymObs, dict]:
    """
    Called at the beginning of an episode.
    :return: the first observation of the episode
    """
    info = {}
    return self.observation_space.sample(), info

  def step(self, action: Union[int, np.ndarray]) -> Tuple[GymObs, float, bool, Dict]:
    """
    Step into the environment.
    :return: A tuple containing the new observation, the reward signal,
      whether the episode is over and additional informations.
    """
    obs = self.observation_space.sample()
    reward = 1.0
    terminated = False
    truncated = False
    info = {}
    return obs, reward, terminated, truncated, info
  
  def is_out_of_bounds(self, x, y):
        return x**2 + y**2 > self.radius**2
  
  def _calculate_new_position(self, curr_pos: tuple, angle: float, speed: float) -> dict:
    x = curr_pos[0] + speed * math.cos(angle)
    y = curr_pos[1] + speed * math.sin(angle)
    z = self.mountain.get_height(x, y)
    summit = self.mountain.see_flag(x, y)
    dx, dy = self.mountain.get_inclination(x, y)

env = MountainEnv()
# Check your custom environment
# this will print warnings and throw errors if needed
check_env(env)

cliente = MountainClient("34.16.147.147",8080)


directions ={}
directions['facu'] = {'speed': 30, 'direction': 45}
cliente.add_team("LIFFT",['facu'])
cliente.finish_registration()
def mandar_data():
    while not cliente.is_over():
        info = cliente.get_data() #{'LIFFT': {'facu': {'x': 14000, 'y': 14000, 'z': -14109979074.0, 'inclinacion_x': -503966.0, 'inclinacion_y': -503962.0, 'cima': False}
        print(info)
        cliente.next_iteration("LIFFT", directions)
        directions['facu']['direction'] += random.choice([i for i in range(300)])
mandar_data()








"""
def _calculate_new_position(self, curr_pos: tuple, angle: float, speed: float) -> dict:
    x = curr_pos[0] + speed * math.cos(angle)
    y = curr_pos[1] + speed * math.sin(angle)
    z = self.mountain.get_height(x, y)
    summit = self.mountain.see_flag(x, y)
    dx, dy = self.mountain.get_inclination(x, y)
    data = {
            'x': x, 
            'y': y, 
            'z': z, 
            'inclinacion_x': dx, 
            'inclinacion_y': dy, 
            'cima': summit
        }
    return data
"""

"""
import sys
class Mountain:
    def __init__(self, function, df, flag, visual_radius) -> None:
        self.surface = function
        self.inclination = df
        self.flag = flag
        self.visual_radius = visual_radius

    def get_height(self, x: float, y: float) -> float:
        return self.surface(x, y)
    
    def get_inclination(self, x: float, y: float) -> float:
        return self.inclination(x, y)
    
    def see_flag(self, x: float, y: float) -> bool:
        if ((x-self.flag[0])**2 + (y-self.flag[1])**2) < self.visual_radius**2:
            sys.exit(0)
        else:
            return False
    def is_out_of_bounds(self, x, y):
        raise NotImplementedError("This method should be implemented by a subclass")
"""

"""
class CircularBaseMountain(Mountain):
    def __init__(self, function, df, flag, visual_radius, base_radius) -> None:
        super().__init__(function, df, flag, visual_radius)
        self.base_radius = base_radius

    def get_height(self, x: float, y: float) -> float:
        return self.surface(x, y)
    
    def get_inclination(self, x: float, y: float) -> float:
        return self.inclination(x, y)
    
    def see_flag(self, x: float, y: float) -> bool:
        return ((x-self.flag[0])**2 + (y-self.flag[1])**2) < self.visual_radius**2
    
    def is_out_of_bounds(self, x, y):
        return x**2 + y**2 > self.base_radius**2
"""