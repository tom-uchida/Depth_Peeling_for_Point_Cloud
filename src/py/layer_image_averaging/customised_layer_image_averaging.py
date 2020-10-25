# customised_layer_image_averaging.py
#   Tomomasa Uchida
#   2020/10/25

import numpy as np
import cv2
import time

# Check arguments
import sys
args = sys.argv
if len(args) != 4:
    print("\nUSAGE   : $ python {} [input_images_path] [num_of_layers] [image_resolution]".format(args[0]))
    print("EXAMPLE : $ python {} ../IMAGE_DATA 10 1000\n".format(args[0]))
    sys.exit()

def create_empty_2d_array():
    empty_2d_array = np.empty( ( image_resol, image_resol ), dtype=np.uint8 )

    return empty_2d_array

def create_empty_3d_array( _num_of_images ):
    empty_3d_array = np.empty( ( image_resol, image_resol, _num_of_images ), dtype=np.uint8 )
    
    return empty_3d_array

def read_layer_images():
    # Read the layer images
    for layer in range( num_of_layers ):
        # Read each layer image
        tmp_image_BGR  = cv2.imread( layer_images_path + "LayerImage" + str( layer + 1 ) + ".bmp" )
        tmp_image_RGB  = cv2.cvtColor( tmp_image_BGR, cv2.COLOR_BGR2RGB )
        tmp_image_GRAY = cv2.cvtColor( tmp_image_RGB, cv2.COLOR_RGB2GRAY )
        
        # Add to numpy array
        layer_images_R[:,:,layer]    = tmp_image_RGB[:,:,0] # R
        layer_images_G[:,:,layer]    = tmp_image_RGB[:,:,1] # G
        layer_images_B[:,:,layer]    = tmp_image_RGB[:,:,2] # B
        layer_images_GRAY[:,:,layer] = tmp_image_GRAY       # GRAY

        if layer == 0:
            print( "R   : {}".format( layer_images_R.shape ) )
            print( "G   : {}".format( layer_images_G.shape ) )
            print( "B   : {}".format( layer_images_B.shape ) )
            print( "GRAY: {}".format( layer_images_GRAY.shape ) )
    # end for layer
# End read_layer_images()

def is_this_pixel_noise( _target_pixel_value ):
    is_noise_pixel = False
    return is_noise_pixel

def average_layer_images():
    # Create median image
    median_image_R = create_empty_2d_array()
    median_image_G = create_empty_2d_array()
    median_image_B = create_empty_2d_array()
    median_image_R = np.median( layer_images_R, axis=2 )
    median_image_G = np.median( layer_images_G, axis=2 )
    median_image_B = np.median( layer_images_B, axis=2 )

    # Pixelwise layer image averaging
    layer_averaged_image = create_empty_2d_array()
    bool_idx = np.empty( (num_of_layers), bool )
    print( "\nNow calculating..." )
    start = time.time()
    for y in range( image_resol ):
        for x in range( image_resol ):
            for layer in range( num_of_layers ):
                # Get the target pixel value
                target_pixel_value_GRAY = layer_images_GRAY[y,x,layer]

                # Check if the pixel is noise pixel
                if is_this_pixel_noise( target_pixel_value_GRAY ) == False:
                    bool_idx[layer] = True
                else:
                    bool_idx[layer] = False
                # end if
            # end for layer

            # Extract only non-noise pixels
            non_noise_pixel_values = layer_images_GRAY[y,x,bool_idx]

            # Average the pixel values
            layer_averaged_image[y,x] = np.sum( non_noise_pixel_values ) / non_noise_pixel_values.size
        # end for x
    # end for y

    print ("Done! ({} [sec])\n".format( round(time.time() - start , 2) ) )

    # Save the result image
    # layer_averaged_image_BGR = cv2.cvtColor( layer_averaged_image, cv2.COLOR_RGB2BGR )
    cv2.imwrite( layer_images_path + "Layer_Averaged_Image.png", layer_averaged_image )

if __name__ == "__main__":
    # Set the number of layer images
    num_of_layers = int( args[2] )
    print( "\nNumber of Layers: {}".format( num_of_layers ) )

    # Set image resolution
    image_resol = int( args[3] )
    print( "Image Resolution: {}".format( image_resol ) )

    # Read the target layer images
    layer_images_R    = create_empty_3d_array( num_of_layers )
    layer_images_G    = create_empty_3d_array( num_of_layers )
    layer_images_B    = create_empty_3d_array( num_of_layers )
    layer_images_GRAY = create_empty_3d_array( num_of_layers )
    layer_images_path = args[1] + "/"
    read_layer_images()

    # Average the layer images
    average_layer_images()