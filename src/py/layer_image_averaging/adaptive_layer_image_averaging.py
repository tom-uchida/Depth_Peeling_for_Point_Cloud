# adaptive_layer_image_averaging.py
#   Tomomasa Uchida
#   2020/10/31

import numpy as np
import cv2
import time
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
if len(args) != 4:
    display_opening_message()
    print("\nUSAGE   : $ python {} [input_images_path] [num_of_layers] [image_resolution]".format(args[0]))
    print("EXAMPLE : $ python {} ../IMAGE_DATA 10 1000\n".format(args[0]))
    sys.exit()

def display_opening_message():
    print( "========================================" )
    print( "     Adaptive Layer Image Averaging" )
    print( "           Tomomasa Uchida" )
    print( "             2020/10/31" )
    print( "========================================" )

def create_empty_2d_array_uint8():
    return np.empty( ( image_resol, image_resol ), dtype=np.uint8 )

def create_empty_2d_array_uint16():
    return np.empty( ( image_resol, image_resol ), dtype=np.uint16 )

def create_empty_3d_array_uint8( _num_of_images ):
    return np.empty( ( image_resol, image_resol, _num_of_images ), dtype=np.uint8 )

def create_empty_3d_array_float32( _num_of_images ):
    return np.empty( ( image_resol, image_resol, _num_of_images ), dtype=np.float32 )

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
    median_image_RGB        = create_empty_3d_array_uint8( 3 )
    lim_of_num_of_layers    = NUM_OF_LAYER_IMAGES_USED_TO_CREATE_REF_IMAGE
    median_image_RGB[:,:,0] = np.median( layer_images_R[:,:,:lim_of_num_of_layers], axis=2 )
    median_image_RGB[:,:,1] = np.median( layer_images_G[:,:,:lim_of_num_of_layers], axis=2 )
    median_image_RGB[:,:,2] = np.median( layer_images_B[:,:,:lim_of_num_of_layers], axis=2 )

    return median_image_RGB

def calc_color_dist2( _target_pixel_RGB, _reference_pixel_RGB ):
    # In RGB color space, calc the euclidean distance
    r1, r2 = int( _target_pixel_RGB[0] ), int( _reference_pixel_RGB[0] )
    g1, g2 = int( _target_pixel_RGB[1] ), int( _reference_pixel_RGB[1] )
    b1, b2 = int( _target_pixel_RGB[2] ), int( _reference_pixel_RGB[2] )
    d2 = (r1-r2)**2 + (g1-g2)**2 + (b1-b2)**2
    # 255^2 * 3 = 195075
    # sqrt( 255^2 * 3) = 441.6729559300637

    return d2

def average_layer_images():
    # Pixel-wise layer image averaging
    target_pixel_values = np.zeros( ( num_of_layers, 3 ), dtype=np.uint8 )
    is_non_noise_pixels = np.empty( ( num_of_layers ), bool )
    # num_of_non_noise_pixels_image4viz = create_empty_2d_array_uint8()
    # mean_color_dist_image4viz = create_empty_2d_array_uint16()
    color_dist2s = np.zeros( num_of_layers )
    weights = np.zeros( num_of_layers, float )
    layer_averaged_image = create_empty_3d_array_uint8( 3 )
    counter = 0
    print( "")
    print( "** Now executing \"Adaptive Layer Image Averaging\"..." )
    start = time.time()
    for y in range( image_resol ):
        for x in range( image_resol ):

            # Calc the color distance b/w the target pixel and the reference pixel
            for layer in range( num_of_layers ):
                # Get the target pixel value
                target_pixel_values[layer,0] = layer_images_R[y,x,layer]
                target_pixel_values[layer,1] = layer_images_G[y,x,layer]
                target_pixel_values[layer,2] = layer_images_B[y,x,layer]

                color_dist2s[layer] = calc_color_dist2( target_pixel_values[layer,:], reference_image_RGB[y,x,:] )
            # end for layer

            # Calc the max of color distances
            color_dists = np.sqrt( color_dist2s ) 
            # color_dists = [round( i ) for i in color_dists]
            d_max = np.max( color_dists )

            # If all the pixels are background color
            if d_max == 0:
                layer_averaged_image[y,x,:] = 0
                continue # for speeding up

            # Convert color distance to weight
            for layer in range( num_of_layers ):
                weights[layer] = num_of_layers * ( 1.0 - color_dists[layer] / d_max )
            # end for layer

            if np.sum( weights ) == 0:
                layer_averaged_image[y,x,:] = 0
                counter += 1
                continue # for speeding up

            # Calc the sum of the pixel value
            sum_of_pixel_values = np.zeros( 3, float )
            for layer in range( num_of_layers ):
                sum_of_pixel_values += target_pixel_values[layer,:] * weights[layer]
            # end for layer

            # Calc weighted average
            weighted_avg_pixel_value = np.divide( sum_of_pixel_values, np.sum( weights ) )

            # Save the final pixel value to the output image
            layer_averaged_image[y,x,0] = weighted_avg_pixel_value[0]
            layer_averaged_image[y,x,1] = weighted_avg_pixel_value[1]
            layer_averaged_image[y,x,2] = weighted_avg_pixel_value[2]

        # end for x
    # end for y
    print( "**  Done! ( {} [sec] )\n".format( round(time.time() - start , 2) ) )
    print( "counter: {}".format( counter ) )

    # Save the layer averaged image
    layer_averaged_image_BGR = cv2.cvtColor( layer_averaged_image, cv2.COLOR_RGB2BGR )
    output_image_name = layer_images_path + "adaptive_layer_averaged_image_" + str( num_of_layers ) + ".png"
    cv2.imwrite( output_image_name, layer_averaged_image_BGR )
    print( "** Saved the adaptive layer averaged image." )
    print( "**  PATH: {}\n".format( output_image_name ) )

    # Save the figures for visualization
    # save_figure_for_viz( num_of_non_noise_pixels_image4viz, mean_color_dist_image4viz )
# End of average_layer_images()

# def save_figure_for_viz( _image4viz1, _image4viz2 ):
#     fig = plt.figure( figsize=(12, 5) ) # figsize=(width, height)
#     gs  = gridspec.GridSpec(1, 2)

#     from mpl_toolkits.axes_grid1 import make_axes_locatable
#     ax1 = fig.add_subplot( gs[0, 0] )
#     ax1.set_title( "Num. of pixels used for averaging (pixel-wise)", fontsize=12 )
#     img1 = ax1.imshow( _image4viz1, clim=[0, num_of_layers], cmap='viridis' )
#     ax1.axis( "image" ), ax1.axis( 'off' )
#     ax1_cb = make_axes_locatable( ax1 ).new_horizontal( size="4.5%", pad=0.2 )
#     fig.add_axes( ax1_cb )
#     plt.colorbar( img1, cax=ax1_cb )

#     # _image4viz2 = np.sqrt( _image4viz2 )
#     ax2 = fig.add_subplot( gs[0, 1] )
#     ax2.set_title( 'Mean color distance (pixel-wise)', fontsize=12 )
#     img2 = ax2.imshow( _image4viz2, clim=[0, np.max( _image4viz2 )], cmap='viridis' )
#     ax2.axis( "image" ), ax2.axis( 'off' )
#     ax2_cb = make_axes_locatable( ax2 ).new_horizontal( size="4.5%", pad=0.2 )
#     fig.add_axes( ax2_cb )
#     plt.colorbar( img2, cax=ax2_cb )

#     # Save the figure
#     plt.savefig( layer_images_path + "figure.png" )
#     print( "** Saved the figure." )
#     print( "**  PATH: {}\n".format( layer_images_path + "figure.png" ) )

if __name__ == "__main__":
    display_opening_message()

    # Set the number of layer images
    num_of_layers = int( args[2] )
    print( "" )
    print( "** Num. of layer images: {}".format( num_of_layers ) )

    # Set image resolution
    image_resol = int( args[3] )
    print( "** Image resolution    : {}".format( image_resol ) )

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
    print( "** Num. of layer images used to create the reference image:" )
    print( "**  NUM_OF_LAYER_IMAGES_USED_TO_CREATE_REF_IMAGE = {}".format( NUM_OF_LAYER_IMAGES_USED_TO_CREATE_REF_IMAGE ) )
    reference_image_RGB = create_reference_image()
    reference_image_BGR = cv2.cvtColor( reference_image_RGB, cv2.COLOR_RGB2BGR )
    cv2.imwrite( layer_images_path + "Reference_Image_" + str( NUM_OF_LAYER_IMAGES_USED_TO_CREATE_REF_IMAGE ) + ".png", reference_image_BGR )

    # Average the layer images
    # COLOR_DISTANCE_THRESHOLD_FOR_NOISE = 100
    # print( "" )
    # print( "** The value of the threshold for determining noise pixels:" )
    # print( "**  COLOR_DISTANCE_THRESHOLD_FOR_NOISE = {}".format( COLOR_DISTANCE_THRESHOLD_FOR_NOISE ) )
    average_layer_images()