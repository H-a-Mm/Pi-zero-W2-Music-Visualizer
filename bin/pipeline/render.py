# Internal Libs
import os
import colorsys

# External Libs
import numpy as np
from pathlib import Path
import moderngl
from PIL import Image

# Local Modules
from bin.pipeline.elemets.background import Background
from utils.tools import Load

SHADER_PATH = "/shaders"

class Render:
    def __init__(self, ctx):
        self.ctx = ctx

        self.load = Load()
        self.load.config(self.ctx) # Bind the load class

        self.program = self.load.shaders("bin/pipeline/shaders/vert.vert", "bin/pipeline/shaders/frag.frag")

        self.background = Background(self.ctx, self.program)

    def render(self, state):
        self.background.render(state)
        self.background.cycle_col()