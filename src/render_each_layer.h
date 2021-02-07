/*****************************************************************************/
/**
 *  @file   render_each_layer.h
 *  @author Tomomasa Uchida
 */
/*****************************************************************************/
#pragma once

#include <kvs/OpenGL>
#include "GLdef.h"

#include "depth_peeling_renderer.h"
#include <kvs/ColorImage>
#include <time.h>

#include <kvs/Label>
#include <kvs/Font>
#include <kvs/FontMetrics>

// #define DRAW_LABEL

namespace local
{

class Screen : public kvs::Screen
{
private:
    kvs::Label  m_label;
    kvs::Font   m_font;

public:
    Screen( kvs::glut::Application* _app ):
        kvs::Screen( _app ),
        m_label( this )
    {
#ifdef DRAW_LABEL
        const int screen_width  = this->width();
        const int screen_height = this->height();
        m_label.setX( screen_width  * 0.3f );
        m_label.setY( screen_height * 0.2f );
        // m_label.setBackgroundColor( kvs::UIColor::Fill() );

        m_font.setFamilyToSans();
        m_font.setStyleToBold();
        // m_font.setEnabledShadow( true );
        // m_font.setShadowDistance( 5.0f );
        // m_font.setShadowBlur( 3.0f );
        m_font.setSize( screen_width * 0.1f );
        m_font.setColor( kvs::RGBColor::White() );
#endif
    };

    void paintEvent( void )
    {
        // Get the depth peeling renderer
        kvs::RendererBase* tmp_rb = scene()->rendererManager()->renderer( "Depth-Peeling-Rendering" );
        local::DepthPeelingRenderer* dp_renderer = local::DepthPeelingRenderer::DownCast( tmp_rb );

        // Get the layer level
        const size_t layer_level = dp_renderer->getLayerLevel();

        // Execute "Depth Peeling"
        const clock_t start = clock();
        std::cout << "\nExecuting Depth Peeling \"" << layer_level << "\" times...\n";
        for ( size_t i = 0; i < layer_level; i++ ) 
        {
            const size_t current_layer_level = i + 1;

            // Set the current layer level
            dp_renderer->setLayerLevel( current_layer_level );

#ifdef DRAW_LABEL
            // Draw label
            drawLabel( current_layer_level );
#endif

            // Rendering
            kvs::glut::Screen::paintEvent();

            // Save the current layer image
            saveImage( current_layer_level );
        }

        const clock_t end = clock();
        std::cout << "Done! ( " << static_cast<double>( end - start ) / CLOCKS_PER_SEC << " [sec] )\n";

        std::cout << "\nAutomatically, snapshotted.\n";
        std::cout << "Saved image path: IMAGE_DATA/OUTPUT_LAYER_IMAGES/LayerImageX.bmp\n";

        exit( 0 ); // Terminate the program normally
    } // end of paintEvent()

    inline void drawLabel( const size_t _current_layer_level )
    {
        std::stringstream ss;
        ss << _current_layer_level;
        m_label.setText( ( "Layer: " + ss.str() ).c_str() );

        m_label.setFont( m_font );
        // m_label.setMargin( 10 );
        m_label.show();
    } // end of drawLabel()

    inline void saveImage( const size_t _current_layer_level )
    {
        const kvs::ColorImage snapshot_image = scene()->camera()->snapshot();

        std::string file_name( "IMAGE_DATA/OUTPUT_LAYER_IMAGES/LayerImage" );
        // char three_digits_num[5];
        // sprintf( three_digits_num, "%03d", static_cast<int>( _current_layer_level ) );
        // file_name += three_digits_num;
        std::stringstream ss;
        ss << _current_layer_level;
        file_name += ss.str();
        file_name += ".bmp";

        snapshot_image.write( file_name );
    } // end of saveImage()

}; // end of Screen class

} // end of namespace local