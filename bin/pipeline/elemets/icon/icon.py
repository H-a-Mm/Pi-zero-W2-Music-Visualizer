# Internal Libs

# External Libs
import numpy as np

# Local Modules
from utils.tools import Load, Read


class Icon:
    @classmethod
    def __init__(cls, ctx, tag): # Input path for now through the constructor
                                 # WILL CHANGE TO RUN LOCALY IN CLASS
        cls.ctx = ctx
        cls.tag = tag
        cls.read = Read()

        cls.load = Load()
        cls.load.config(cls.ctx) # Bind the load class
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

        for song_metadata in cls.tag:
            cls.read.cover(song_metadata)
