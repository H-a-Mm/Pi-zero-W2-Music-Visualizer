# Internal Libs

# External Libs
import numpy as np

# Local Modules
from utils.tools import Load, Read


class Icon:
    @classmethod
    def __init__(cls, ctx): # Input path for now through the constructor
                                  # WILL CHANGE TO RUN LOCALY IN CLASS
        cls.ctx = ctx

        cls.read = Read()

        cls.load = Load()
        cls.program = cls.load.shaders(
            "bin/pipeline/elemets/icon/shaders/icon.vert",
            "bin/pipeline/elemets/icon/shaders/icon.frag"
        )

        cls.vertices = np.array([
            "1.0",  "1.0",  "0.0", "0.0",
            "-1.0", "1.0",  "1.0", "0.0",
            "-1.0", "-1.0", "0.0", "1.0",
            "1.0",  "-1.0", "1.0", "1.0"
        ])
