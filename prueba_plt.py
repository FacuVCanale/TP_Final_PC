import math
import numpy as np

x = 1
y = 1
x_array = np.array([1, 2, 3])
y_array = np.array([4, 5, 6])

angle_math = math.atan2(y, x)
angle_numpy = np.arctan2(y, x)

print(angle_math)     # Output: 0.7853981633974483
print(angle_numpy)    # Output: [0.78539816 0.89605538 0.98279372]
print(type(angle_numpy))
