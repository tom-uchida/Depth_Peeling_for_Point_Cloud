import numpy as np
import cv2
from matplotlib import pyplot as plt
from matplotlib import cycler
import matplotlib.gridspec as gridspec

# Plot settings
plt.style.use('bmh')
colors = cycler('color', ['#EE6666', '#3388BB', '#9988DD', '#EECC55', '#88BB44', '#FFBBBB'])
plt.rc('axes', facecolor='#E6E6E6', edgecolor='none', axisbelow=True, grid=False, prop_cycle=colors)
plt.rcParams["mathtext.fontset"] = "cm"
plt.rcParams["mathtext.rm"] = "Times New Roman"

# Check arguments
import sys
args = sys.argv
if len(args) != 7:
    print( "\nUSAGE   : $ python {} [R1] [G1] [B1] [R2] [G2] [B2]".format (args[0] ) )
    print( "EXAMPLE : $ python {} 0 0 0 255 255 255\n".format( args[0] ) )
    sys.exit()

def calc_color_distance( _color1, _color2 ):
    # In RGB color space, calc the euclidean distance
    r1, r2 = _color1[0], _color2[0]
    g1, g2 = _color1[1], _color2[1]
    b1, b2 = _color1[2], _color2[2]
    color_dist2 = (r1-r2)**2 + (g1-g2)**2 + (b1-b2)**2

    return color_dist2

def create_figure( _color1, _color2 ):
    # Create color image
    color1_image = np.empty( ( 256, 256, 3 ), dtype=np.uint8 )
    color2_image = np.empty( ( 256, 256, 3 ), dtype=np.uint8 )

    color1_image[:,:,0], color2_image[:,:,0] = _color1[0], _color2[0]
    color1_image[:,:,1], color2_image[:,:,1] = _color1[1], _color2[1]
    color1_image[:,:,2], color2_image[:,:,2] = _color1[2], _color2[2]

    # Create figure
    fig = plt.figure( figsize=(8, 4) ) # figsize=(width, height)
    gs  = gridspec.GridSpec(1, 2)

    ax1 = fig.add_subplot( gs[0, 0] )
    title1 = 'Color1: (' + str(_color1[0]) + ', ' + str(_color1[1]) + ', ' + str(_color1[2]) + ')'
    ax1.set_title( title1, fontsize=12 )
    ax1.imshow( color1_image )
    ax1.axis("off")

    ax2 = fig.add_subplot( gs[0, 1] )
    title2 = 'Color2: (' + str(_color2[0]) + ', ' + str(_color2[1]) + ', ' + str(_color2[2]) + ')'
    ax2.set_title( title2, fontsize=12 )
    ax2.imshow( color2_image )
    ax2.axis("off")
    
    plt.savefig( "./figure_d" + str( round( color_dist ) ) + ".png" )
    print( "** Saved the figure." )
    print( "" )

if __name__ == "__main__":
    color1 = [int(args[1]), int(args[2]), int(args[3])]
    color2 = [int(args[4]), int(args[5]), int(args[6])]
    print( "" )
    print( "** Color1: ({}, {}, {})".format( color1[0], color1[1], color1[2] ) )
    print( "** Color2: ({}, {}, {})".format( color2[0], color2[1], color2[2] ) )

    color_dist = np.sqrt( calc_color_distance( color1, color2 ) )
    print( "" )
    print( "** Color distance: {}".format( color_dist ) )

    create_figure( color1, color2 )