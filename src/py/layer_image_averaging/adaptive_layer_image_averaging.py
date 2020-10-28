# noise_robust_layer_image_averaging.py
#   Tomomasa Uchida
#   2020/10/25

import numpy as np
import cv2
import time
from matplotlib import pyplot as plt

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
    # end for layer
# End read_layer_images()

def create_reference_image():
    # median_image_GRAY = create_empty_2d_array_uint8()
    # median_image_GRAY = np.median( layer_images_GRAY[:,:,:NUM_OF_LAYER_IMAGES_USED_TO_CREATE_REF_IMAGE], axis=2 )

    median_image_RGB        = create_empty_3d_array_uint8( 3 )
    lim_of_num_of_layers    = NUM_OF_LAYER_IMAGES_USED_TO_CREATE_REF_IMAGE
    median_image_RGB[:,:,0] = np.median( layer_images_R[:,:,:lim_of_num_of_layers], axis=2 )
    median_image_RGB[:,:,1] = np.median( layer_images_G[:,:,:lim_of_num_of_layers], axis=2 )
    median_image_RGB[:,:,2] = np.median( layer_images_B[:,:,:lim_of_num_of_layers], axis=2 )

    return median_image_RGB

def is_this_pixel_noise( _target_pixel_RGB, _reference_image_RGB ):
    is_noise_pixel = False

    # # Convert RGB to GRAY
    # grayscale = 0.299*_target_pixel_RGB[0] + 0.587*_target_pixel_RGB[1] + 0.114*_target_pixel_RGB[2]

    # In RGB color space, calc the euclidean distance
    r1, r2 = _target_pixel_RGB[0], _reference_image_RGB[0]
    g1, g2 = _target_pixel_RGB[1], _reference_image_RGB[1]
    b1, b2 = _target_pixel_RGB[2], _reference_image_RGB[2]
    color_distance2 = (r1-r2)**2 + (g1-g2)**2 + (b1-b2)**2

    if color_distance2 >= COLOR_DISTANCE_THRESHOLD_FOR_NOISE**2:
        is_noise_pixel = True

    return is_noise_pixel

def average_layer_images():
    # Pixel-wise layer image averaging
    target_pixel_RGB           = [0, 0, 0]
    is_non_noise_pixels  = np.empty( ( num_of_layers ), bool )
    num_of_non_noise_pixels_image = create_empty_2d_array_uint8()
    layer_averaged_image = create_empty_3d_array_uint8( 3 )
    print( "")
    print( "** Now creating the layer-averaged image..." )
    start = time.time()
    for y in range( image_resol ):
        for x in range( image_resol ):

            for layer in range( num_of_layers ):
                # Get the target pixel value
                target_pixel_RGB[0] = layer_images_R[y,x,layer]
                target_pixel_RGB[1] = layer_images_G[y,x,layer]
                target_pixel_RGB[2] = layer_images_B[y,x,layer]

                # Check if the pixel is noise pixel
                if is_this_pixel_noise( target_pixel_RGB, reference_image_RGB[y,x,:] ) == False:
                    is_non_noise_pixels[layer] = True
                else:
                    is_non_noise_pixels[layer] = False
                # end if
            # end for layer

            # Get only non-noise pixels
            R_pixel_values = layer_images_R[y,x,is_non_noise_pixels]
            G_pixel_values = layer_images_G[y,x,is_non_noise_pixels]
            B_pixel_values = layer_images_B[y,x,is_non_noise_pixels]

            # If all the pixels are background color
            num_of_bg_color_R = R_pixel_values.size - np.count_nonzero( R_pixel_values )
            num_of_bg_color_G = G_pixel_values.size - np.count_nonzero( G_pixel_values )
            num_of_bg_color_B = B_pixel_values.size - np.count_nonzero( B_pixel_values )
            if num_of_bg_color_R == num_of_bg_color_G == num_of_bg_color_B == num_of_layers:
                num_of_non_noise_pixels_image[y,x] = num_of_layers
                layer_averaged_image[y,x,:] = 0
                continue

            # Average the pixel values
            num_of_non_noise_pixels = np.count_nonzero( is_non_noise_pixels )
            num_of_non_noise_pixels_image[y,x] = num_of_non_noise_pixels
            if num_of_non_noise_pixels != 0:
                R_avg_pixel_value = round( np.sum( R_pixel_values ) / R_pixel_values.size )
                G_avg_pixel_value = round( np.sum( G_pixel_values ) / G_pixel_values.size )
                B_avg_pixel_value = round( np.sum( B_pixel_values ) / B_pixel_values.size )
            else:
                R_avg_pixel_value, G_avg_pixel_value, B_avg_pixel_value = 0, 0, 0

            # Create output image
            layer_averaged_image[y,x,0] = R_avg_pixel_value
            layer_averaged_image[y,x,1] = G_avg_pixel_value
            layer_averaged_image[y,x,2] = B_avg_pixel_value

        # end for x
    # end for y
    print ("** Done! ( {} [sec] )\n".format( round(time.time() - start , 2) ) )

    # Save the image
    # cv2.imwrite( layer_images_path + "Num_of_Non_Noise_Pixels_Image.png", num_of_non_noise_pixels_image )
    plt.figure( figsize=(10, 10) )
    plt.title( "The pixel-wise number of pixels used for averaging", fontsize=18 )
    plt.imshow( num_of_non_noise_pixels_image, clim=[0, num_of_layers], cmap='viridis' )
    plt.colorbar()
    # plt.xticks([]), plt.yticks([])
    plt.savefig( layer_images_path + "Num_of_Non_Noise_Pixels_Image.png" )

    # Save the layer averaged image
    layer_averaged_image_BGR = cv2.cvtColor( layer_averaged_image, cv2.COLOR_RGB2BGR )
    cv2.imwrite( layer_images_path + "Layer_Averaged_Image_" + str( num_of_layers ) + ".png", layer_averaged_image_BGR )

if __name__ == "__main__":
    # Set the number of layer images
    num_of_layers = int( args[2] )
    print( "" )
    print( "** Number of Layers: {}".format( num_of_layers ) )

    # Set image resolution
    image_resol = int( args[3] )
    print( "** Image Resolution: {}".format( image_resol ) )

    # Read the target layer images
    layer_images_R    = create_empty_3d_array_float32( num_of_layers )
    layer_images_G    = create_empty_3d_array_float32( num_of_layers )
    layer_images_B    = create_empty_3d_array_float32( num_of_layers )
    layer_images_GRAY = create_empty_3d_array_uint8( num_of_layers )
    layer_images_path = args[1] + "/"
    read_layer_images()

    # Create the reference image
    NUM_OF_LAYER_IMAGES_USED_TO_CREATE_REF_IMAGE = min( 10, num_of_layers )
    print( "" )
    print( "** The number of layer images used to create the reference image:" )
    print( "**  NUM_OF_LAYER_IMAGES_USED_TO_CREATE_REF_IMAGE = {}".format( NUM_OF_LAYER_IMAGES_USED_TO_CREATE_REF_IMAGE ) )
    reference_image_RGB = create_reference_image()
    reference_image_BGR = cv2.cvtColor( reference_image_RGB, cv2.COLOR_RGB2BGR )
    cv2.imwrite( layer_images_path + "Reference_Image_" + str( NUM_OF_LAYER_IMAGES_USED_TO_CREATE_REF_IMAGE ) + ".png", reference_image_BGR )

    # Average the layer images
    COLOR_DISTANCE_THRESHOLD_FOR_NOISE = 50
    print( "" )
    print( "** The value of the threshold for determining noise pixels:" )
    print( "**  COLOR_DISTANCE_THRESHOLD_FOR_NOISE = {}".format( COLOR_DISTANCE_THRESHOLD_FOR_NOISE ) )
    average_layer_images()