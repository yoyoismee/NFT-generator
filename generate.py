import argparse
from PIL import Image
from glob import glob
from numpy.random import choice
import os
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("input_dir", help="input dir")
parser.add_argument("output_dir", help="output dir")
parser.add_argument("amount", help="target amount")
parser.add_argument("--animate", action="store_true", help="create animate gif")
parser.add_argument("--n_frame", default=1, help="no frame")
parser.add_argument("--fps", default=4, help="frame per sec")

args = parser.parse_args()

Path(args.output_dir).mkdir(parents=True, exist_ok=True)

component = [p for p in os.listdir(args.input_dir) if not p.startswith('.')]
component = sorted(component)
component = [glob(args.input_dir + f"/{c}/*") for c in component]
component = [c for c in component if len(c) > 0]
img_no = 0
for _ in range(int(args.amount)):
    frames = []
    parts = []
    for part in component:
        part_option = choice(part, 1)[0]
        parts.append(part_option)
        if os.path.isdir(part_option):
            parts[-1] = [p for p in sorted(glob(part_option + '/*')) if not p.startswith('.')]

    for i in range(int(args.n_frame)):
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
    if args.animate:
        frames[0].save(f"{args.output_dir}/No_{img_no}.gif", save_all=True, append_images=frames[1:], loop=0,
                       duration=int(1000 / int(args.fps)))
    else:
        frames[0].save(f"{args.output_dir}/No_{img_no}.png")

    img_no += 1
