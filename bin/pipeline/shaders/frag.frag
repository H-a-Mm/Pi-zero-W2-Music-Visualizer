#version 330

uniform sampler2D tex;

uniform float uTime;
uniform float uScrollSpeed;

uniform vec3 uDarkColor;
uniform vec3 uLightColor;

in vec2 v_uv;

out vec4 frag_color;

void main()
{
    vec2 p = v_uv;
    
    p.x += uTime * uScrollSpeed;
    float n =
          sin(p.x * 4.0 + uTime * 0.40)
        + sin(p.y * 3.0 + uTime * 0.30)
        + sin((p.x + p.y) * 5.0 + uTime * 0.20)
        + sin(length(p - vec2(
                0.5 + 0.2 * sin(uTime * 0.15),
                0.5 + 0.2 * cos(uTime * 0.12)
            )) * 12.0);
    
    n /= 4.0;
    
    n = n * 0.5 + 0.5;
    
    n = smoothstep(0.25, 0.85, n);
    n = pow(n, 1.8);
    
    vec3 bgColor = mix(uDarkColor, uLightColor, n);
    frag_color = vec4(bgColor, 1.0);
}