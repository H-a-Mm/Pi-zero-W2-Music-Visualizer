#version 100

attribute vec2 in_pos;
attribute vec2 in_uv;

varying vec2 v_uv;

void main()
{
    v_uv = in_uv;
    gl_Position = vec4(in_pos, 0.0, 1.0);
}