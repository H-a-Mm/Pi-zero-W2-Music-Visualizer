# Internal Libs

# External Libs

# Local Modules
from bin.pipeline.elemets.background.background import Background
from bin.pipeline.elemets.icon.icon import Icon


class Render:
    def __init__(self, ctx, tag):
        self.ctx = ctx
        self.background = Background(self.ctx)

        self.icon = Icon(self.ctx, tag)

    def render(self, state):
        self.background.render(state)
