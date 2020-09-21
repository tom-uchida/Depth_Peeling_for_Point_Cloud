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
        kvs::glut::Screen::paintEvent();

        // Draw the color buffer of each layer

        // Get the depth peeling renderer
        kvs::RendererBase* tmp_rb = scene()->rendererManager()->renderer( "Depth-Peeling-Rendering" );
        local::DepthPeelingRenderer* dp_renderer = local::DepthPeelingRenderer::DownCast( tmp_rb );

        // Get the color buffer of each layer
        std::vector<kvs::Texture2D> color_buffer_of_each_layer = dp_renderer->getColorBufferOfEachLayer();

        std::cout << "\nRendering the color buffer of each layer...\n";
        for ( size_t i = 0; i < color_buffer_of_each_layer.size(); i++ ) 
        {
            kvs::OpenGL::SetDrawBuffer( GL_COLOR_ATTACHMENT0 );
            kvs::OpenGL::SetClearColor( kvs::Vec4::Zero() );
            kvs::OpenGL::SetClearDepth( 0.0 );
            kvs::OpenGL::Clear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT );

            kvs::Texture::Binder tex0( color_buffer_of_each_layer[i], 0 );
            DrawRect();

            // Save the rendered image
            kvs::ColorImage snapshot_image;
            snapshot_image = scene()->camera()->snapshot();
            std::string file_name( "IMAGE_DATA/LAYER_IMAGES/Layer" );
            char three_digits_num[5];
            sprintf( three_digits_num, "%03d", i );
            file_name += three_digits_num;
            file_name += ".bmp";
            snapshot_image.write( file_name );
        }

        // exit(0);
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