# Internal Libs

# External Libs
import numpy as np
import moderngl

# Local Modules
from utils.tools import Load

class Background:
    def __init__(self, ctx):
        cls = type(self)
        cls.ctx = ctx
        cls.load = Load()
        cls.load.config(cls.ctx) # Bind the load class

        cls.program = cls.load.shaders(
            "bin/pipeline/elemets/background/shaders/bg.vert",
            "bin/pipeline/elemets/background/shaders/bg.frag"
        )

        cls.vertices = np.array([
            -1.0, -1.0, 0.0, 0.0,
             1.0, -1.0, 1.0, 0.0,
            -1.0,  1.0, 0.0, 1.0,
             1.0,  1.0, 1.0, 1.0,
        ], dtype='f4')

        cls.vbo = cls.ctx.buffer(
            cls.vertices.tobytes()
        )

        cls.vao = cls.ctx.vertex_array(
            cls.program,
            [(cls.vbo, '2f 2f', 'in_pos', 'in_uv')]
        )

        cls.colors = [
            [22, 22, 22],   # Black
            [0, 31, 73],    # Blue
            [159, 126, 49], # Yello
            [99, 5, 56],    # Pink
            [49, 2, 62]     # Purple
        ]

        cls.color_index = 0
        cls.color_t = 0.0

        cls.uTime = 1.0
        cls.uScrollSpeed = 0.0025
        cls.uDarkColor = [5, 5, 5]
        cls.uLightColor = cls.colors[0]

    @classmethod
    def cycle_col(cls):
        cls.color_t += 0.0002 # Time var

        if cls.color_t >= 1.0:
            cls.color_t = 0.0
            cls.color_index = (cls.color_index + 1) % len(cls.colors)

        current = cls.colors[cls.color_index]
        target = cls.colors[(cls.color_index + 1) % len(cls.colors)]

        t = cls.color_t * cls.color_t * (3.0 - 2.0 * cls.color_t)

        cls.uLightColor[0] = int(current[0] + (target[0] - current[0]) * t)
        cls.uLightColor[1] = int(current[1] + (target[1] - current[1]) * t)
        cls.uLightColor[2] = int(current[2] + (target[2] - current[2]) * t)

        cls.uDarkColor[0] = max(0, cls.uLightColor[0] - 20)
        cls.uDarkColor[1] = max(0, cls.uLightColor[1] - 20)
        cls.uDarkColor[2] = max(0, cls.uLightColor[2] - 20)

    @classmethod
    def render(cls, state):
        cls.uTime += 0.016

        cls.program["uTime"].value = cls.uTime
        cls.program["uScrollSpeed"].value = cls.uScrollSpeed

        cls.program["uDarkColor"].value = tuple(c / 255.0 for c in cls.uDarkColor)

        cls.program["uLightColor"].value = tuple(c / 255.0 for c in cls.uLightColor)

        cls.vao.render(moderngl.TRIANGLE_STRIP)

        if state == "playing":
            cls.cycle_col()
        else:
            cls.color_index = 0
