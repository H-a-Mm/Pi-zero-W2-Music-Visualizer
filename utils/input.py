# Internal Libs

# External Libs
import glfw

# Local Modules


class Input:
    def check(self, win):
        if glfw.get_key(win, glfw.KEY_ESCAPE):
            glfw.terminate()

    def check_state(self, win, state):
        if glfw.get_key(win, glfw.KEY_0):
            state = "playing"

        if glfw.get_key(win, glfw.KEY_1):
            state = "selection"

        return state