# Internal Libs
import os
import colorsys

# External Libs
import numpy as np
from pathlib import Path
import moderngl
from PIL import Image

# Local Modules

SHADER_PATH = "/shaders"

class Render:
    def __init__(self, ctx):
        self.ctx = ctx

        self.program = self.load_shaders()

        self.textures = {}

        self.colors = [
            [22, 22, 22],   # Black
            [0, 31, 73],    # Blue
            [159, 126, 49], # Yello
            [99, 5, 56],    # Pink
            [49, 2, 62]     # Purple
        ]

        self.color_index = 0
        self.color_t = 0.0

        self.vertices = np.array([
            -1.0, -1.0, 0.0, 0.0,
             1.0, -1.0, 1.0, 0.0,
            -1.0,  1.0, 0.0, 1.0,
             1.0,  1.0, 1.0, 1.0,
        ], dtype='f4')

        self.vbo = self.ctx.buffer(
            self.vertices.tobytes()
        )

        self.vao = self.ctx.vertex_array(
            self.program,
            [(self.vbo, '2f 2f', 'in_pos', 'in_uv')]
        )

        self.uTime = 1.0
        self.uScrollSpeed = 0.025
        self.uDarkColor = [5, 5, 5]
        self.uLightColor = self.colors[0]

    def cycle_col(self):
        self.color_t += 0.0002 # Time var
    
        if self.color_t >= 1.0:
            self.color_t = 0.0
            self.color_index = (self.color_index + 1) % len(self.colors)
    
        current = self.colors[self.color_index]
        target = self.colors[(self.color_index + 1) % len(self.colors)]
    
        t = self.color_t * self.color_t * (3.0 - 2.0 * self.color_t)
    
        self.uLightColor[0] = int(current[0] + (target[0] - current[0]) * t)
        self.uLightColor[1] = int(current[1] + (target[1] - current[1]) * t)
        self.uLightColor[2] = int(current[2] + (target[2] - current[2]) * t)
    
        self.uDarkColor[0] = max(0, self.uLightColor[0] - 20)
        self.uDarkColor[1] = max(0, self.uLightColor[1] - 20)
        self.uDarkColor[2] = max(0, self.uLightColor[2] - 20)

    # Load the shaders, works in windows and linux
    # Path is relitive for root (Above bin)
    def load_shaders(self):
        with open(os.path.join("bin/pipeline/shaders/vert.vert"), "r") as f:
            vertex_src = f.read()

        with open(os.path.join("bin/pipeline/shaders/frag.frag"), "r") as f:
            fragment_src = f.read()

        return self.ctx.program(
            vertex_shader=vertex_src,
            fragment_shader=fragment_src
        )

    def load_texture(self, name, image_path):
        with Image.open(image_path) as img:
            img = img.convert("RGBA")

            tex = self.ctx.texture(img.size, 4, img.tobytes())

        tex.filter = (moderngl.LINEAR, moderngl.LINEAR)

        # Bind Texture args 
        self.textures[name] = tex

    def draw(self, texture_name, x, y, width, height):
        vertices = np.array([
            x,         y,          0.0, 0.0,
            x+width,   y,          1.0, 0.0,
            x,         y+height,   0.0, 1.0,
            x+width,   y+height,   1.0, 1.0,
        ], dtype='f4')

        self.vbo.write(vertices.tobytes())

        self.textures[texture_name].use(0)

        self.program["tex"] = 0

    def render(self):
    
        self.uTime += 0.016
    
        self.program["uTime"].value = self.uTime
        self.program["uScrollSpeed"].value = self.uScrollSpeed
    
        self.program["uDarkColor"].value = tuple(c / 255.0 for c in self.uDarkColor)
    
        self.program["uLightColor"].value = tuple(c / 255.0 for c in self.uLightColor)

        self.vao.render(moderngl.TRIANGLE_STRIP)

        self.cycle_col()