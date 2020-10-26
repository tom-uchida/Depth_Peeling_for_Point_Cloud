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

def create_empty_2d_array_uint8():
    empty_2d_array_uint8 = np.empty( ( image_resol, image_resol ), dtype=np.uint8 )

    return empty_2d_array_uint8

def create_empty_3d_array_uint8( _num_of_images ):
    empty_3d_array_uint8 = np.empty( ( image_resol, image_resol, _num_of_images ), dtype=np.uint8 )
    
    return empty_3d_array_uint8

def create_empty_3d_array_float32( _num_of_images ):
    empty_3d_array_float32 = np.empty( ( image_resol, image_resol, _num_of_images ), dtype=np.float32 )
    
    return empty_3d_array_float32

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

        # if layer == 0:
        #     print( "R   : {}".format( layer_images_R.shape ) )
        #     print( "G   : {}".format( layer_images_G.shape ) )
        #     print( "B   : {}".format( layer_images_B.shape ) )
        #     print( "GRAY: {}".format( layer_images_GRAY.shape ) )
    # end for layer
# End read_layer_images()

def create_original_image():
    median_image_GRAY = create_empty_2d_array_uint8()
    median_image_GRAY = np.median( layer_images_GRAY[:,:,:NUM_OF_REF_LAYER_IMAGES], axis=2 )

    return median_image_GRAY

def is_this_pixel_noise( _RGB, _original_pixel_value ):
    is_noise_pixel = False

    # Convert RGB to GRAY
    grayscale = 0.299*_RGB[0] + 0.587*_RGB[1] + 0.114*_RGB[2]

    target_pixel_value = grayscale
    diff = np.abs( target_pixel_value - _original_pixel_value )
    if diff >= NOISE_THRESHOLD:
        is_noise_pixel = True

    return is_noise_pixel

def average_layer_images():
    # Pixelwise layer image averaging
    target_RGB           = [0] * 3
    is_non_noise_pixels  = np.empty( (num_of_layers), bool )
    layer_averaged_image = create_empty_3d_array_uint8( 3 )
    print( "\nNow creating the layer-averaged image..." )
    start = time.time()
    for y in range( image_resol ):
        for x in range( image_resol ):
            for layer in range( num_of_layers ):
                # Get the target pixel value
                target_RGB[0] = layer_images_R[y,x,layer]
                target_RGB[1] = layer_images_G[y,x,layer]
                target_RGB[2] = layer_images_B[y,x,layer]

                # Check if the pixel is noise pixel
                if is_this_pixel_noise( target_RGB, original_image[y,x] ) == False:
                    is_non_noise_pixels[layer] = True
                else:
                    is_non_noise_pixels[layer] = False
                # end if
            # end for layer

            # Get only non-noise pixels
            R_pixel_values = layer_images_R[y,x,is_non_noise_pixels]
            G_pixel_values = layer_images_G[y,x,is_non_noise_pixels]
            B_pixel_values = layer_images_B[y,x,is_non_noise_pixels]

            # Average the pixel values
            divide_value = R_pixel_values.size
            if divide_value != 0:
                R_avg_pixel_value = round( np.sum( R_pixel_values ) / R_pixel_values.size )
                G_avg_pixel_value = round( np.sum( G_pixel_values ) / G_pixel_values.size )
                B_avg_pixel_value = round( np.sum( B_pixel_values ) / B_pixel_values.size )
            else:
                R_avg_pixel_value = 0
                G_avg_pixel_value = 0
                G_avg_pixel_value = 0

            if (x == 500 and y == 500) or (x == 750 and y == 750):
                print( "({}, {}) = ({}, {}, {})".format( x, y, R_avg_pixel_value, G_avg_pixel_value, B_avg_pixel_value ) )

            # Create output image
            layer_averaged_image[y,x,0] = R_avg_pixel_value
            layer_averaged_image[y,x,1] = G_avg_pixel_value
            layer_averaged_image[y,x,2] = B_avg_pixel_value
        # end for x
    # end for y
    print ("Done! ({} [sec])\n".format( round(time.time() - start , 2) ) )

    # Save the result image
    layer_averaged_image_BGR = cv2.cvtColor( layer_averaged_image, cv2.COLOR_RGB2BGR )
    cv2.imwrite( layer_images_path + "Layer_Averaged_Image_" + str( num_of_layers ) + ".png", layer_averaged_image_BGR )

if __name__ == "__main__":
    # Set the number of layer images
    num_of_layers = int( args[2] )
    print( "\nNumber of Layers: {}".format( num_of_layers ) )

    # Set image resolution
    image_resol = int( args[3] )
    print( "Image Resolution: {}".format( image_resol ) )

    # Read the target layer images
    layer_images_R    = create_empty_3d_array_float32( num_of_layers )
    layer_images_G    = create_empty_3d_array_float32( num_of_layers )
    layer_images_B    = create_empty_3d_array_float32( num_of_layers )
    layer_images_GRAY = create_empty_3d_array_uint8( num_of_layers )
    layer_images_path = args[1] + "/"
    read_layer_images()

    # Create the original image
    NUM_OF_REF_LAYER_IMAGES = 20
    print( "The number of layer images referenced to create the original image:" )
    print( " NUM_OF_REF_LAYER_IMAGES = {}".format( NUM_OF_REF_LAYER_IMAGES ) )

    original_image = create_original_image()
    # original_image_BGR = cv2.cvtColor( original_image, cv2.COLOR_RGB2BGR )
    cv2.imwrite( layer_images_path + "Original_Image_" + str( NUM_OF_REF_LAYER_IMAGES ) + ".png", original_image )

    # Average the layer images
    NOISE_THRESHOLD = 20
    print( "The value of the threshold for determining noise pixels:" )
    print( " NOISE_THRESHOLD = {}".format( NOISE_THRESHOLD ) )
    average_layer_images()