# Internal Libs
import os

# External Libs
import numpy as np
from pathlib import Path
import moderngl

# Local Modules

SHADER_PATH =  "/shaders"

class Render:
    def __init__(self, ctx):
        self.ctx = ctx

        self.program = self.load_shaders()
        
        self.vertices = np.array([
            1.0, -1.0, 0.0,
            0.0,  1.0, 0.0,
           -1.0, -1.0, 0.0
        ], dtype = 'f4')

        self.vbo = ctx.buffer(self.vertices.tobytes())

        self.vao = ctx.vertex_array(
            self.program,
            [(self.vbo, '3f', 'in_vert')]
        )

    # Load the shaders, works in windows and linux
    # Path is relitive for root (Above bin)
    def load_shaders(self):
        with open(os.path.join("bin/pipeline/shaders/vert.vert"), "r") as f:
            self.vertex_src = f.read()

        with open(os.path.join("bin/pipeline/shaders/frag.frag"), "r") as f:
            self.fragment_src = f.read()

        return self.ctx.program(
            vertex_shader=self.vertex_src,
            fragment_shader=self.fragment_src
        )
        
    def render(self):
        self.vao.render(mode=moderngl.TRIANGLES, vertices=3)