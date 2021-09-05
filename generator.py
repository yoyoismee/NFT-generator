import time

from PIL import Image
from glob import glob
from numpy.random import choice
import os
from itertools import product


class NFTGenerator:
    def __init__(self, input_dir, animate=False, n_frame=1, fps=1, reverse=False, unique=False):
        self.input_dir = input_dir
        component = [p for p in os.listdir(self.input_dir) if not (p.startswith('.') or p.startswith('__'))]
        component = sorted(component, reverse=reverse)
        component = [glob(self.input_dir + f"/{c}/*") for c in component]
        self.component = [c for c in component if len(c) > 0]
        self.unique = unique
        if unique:
            self._options_product = product(*self.component)
        self.n_frame = n_frame
        self.animate = animate
        self.fps = fps

    def generate(self, save_path=None, file_name=None):
        frames = []
        parts = []
        if not self.unique:
            for part in self.component:
                part_option = choice(part, 1)[0]
                parts.append(part_option)
        else:
            parts = list(next(self._options_product))

        for i in range(len(parts)):
            if os.path.isdir(parts[i]):
                parts[i] = [p for p in sorted(glob(parts[i] + '/*')) if not (p.startswith('.') or p.startswith('__'))]

        for i in range(int(self.n_frame)):
            new_img = None
            for p in parts:
                if type(p) is list:
                    tmp = Image.open(p[i]).convert("RGBA")
                else:
                    tmp = Image.open(p).convert("RGBA")
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
