# Internal Libs

# External Libs
import glfw
import moderngl

# Local Modules
from bin.pipeline.render import Render # relitive from root

class Main:
    def __init__(self):
        if not glfw.init():
            return

        self.win = glfw.create_window(960, 320, "visualizer", None, None) # When display is connected, change to run in full screen.
        if not self.win:
            glfw.terminate()
            return

        glfw.make_context_current(self.win)
        self.ctx = moderngl.create_context()
        self.render = Render(self.ctx)

        width, height = glfw.get_framebuffer_size(self.win)
        self.ctx.viewport = (0, 0, width, height)

        self.ctx.enable(moderngl.BLEND)

        self.state = "boot" # Controlls visulizer and music slections screen, runs the whole program, WILL MIGRATE LATER

    def check_input(self):
        if glfw.get_key(self.win, glfw.KEY_ESCAPE):
            glfw.terminate()

        if glfw.get_key(self.win, glfw.KEY_0):
            self.state = "playing"

        if glfw.get_key(self.win, glfw.KEY_1):
            self.state = "selection"

    def run(self):
        while not glfw.window_should_close(self.win):
            self.ctx.clear(0.0, 0.0, 0.0)

            self.check_input()
            self.render.render(self.state)

            glfw.swap_buffers(self.win)
            glfw.poll_events()

        glfw.terminate()

if __name__ == "__main__":
    engine = Main()
    engine.run()
