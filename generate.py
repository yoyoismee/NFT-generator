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
args = parser.parse_args()

component = os.listdir(args.input_dir)
component = sorted(component)
component = [glob(args.input_dir + f"/{c}/*.png") for c in component]
component = [c for c in component if len(c) > 0]
print(component)
img_no = 0
Path(args.output_dir).mkdir(parents=True, exist_ok=True)

for _ in range(int(args.amount)):
    new_img = None
    for part in component:
        part_option = choice(part, 1)[0]
        tmp = Image.open(part_option)
        if new_img is None:
            new_img = tmp
        else:
            new_img.paste(tmp, (0, 0), tmp)
    new_img.save(f"{args.output_dir}/No_{img_no}.png")
    img_no += 1
