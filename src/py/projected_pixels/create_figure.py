# create_figure.py
#   Tomomasa Uchida
#   2020/10/22

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
plt.style.use('bmh')
plt.rcParams["mathtext.fontset"] = "cm"
plt.rcParams["mathtext.rm"] = "Times New Roman"
plt.rcParams["font.size"] = 14
plt.figure( figsize=(10, 8) )

# Check arguments
import sys
args = sys.argv
if len(args) != 2:
    print("\nUSAGE   : $ python create_figure.py [csv_file]")
    print("EXAMPLE : $ python create_figure.py *.csv\n")
    sys.exit()



# Read csv file
Layer_nPixels   = pd.read_csv( args[1] ).values

# Get each column
Layer, nPixels  = Layer_nPixels[:, 0], Layer_nPixels[:, 1]

# Calc cumulative about nPixels
nPixels_sum = 0
nPixels_cum = np.zeros( Layer.shape[0] )
for i in range( Layer.shape[0] ):
    nPixels_sum     += nPixels[i]
    nPixels_cum[i]   = nPixels_sum
print( "The sum of projected pixels: {} (pixels)".format( nPixels_sum ) )


# Creat figure

plt.scatter( Layer, nPixels, color='black', marker="o" )
plt.ylabel( 'Number of projected pixels', fontsize=24 )
# plt.scatter( Layer, nPixels_cum, color='black', marker="o" )
# plt.ylabel( 'Cumulative number of projected pixels', fontsize=24 )

plt.xlabel( 'Layer', fontsize=24 )
plt.xticks( [1, 20, 40, 60, 80], fontsize=20 )
plt.yticks( fontsize=20 )

ax = plt.gca()
ax.ticklabel_format( style="sci",  axis="y",scilimits=(0,0) )

# plt.grid()
plt.show()