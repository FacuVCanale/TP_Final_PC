from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import numpy as np


x = np.linspace(-20000, 20000, 1000)
y = np.linspace(-20000, 20000, 1000)

X, Y = np.meshgrid(x,y)

ans = -20*np.exp(-0.2*np.sqrt(0.5*(X**2 + Y**2))) - np.exp(0.5*(np.cos(2*np.pi*X) + np.cos(2*np.pi*Y))) + np.e + 20
Z = -ans + 20
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
plt.show()

# #3D 2
# fig = plt.figure()
# ax = plt.axes(projection='3d')
# ax.contour3D(X, Y, Z, 50, cmap='plasma')
# ax.view_init(30, 60)
# plt.show()