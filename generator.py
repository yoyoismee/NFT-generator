import time

from PIL import Image
from glob import glob
from numpy.random import choice
import os


class NFTGenerator:
    def __init__(self, input_dir, animate=False, n_frame=1, fps=1):
        self.input_dir = input_dir
        component = [p for p in os.listdir(self.input_dir) if not p.startswith('.')]
        component = sorted(component)
        component = [glob(self.input_dir + f"/{c}/*") for c in component]
        self.component = [c for c in component if len(c) > 0]
        self.n_frame = n_frame
        self.animate = animate
        self.fps = fps

    def generate(self, save_path=None, file_name=None):
        frames = []
        parts = []
        for part in self.component:
            part_option = choice(part, 1)[0]
            parts.append(part_option)
            if os.path.isdir(part_option):
                parts[-1] = [p for p in sorted(glob(part_option + '/*')) if not p.startswith('.')]

        for i in range(int(self.n_frame)):
            new_img = None
            for p in parts:
                if type(p) is list:
                    tmp = Image.open(p[i])
                else:
                    tmp = Image.open(p)
                if new_img is None:
                    new_img = tmp
                else:
                    new_img.paste(tmp, (0, 0), tmp)
            frames.append(new_img)
        if self.animate:
            if save_path is not None:
                if file_name is None:
                    file_name = str(time.time())
                frames[0].save(f"{save_path}/{file_name}.gif", save_all=True, append_images=frames[1:], loop=0,
                               duration=int(1000 / int(self.fps)))
            return frames
        else:
            if save_path is not None:
                if file_name is None:
                    file_name = str(time.time())
                frames[0].save(f"{save_path}/No_{file_name}.png")
            return frames[0]
