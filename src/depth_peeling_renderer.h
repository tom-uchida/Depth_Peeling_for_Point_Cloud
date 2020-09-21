#pragma once
#include <kvs/Module>
#include <kvs/ProgramObject>
#include <kvs/VertexBufferObject>
#include <kvs/IndexBufferObject>
#include <kvs/FrameBufferObject>
#include <kvs/Texture2D>
#include <kvs/PolygonObject>
#include <kvs/PolygonRenderer>

#include <kvs/ParticleBasedRenderer>
#include <kvs/PointObject>
#include <kvs/PointRenderer>

namespace kvs
{
class ObjectBase;
class Camera;
class Light;
}

namespace local
{

class DepthPeelingRenderer : public kvs::glsl::ParticleBasedRenderer
{
    kvsModule( local::DepthPeelingRenderer, Renderer );
    kvsModuleBaseClass( kvs::glsl::ParticleBasedRenderer );

private:
    size_t m_width; ///< window width
    size_t m_height; ///< window height
    const kvs::ObjectBase* m_object; ///< pointer to the rendering object
    kvs::Shader::ShadingModel* m_shader; ///< shading method

    kvs::VertexBufferObject m_vbo; ///< vertex buffer object
    kvs::IndexBufferObject m_ibo; ///< index buffer object

    int m_cycle;
    size_t m_layer_level;
    kvs::RGBColor m_background_color;

    kvs::ProgramObject m_peeling_shader; ///< shader program for depth peeling
    kvs::ProgramObject m_blending_shader; ///< shader program for blending
    kvs::ProgramObject m_finalizing_shader; ///< shader program for finalizing

    kvs::FrameBufferObject m_framebuffer[3];
    kvs::Texture2D m_color_buffer[3];
    kvs::Texture2D m_depth_buffer[3];
    std::vector<kvs::Texture2D> m_color_buffer_of_each_layer;

public:
    DepthPeelingRenderer();
    ~DepthPeelingRenderer();

    void exec( kvs::ObjectBase* object, kvs::Camera* camera, kvs::Light* light );

    template <typename ShadingType>
    void setShader( const ShadingType shader );

    void setLayerLevel( const size_t _nlayers ) { m_layer_level = _nlayers; }
    void setBackgroundColor( const kvs::RGBColor& _color ) { m_background_color = _color; }

    size_t getLayerLevel() const { return m_layer_level; }
    std::vector<kvs::Texture2D> getColorBuffers() const { return m_color_buffer_of_each_layer; }

private:
    void create_shader_program();
    void create_vbo( const kvs::PointObject* _point_object );
    void create_framebuffer( const size_t _width, const size_t _height );
    void update_framebuffer( const size_t _width, const size_t _height );
    
    void create_color_buffers_for_each_layer( const size_t _width, const size_t _height );
    void initialize_pass();
    void finalize_pass();
    void peel_pass( const kvs::PointObject* _point_object, const size_t _index );
    void draw( const kvs::PointObject* _point_object );
    void blend();
};

template <typename ShadingType>
inline void DepthPeelingRenderer::setShader( const ShadingType shader )
{
    if ( m_shader )
    {
        delete m_shader;
        m_shader = NULL;
    }

    m_shader = new ShadingType( shader );
    if ( !m_shader )
    {
        kvsMessageError("Cannot create a specified shader.");
    }
};

} // end of namespace local
