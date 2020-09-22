#version 120
#include "texture.h"

uniform float width; // screen width
uniform float height; // screen height
uniform vec3 background_color;
uniform sampler2D color_buffer_of_each_layer;

void main()
{
    gl_FragColor = texture2D( color_buffer_of_each_layer, gl_TexCoord[0].xy );
}