# import plotly.express as px
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

plt.style.use('bmh')
plt.rcParams["mathtext.fontset"] = "cm"
plt.rcParams["mathtext.rm"] = "Times New Roman"
plt.rcParams["font.size"] = 14

fig = plt.figure( figsize=(10, 8) )
ax = fig.gca( projection='3d' )

color1 = [255, 0, 0]
color2 = [0, 0, 255]

ax.plot( [color1[0]], [color1[1]], [color1[2]], color='r', label='color1', marker='o', markersize=20 )
ax.plot( [color2[0]], [color2[1]], [color2[2]], color='b', label='color2', marker='o', markersize=20 )
ax.legend()

# Draw a line
import mpl_toolkits.mplot3d.art3d as art3d
line = art3d.Line3D([2,3,4,5,6,7,8],[2,3,4,5,6,7,8],[3,5,3,5,3,5,3], color='g')
ax.add_line(line)

ax.set_title( "Color distance", fontsize=16 )
ax.set_xlabel( r'$R$', fontsize=20, color='r' )
ax.set_ylabel( r'$G$', fontsize=20, color='g' )
ax.set_zlabel( r'$B$', fontsize=20, color='b' )

ax.set_xticklabels( [0, 50, 100, 150, 200, 250], fontsize=10)
ax.set_yticklabels( [0, 50, 100, 150, 200, 250], fontsize=10)
ax.set_zticklabels( [0, 50, 100, 150, 200, 250], fontsize=10)


plt.show()