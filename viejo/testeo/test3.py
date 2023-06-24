from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import numpy as np


x = np.linspace(-2000, 2000, 1000)
y = np.linspace(-2000, 2000, 1000)

X, Y = np.meshgrid(x,y)

Z = -(np.sin(X+Y) + (X-Y)**2 - 1.5*X + 2.5*Y + 1)

# # 2D
# fig=plt.figure()
# plt.contourf(X,Y,Z,cmap='plasma')
# plt.axis('scaled')
# plt.colorbar()
# plt.show()

# 3D
fig = plt.figure()
ax = plt.axes(projection='3d')
ax.plot_surface(X, Y, Z, cmap="plasma", linewidth=0, antialiased=False, alpha=0.5)
# rotation
ax.view_init(30, 60)
# ax.set_zlim3d(0,100)
plt.show()

# #3D 2
# fig = plt.figure()
# ax = plt.axes(projection='3d')
# ax.contour3D(X, Y, Z, 50, cmap='plasma')
# ax.view_init(30, 60)
# plt.show()