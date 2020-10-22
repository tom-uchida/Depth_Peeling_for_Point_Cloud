# calc_mean_pixel_value.py
#   Tomomasa Uchida
#   2020/10/14

import cv2
import numpy as np

# Check arguments
import sys
args = sys.argv
if len( args ) != 2:
    print( "\nUSAGE   : $ python calc_mean_pixel_value.py [input_image]" )
    print( "EXAMPLE : $ python calc_mean_pixel_value.py image.bmp\n" )
    sys.exit()

def ReadImage( _img_name ):
    # read input image
    img_BGR = cv2.imread( _img_name )

    # convert color BGR to RGB
    img_RGB = cv2.cvtColor( img_BGR, cv2.COLOR_BGR2RGB )

    return img_RGB

def display_statistical_value_of_image( _img_RGB ):
    # Convert RGB to Grayscale
    img_Gray = cv2.cvtColor( _img_RGB, cv2.COLOR_RGB2GRAY )

    # Exclude bgcolor pixels
    img_Gray_non_BGColor = img_Gray[img_Gray != 0]
    
    print( "Mean    : {}".format( img_Gray_non_BGColor.mean() ) )
    print( "Min     : {}".format( np.min( img_Gray_non_BGColor ) ) )
    print( "Max     : {}".format( np.max( img_Gray_non_BGColor ) ) )
    print( "Std     : {}".format( np.std( img_Gray_non_BGColor ) ) )
    print( "Median  : {}".format( np.median( img_Gray_non_BGColor ) ) )

if __name__ == "__main__":
    img_RGB = ReadImage( args[1] )
    display_statistical_value_of_image( img_RGB )