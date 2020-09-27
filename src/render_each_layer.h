/*****************************************************************************/
/**
 *  @file   render_each_layer.h
 *  @author Tomomasa Uchida
 */
/*****************************************************************************/
#pragma once

#include <kvs/OpenGL>
#include "GLdef.h"

// #include <kvs/rendererManager>
#include "depth_peeling_renderer.h"
#include <kvs/ColorImage>
#include <time.h>

namespace local
{

class Screen : public kvs::glut::Screen
{

private:

public:
    Screen( kvs::glut::Application* _application ):
        kvs::glut::Screen( _application )
    {};

    void paintEvent( void )
    {
        // Get the depth peeling renderer
        kvs::RendererBase* tmp_rb = scene()->rendererManager()->renderer( "Depth-Peeling-Rendering" );
        local::DepthPeelingRenderer* dp_renderer = local::DepthPeelingRenderer::DownCast( tmp_rb );

        // Get the layer level
        const size_t layer_level = dp_renderer->getLayerLevel();

        const clock_t start = clock();
        std::cout << "\nDoing Depth Peeling " << layer_level << " times...\n";
        for ( size_t i = 0; i < layer_level; i++ ) 
        {
            // Change the layer level
            dp_renderer->setLayerLevel( i+1 );

            // Rendering
            kvs::glut::Screen::paintEvent();

            // Save the current layer image
            kvs::ColorImage snapshot_image = scene()->camera()->snapshot();
            std::string file_name( "IMAGE_DATA/LAYER_IMAGES/LayerImage" );
            char three_digits_num[5];
            sprintf( three_digits_num, "%03d", i );
            file_name += three_digits_num;
            file_name += ".bmp";
            snapshot_image.write( file_name );
        }

        const clock_t end = clock();
        std::cout << "Done! ( " << static_cast<double>(end - start) / CLOCKS_PER_SEC << " [sec] )\n";

        std::cout << "\nAutomatically, snapshotted.\n";
        std::cout << "Saved image path: IMAGE_DATA/LAYER_IMAGES/LayerImageXXX.bmp\n";

        exit(0); // Terminate the program normally
    } // end of paintEvent()

}; // end of Screen class

} // end of namespace local