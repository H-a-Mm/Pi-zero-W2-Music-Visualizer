# Internal Libs
import os

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

        self.vertices = np.array([
            -0.5, -0.5, 0.0, 0.0,
             0.5, -0.5, 1.0, 0.0,
            -0.5,  0.5, 0.0, 1.0,
             0.5,  0.5, 1.0, 1.0,
        ], dtype='f4')

        self.vbo = self.ctx.buffer(
            self.vertices.tobytes()
        )

        self.vao = self.ctx.vertex_array(
            self.program,
            [(self.vbo, '2f 2f', 'in_pos', 'in_uv')]
        )

        self.load_texture(
            "background",
            "assets/bg_img.png"
        )

        self.load_texture(
            "background_element",
            "assets/bg_elm_img.png"
        )

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

        self.vao.render(moderngl.TRIANGLE_STRIP)

    def render(self):
        self.draw("background", -1.0, -1.0, 2.0, 2.0)
        self.draw("background_element", -1.0, -1.0, 2.0, 2.0)