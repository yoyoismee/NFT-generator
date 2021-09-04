import argparse
from pathlib import Path
from generator import NFTGenerator

parser = argparse.ArgumentParser()
parser.add_argument("input_dir", help="input dir")
parser.add_argument("output_dir", help="output dir")
parser.add_argument("amount", help="target amount")
parser.add_argument("--animate", action="store_true", help="create animate gif")
parser.add_argument("--n_frame", default=1, help="no frame")
parser.add_argument("--fps", default=4, help="frame per sec")
parser.add_argument("--unique", action="store_true", help="unique")

args = parser.parse_args()

Path(args.output_dir).mkdir(parents=True, exist_ok=True)
nft_gen = NFTGenerator(args.input_dir, animate=args.animate, n_frame=args.n_frame, fps=args.fps,unique=args.unique)
for i in range(int(args.amount)):
    img = nft_gen.generate(save_path=args.output_dir, file_name=str(f'{i + 1}'))
