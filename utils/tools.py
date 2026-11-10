# Internal Libs
import os
from itertools import chain
from io import BytesIO

# External Libs
import moderngl
from PIL import Image
from tinytag import TinyTag
from pathlib import Path

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

class Read:
    def cover(self, tag): # Tag defines tinytag meta-tag
        cover_bytes = tag.get("cover")
        title = tag.get("title")

        if cover_bytes:
            path = f"music/covers/{title}.png"
            image = Image.open(BytesIO(cover_bytes))
            image.save(path)
            print(f"Cover art saved as {path}")
        else:
            print(f"No album cover found for song {title}")

    def tag(self, path):
        path = Path(path)

        # Store the actual file objects in 'instances'
        instances = [
            f for f in chain(path.glob("*.mp4"), path.glob("*.m4a"))
            if f.is_file()
        ]

        count = len(instances)

        if count > 0:
            print(f"music found: {count}")
            metadata_list = []

            for file_path in instances:
                try:
                    tag_data = TinyTag.get(str(file_path), image=True)
                    metadata_list.append({
                        "file": file_path.name,
                        "artist": tag_data.artist,
                        "album": tag_data.album,
                        "title": tag_data.title,
                        "duration": tag_data.duration,
                        "cover": tag_data.get_image()
                    })
                except Exception as e:
                    print(f"Error reading metadata for {file_path.name}: {e}")

            return metadata_list
        else:
            print("no music found in dir")
