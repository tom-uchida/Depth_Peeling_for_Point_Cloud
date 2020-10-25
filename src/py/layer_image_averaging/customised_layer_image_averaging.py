# customised_layer_image_averaging.py
#   Tomomasa Uchida
#   2020/10/25

import numpy as np
import cv2

# Check arguments
import sys
args = sys.argv
if len(args) != 4:
    print("\nUSAGE   : $ python {} [input_images_path] [num_of_layers] [image_resolution]".format(args[0]))
    print("EXAMPLE : $ python {} ../IMAGE_DATA 10 1000\n".format(args[0]))
    sys.exit()

def create_empty_images( _num_of_images ):
    empty_images_R = np.empty( (image_resol*1, image_resol*1, _num_of_images), dtype=np.uint8 )
    empty_images_G = np.empty( (image_resol*1, image_resol*1, _num_of_images), dtype=np.uint8 )
    empty_images_B = np.empty( (image_resol*1, image_resol*1, _num_of_images), dtype=np.uint8 )

    return empty_images_R, empty_images_G, empty_images_B

def read_layer_images():
    # Read the layer images
    for i in range( num_of_layers ):
        # Read each layer image
        tmp_image_BGR = cv2.imread( layer_images_path + "LayerImage" + str( i + 1 ) + ".bmp" )
        tmp_image_RGB = cv2.cvtColor( tmp_image_BGR, cv2.COLOR_BGR2RGB )

        # Split into RGB and add to numpy array
        layer_images_R[:,:,i] = tmp_image_RGB[:,:,0] # R
        layer_images_G[:,:,i] = tmp_image_RGB[:,:,1] # G
        layer_images_B[:,:,i] = tmp_image_RGB[:,:,2] # B

        if i == num_of_layers-1:
            print( "R: {}".format( layer_images_R.shape ) )
            print( "G: {}".format( layer_images_G.shape ) )
            print( "B: {}".format( layer_images_B.shape ) )
    # end for

def average_layer_images():
    # Create median image
    median_image_R, median_image_G, median_image_B = create_empty_images( 1 )
    median_image_R = np.median( layer_images_R, axis=2 )
    median_image_G = np.median( layer_images_G, axis=2 )
    median_image_B = np.median( layer_images_B, axis=2 )
    
    # Pixelwise layer image averaging
    # M_array = np.empty( (image_resol*1, image_resol*1), float )
    for y in range( image_resol ):     # height
        for x in range( image_resol ): # width
            for l in range( num_of_layers ):
                layer_images_R[y,x,l]
                layer_images_G[y,x,l]
                layer_images_B[y,x,l]

                final_pixel_value = 0
            # end for l
        # end for x
    # end for y


if __name__ == "__main__":
    # Set the number of layer images
    num_of_layers = int( args[2] )
    print( "Number of Layers: {}".format( num_of_layers ) )

    # Set image resolution
    image_resol = int( args[3] )
    print( "Image Resolution: {}".format( image_resol ) )


    # Read the target layer images
    layer_images_path = args[1] + "/"
    layer_images_R, layer_images_G, layer_images_B = create_empty_images( num_of_layers )
    read_layer_images()

    # Average the layer images
    average_layer_images()