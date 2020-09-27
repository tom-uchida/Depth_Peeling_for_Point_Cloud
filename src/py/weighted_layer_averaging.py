# weighted_layer_averaging.py
#   Tomomasa Uchida
#   2020/09/27

import numpy as np
import cv2

# Check arguments
import sys
args = sys.argv
if len(args) != 4:
    print("\nUSAGE   : $ python weighted_layer_averaging.py [input_images_path] [num_of_layers] [image_resolution]")
    print("EXAMPLE : $ python weighted_layer_averaging.py ../IMAGE_DATA 10 1000\n")
    sys.exit()



def ReadImage( _img_name ):
    # read input image
    img_BGR = cv2.imread(_img_name)

    # convert color BGR to RGB
    img_RGB = cv2.cvtColor(img_BGR, cv2.COLOR_BGR2RGB)

    return img_RGB



def run( _num_of_layers, _image_resol, _serial_img_path ):
    # Prepare empty numpy array
    R_pixel_values = np.empty( (_image_resol*1, _image_resol*1, _num_of_layers), dtype=np.float32 )
    G_pixel_values = np.empty( (_image_resol*1, _image_resol*1, _num_of_layers), dtype=np.float32 )
    B_pixel_values = np.empty( (_image_resol*1, _image_resol*1, _num_of_layers), dtype=np.float32 )

    # Read intermediate images
    for i in range( _num_of_layers ):
        # Read each ensemble image
        tmp_image_RGB = ReadImage( _serial_img_path + "LayerLevel"+str(i+1)+".bmp" )

        # Split into RGB and add to numpy array
        R_pixel_values[:,:,i] = tmp_image_RGB[:,:,0] # R
        G_pixel_values[:,:,i] = tmp_image_RGB[:,:,1] # G
        B_pixel_values[:,:,i] = tmp_image_RGB[:,:,2] # B

        if i == _num_of_layers-1:
            print("R: ", R_pixel_values.shape)
            print("G: ", G_pixel_values.shape)
            print("B: ", B_pixel_values.shape)
    # end for i


    # Prepare empty numpy array
    sum_R = np.empty( (_image_resol*1, _image_resol*1), dtype=np.float32 )
    sum_G = np.empty( (_image_resol*1, _image_resol*1), dtype=np.float32 )
    sum_B = np.empty( (_image_resol*1, _image_resol*1), dtype=np.float32 )

    # Calc weighted average
    weight = [0] * _num_of_layers
    for i in range( _num_of_layers ):
        weight[i] = _num_of_layers - i
        # print( "weight[{}]: {}".format(i, weight[i]) )

        sum_R[:,:] += R_pixel_values[:,:,i] * weight[i]
        sum_G[:,:] += G_pixel_values[:,:,i] * weight[i]
        sum_B[:,:] += B_pixel_values[:,:,i] * weight[i]
    # end for i

    sum_of_weight = np.sum( weight )
    print("sum_of_weight: {}".format(sum_of_weight))
    weighted_averaged_R = sum_R / sum_of_weight
    weighted_averaged_G = sum_G / sum_of_weight
    weighted_averaged_B = sum_B / sum_of_weight
    # print( "weighted_averaged_R: {}".format(weighted_averaged_R[:10, :10, 0]) )

    # Convert float32 to uint8
    weighted_averaged_R = weighted_averaged_R.astype(np.uint8)
    weighted_averaged_G = weighted_averaged_G.astype(np.uint8)
    weighted_averaged_B = weighted_averaged_B.astype(np.uint8)

    # Combine R, G and B arrays
    # (3, 1000, 1000) → (1000, 1000, 3)
    # (0,    1,    2) → (   1,    2, 0)
    weighted_averaged_RGB = np.array([weighted_averaged_R, weighted_averaged_G, weighted_averaged_B]).transpose((1, 2, 0))
    
    # Save the result image
    weighted_averaged_BGR = cv2.cvtColor(weighted_averaged_RGB, cv2.COLOR_RGB2BGR)
    cv2.imwrite("./Weighted_Layer_Averaging.png", weighted_averaged_BGR)



if __name__ == "__main__":
    # Set the number of layers
    num_of_layers = int(args[2])
    print("Number of Layers :", num_of_layers)

    # Set image resolution
    image_resol = int(args[3])
    print("Image Resolution :", image_resol)

    # Read target images
    layer_img_path = args[1] + "/"
    run( num_of_layers, image_resol, layer_img_path )