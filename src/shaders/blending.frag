#version 120
#include "texture.h"

uniform float width; // screen width
uniform float height; // screen height
uniform sampler2D color_front;
uniform sampler2D depth_back;
uniform sampler2D color_back;

void main()
{
    vec2 index = gl_FragCoord.xy / vec2( width, height );
    vec4 front_color = LookupTexture2D( color_front, index );
    vec4 back_color = LookupTexture2D( color_back, index );

    vec3 color = front_color.rgb + back_color.rgb;
    gl_FragColor = vec4( color, 1.0 );
    gl_FragDepth = LookupTexture2D( depth_back, index ).r;
}
