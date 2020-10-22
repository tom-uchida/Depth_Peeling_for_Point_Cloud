# calc_num_of_effective_pixels.py
#   Tomomasa Uchida
#   2020/10/22

import numpy as np
import cv2
import pandas as pd

# Check arguments
import sys
args = sys.argv
if len(args) != 4:
    print("\nUSAGE   : $ python calc_num_of_effective_pixels.py [input_images_path] [num_of_layers] [image_resolution]")
    print("EXAMPLE : $ python calc_num_of_effective_pixels.py ../IMAGE_DATA 10 1000\n")
    sys.exit()



def ReadImage( _img_name ):
    # read input image
    img_BGR = cv2.imread( _img_name )

    # convert color BGR to RGB
    img_RGB = cv2.cvtColor( img_BGR, cv2.COLOR_BGR2RGB )

    return img_RGB



def run( _num_of_layers, _image_resol, _serial_img_path ):
    # Create dataframe
    nCol = 2
    df = pd.DataFrame( np.zeros(_num_of_layers*nCol).reshape(_num_of_layers, nCol) )
    df.columns = ['Layer', 'nPixels']

    sum_of_effective_pixels = 0
    for i in range( _num_of_layers ):
        # Read each layer image
        image_RGB = ReadImage( _serial_img_path + "LayerImage" + str( i + 1 ) + ".bmp" )

        # Convert RGB to Grayscale
        image_Gray = cv2.cvtColor( image_RGB, cv2.COLOR_RGB2GRAY )

        # Exclude background color pixels
        image_Gray_non_BGColor = image_Gray[image_Gray != 0]

        # Count effective pixels
        effective_pixels = image_Gray_non_BGColor.shape[0]
        sum_of_effective_pixels += effective_pixels

        # Add to dataframe
        df.at[i, 'Layer']   = i + 1
        df.at[i, 'nPixels'] = effective_pixels
    # end for
    
    # Write to csv file
    df.to_csv( '/Users/uchidatomomasa/work/SPBR/myProject/SPBR_Depth_Peeling/src/py/csv/Layer_Num-of-Effective-Pixels.csv', sep=",", index=False, header=True )

    # print( "The number of effective pixels: {}".format( sum_of_effective_pixels ) )
    # print( "\ndf: {}".format( df ) )
# end run()



if __name__ == "__main__":
    # Set the number of the layer images
    num_of_layers = int( args[2] )
    print( "Num. of Layer Images : {}".format( num_of_layers ) )

    # Set image resolution
    image_resol = int( args[3] )
    print( "Image Resolution     : {}".format( image_resol ) )

    # Read target images
    layer_img_path = args[1] + "/"
    run( num_of_layers, image_resol, layer_img_path )