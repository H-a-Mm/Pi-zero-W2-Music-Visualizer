# Internal Libs
import os

# External Libs
import moderngl
from PIL import Image

# Local Modules

class Load:
    # Bind all atributes of the Load class in the -
    # config function.
    def config(self, ctx):
        self.ctx = ctx
        self.textures = {} # Here insted of constructer
    
    def shaders(self, vert_path, frag_path):
        with open(os.path.join(vert_path), "r") as f:
            vertex_src = f.read()
    
        with open(os.path.join(frag_path), "r") as f:
            fragment_src = f.read()
    
        return self.ctx.program(
            vertex_shader=vertex_src,
            fragment_shader=fragment_src
        )

    def texture(self, name, image_path):
        with Image.open(image_path) as img:
            img = img.convert("RGBA")

            tex = self.ctx.texture(img.size, 4, img.tobytes())

        tex.filter = (moderngl.LINEAR, moderngl.LINEAR)

        # Bind Texture args 
        self.textures[name] = tex