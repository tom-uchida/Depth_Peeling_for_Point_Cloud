# adaptive_layer_image_averaging.py
#   Tomomasa Uchida
#   2020/11/01

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
    print("\nUSAGE   : $ python {} [input_images_path] [num_of_layers] [image_resolution]".format(args[0]))
    print("EXAMPLE : $ python {} ../IMAGE_DATA 10 1000\n".format(args[0]))
    sys.exit()

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

def create_reference_image():
    median_image_RGB        = create_empty_3d_array_uint8( 3 )
    lim_of_num_of_layers    = NUM_OF_LAYER_IMAGES_USED_TO_CREATE_REF_IMAGE
    median_image_RGB[:,:,0] = np.median( layer_images_R[:,:,:lim_of_num_of_layers], axis=2 )
    median_image_RGB[:,:,1] = np.median( layer_images_G[:,:,:lim_of_num_of_layers], axis=2 )
    median_image_RGB[:,:,2] = np.median( layer_images_B[:,:,:lim_of_num_of_layers], axis=2 )

    return median_image_RGB

def is_this_pixel_non_noise( _target_pixel_RGB, _reference_image_RGB ):
    # In RGB color space, calc the euclidean distance
    r1, r2 = _target_pixel_RGB[0], _reference_image_RGB[0]
    g1, g2 = _target_pixel_RGB[1], _reference_image_RGB[1]
    b1, b2 = _target_pixel_RGB[2], _reference_image_RGB[2]
    color_dist2 = (r1-r2)**2 + (g1-g2)**2 + (b1-b2)**2
    
    is_non_noise_pixel = True
    if color_dist2 >= COLOR_DISTANCE_THRESHOLD_FOR_NOISE**2:
        is_non_noise_pixel = False

    return is_non_noise_pixel, color_dist2

def average_layer_images():
    # Pixel-wise layer image averaging
    target_pixel_RGB     = np.empty( 3, int )
    is_non_noise_pixels  = np.empty( num_of_layers, bool )
    num_of_non_noise_pixels_image4viz = create_empty_2d_array_uint8()
    mean_color_dist2_image4viz = create_empty_2d_array_uint16()
    color_dist2s = np.empty( num_of_layers, int )
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
                is_non_noise_pixel, color_dist2 = is_this_pixel_non_noise( target_pixel_RGB, reference_image_RGB[y,x,:] )
                if is_non_noise_pixel == True:
                    is_non_noise_pixels[layer] = True   # non-noise pixel
                else:
                    is_non_noise_pixels[layer] = False  # noise pixel
                # end if

                # Save the color distance
                color_dist2s[layer] = color_dist2
            # end for layer

            # Calc the mean of color distance
            mean_color_dist2_image4viz[y,x] = np.mean( color_dist2s )

            # Exclude noise pixels and get only non-noise pixels
            R_non_noise_pixels = layer_images_R[y,x,is_non_noise_pixels]
            G_non_noise_pixels = layer_images_G[y,x,is_non_noise_pixels]
            B_non_noise_pixels = layer_images_B[y,x,is_non_noise_pixels]

            # If all the pixels are background color
            num_of_R_zero = R_non_noise_pixels.size - np.count_nonzero( R_non_noise_pixels )
            num_of_G_zero = G_non_noise_pixels.size - np.count_nonzero( G_non_noise_pixels )
            num_of_B_zero = B_non_noise_pixels.size - np.count_nonzero( B_non_noise_pixels )
            if num_of_R_zero == num_of_G_zero == num_of_B_zero == num_of_layers:
                num_of_non_noise_pixels_image4viz[y,x] = num_of_layers
                layer_averaged_image[y,x,:] = 0
                continue # for speeding up

            # Weighted averaging for only non-noise pixels
            num_of_non_noise_pixels = np.count_nonzero( is_non_noise_pixels )
            num_of_non_noise_pixels_image4viz[y,x] = num_of_non_noise_pixels
            sum_of_weights = 0
            sum_R, sum_G, sum_B = 0, 0, 0
            for i in range( num_of_non_noise_pixels ):
                weight = num_of_non_noise_pixels - i
                sum_of_weights += weight

                sum_R += R_non_noise_pixels[i] * weight
                sum_G += G_non_noise_pixels[i] * weight
                sum_B += B_non_noise_pixels[i] * weight
            # end for

            # Create output image
            if not sum_of_weights == 0:
                layer_averaged_image[y,x,0] = sum_R / sum_of_weights
                layer_averaged_image[y,x,1] = sum_G / sum_of_weights
                layer_averaged_image[y,x,2] = sum_B / sum_of_weights
            else:
                layer_averaged_image[y,x,:] = 0

        # end for x
    # end for y
    print ("**  Done! ( {} [sec] )\n".format( round( time.time() - start , 2 ) ) )

    # Save the layer averaged image
    layer_averaged_image_BGR = cv2.cvtColor( layer_averaged_image, cv2.COLOR_RGB2BGR )
    output_image_name = layer_images_path + "adaptive_layer_averaged_image_" + str( num_of_layers ) + ".png"
    cv2.imwrite( output_image_name, layer_averaged_image_BGR )
    print( "** Saved the adaptive layer averaged image." )
    print( "**  PATH: {}\n".format( output_image_name ) )

    # Save the figures for visualization
    save_figure_for_viz( num_of_non_noise_pixels_image4viz, mean_color_dist2_image4viz )
# End of average_layer_images()

def save_figure_for_viz( _image4viz1, _image4viz2 ):
    fig = plt.figure( figsize=(12, 5) ) # figsize=(width, height)
    gs  = gridspec.GridSpec(1, 2)

    from mpl_toolkits.axes_grid1 import make_axes_locatable
    ax1 = fig.add_subplot( gs[0, 0] )
    ax1.set_title( "Num. of pixels used for averaging (pixel-wise)", fontsize=12 )
    img1 = ax1.imshow( _image4viz1, clim=[0, num_of_layers], cmap='viridis' )
    ax1.axis( "image" ), ax1.axis( 'off' )
    ax1_cb = make_axes_locatable( ax1 ).new_horizontal( size="4.5%", pad=0.2 )
    fig.add_axes( ax1_cb )
    plt.colorbar( img1, cax=ax1_cb )

    _image4viz2 = np.sqrt( _image4viz2 )
    ax2 = fig.add_subplot( gs[0, 1] )
    ax2.set_title( 'Mean color distance (pixel-wise)', fontsize=12 )
    img2 = ax2.imshow( _image4viz2, clim=[0, np.max( _image4viz2 )], cmap='viridis' )
    ax2.axis( "image" ), ax2.axis( 'off' )
    ax2_cb = make_axes_locatable( ax2 ).new_horizontal( size="4.5%", pad=0.2 )
    fig.add_axes( ax2_cb )
    plt.colorbar( img2, cax=ax2_cb )

    # Save the figure
    plt.savefig( layer_images_path + "figure.png" )
    print( "** Saved the figure." )
    print( "**  PATH: {}\n".format( layer_images_path + "figure.png" ) )

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
    NUM_OF_LAYER_IMAGES_USED_TO_CREATE_REF_IMAGE = min( 5, num_of_layers )
    print( "" )
    print( "** The number of layer images used to create the reference image:" )
    print( "**  NUM_OF_LAYER_IMAGES_USED_TO_CREATE_REF_IMAGE = {}".format( NUM_OF_LAYER_IMAGES_USED_TO_CREATE_REF_IMAGE ) )
    reference_image_RGB = create_reference_image()
    reference_image_BGR = cv2.cvtColor( reference_image_RGB, cv2.COLOR_RGB2BGR )
    cv2.imwrite( layer_images_path + "Reference_Image_" + str( NUM_OF_LAYER_IMAGES_USED_TO_CREATE_REF_IMAGE ) + ".png", reference_image_BGR )

    # Average the layer images
    COLOR_DISTANCE_THRESHOLD_FOR_NOISE = 100
    print( "" )
    print( "** The value of the threshold for determining noise pixels:" )
    print( "**  COLOR_DISTANCE_THRESHOLD_FOR_NOISE = {}".format( COLOR_DISTANCE_THRESHOLD_FOR_NOISE ) )
    average_layer_images()