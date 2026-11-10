# Internal Libs

# External Libs

# Local Modules
from bin.pipeline.elemets.background.background import Background


class Render:
    def __init__(self, ctx):
        self.ctx = ctx
        self.background = Background(self.ctx)

    def render(self, state):
        self.background.render(state)