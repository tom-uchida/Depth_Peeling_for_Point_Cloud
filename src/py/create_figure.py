# create_figure.py
#   Tomomasa Uchida
#   2020/10/15

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
plt.style.use('bmh')
plt.rcParams["mathtext.fontset"] = "cm"
plt.rcParams["mathtext.rm"] = "Times New Roman"
plt.rcParams["font.size"] = 14
plt.figure( figsize=(8,6) )

# Check arguments
import sys
args = sys.argv
if len(args) != 3:
    print("\nUSAGE   : $ python create_figure.py [csv_file_1] [csv_file_2]")
    print("EXAMPLE : $ python create_figure.py SPBR.csv LayerAvg.csv\n")
    sys.exit()



# Read csv file
csv_SPBR        = pd.read_csv( args[1] )
csv_LayerAvg    = pd.read_csv( args[2] )

# Convert to numpy array
L_mean_std      = csv_SPBR.values
Layer_mean_std  = csv_LayerAvg.values

# Get each column
L, mean_SPBR, std_SPBR = L_mean_std[:,0], L_mean_std[:,1], L_mean_std[:,2]
Layer, mean_LayerAvg, std_LayerAvg = Layer_mean_std[:,0], Layer_mean_std[:,1], Layer_mean_std[:,2]

# Creat figure
plt.scatter( Layer, mean_LayerAvg, color='#24217D', label='mean(LayerAvg.)', marker="o" )
plt.scatter( L, mean_SPBR, color='red', label='mean(SPBR)', marker="o" )

plt.scatter( Layer, std_LayerAvg, color='#24217D', label='std(LayerAvg.)', marker="^" )
plt.scatter( L, std_SPBR, color='red', label='std(SPBR)', marker="^" )

plt.legend( fontsize=14 )
plt.xlabel( 'The number of averaged images', fontsize=14 )
plt.ylabel( 'Pixel Value', fontsize=14 )
plt.xticks( [1, 20, 40, 60, 80, 100], fontsize=14 )
plt.yticks( [1, 20, 40, 60, 80, 100], fontsize=14 )

# plt.grid()
plt.show()