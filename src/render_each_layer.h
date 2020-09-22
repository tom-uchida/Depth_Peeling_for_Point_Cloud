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

        std::cout << "\nDoing Depth Peeling " << layer_level << " times..." << std::endl;
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

        std::cout << "\nAutomatically, snapshotted." << std::endl;
        std::cout << "Saved image path: IMAGE_DATA/LAYER_IMAGES/LayerImageXXX.bmp" << std::endl;

        // Terminate the program normally
        exit(0);
    } // end of paintEvent()

    void DrawRect()
    {
        kvs::OpenGL::WithPushedMatrix p1( GL_MODELVIEW );
        p1.loadIdentity();
        {
            kvs::OpenGL::WithPushedMatrix p2( GL_PROJECTION );
            p2.loadIdentity();
            {
                kvs::OpenGL::SetOrtho( 0, 1, 0, 1, -1, 1 );
                kvs::OpenGL::Begin( GL_QUADS );
                kvs::OpenGL::TexCoordVertex( kvs::Vec2( 1, 1 ), kvs::Vec2( 1, 1 ) );
                kvs::OpenGL::TexCoordVertex( kvs::Vec2( 0, 1 ), kvs::Vec2( 0, 1 ) );
                kvs::OpenGL::TexCoordVertex( kvs::Vec2( 0, 0 ), kvs::Vec2( 0, 0 ) );
                kvs::OpenGL::TexCoordVertex( kvs::Vec2( 1, 0 ), kvs::Vec2( 1, 0 ) );
                kvs::OpenGL::End();
            }
        }
    }

}; // end of Screen class

} // end of namespace local