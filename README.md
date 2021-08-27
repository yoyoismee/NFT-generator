# NFT generator
this is the easiest way to generate a hell lotta image component

buckle up and follow me!

## how to

first have your image in .png (transparent background of course!)

structure it in this way.
in a folder create a sub-folder for each part of your NFT.
layer will be sorted based on name.
for simplicity I would recommend `[layer no]_whatever`
then in each sub-folder just put our part options in there.


for example.
```
your_awesome_nft
├── 01_body
│   ├── body_1.png
│   └── body_2.png
└── 02_face
    ├── face_1.png
    └── face_2.png
```

ok all good?

find a way to set up python [link](https://realpython.com/installing-python/)

run this stuff (don't worry I'm not gonna hack you LOL)

```
pip3 install -r requirement.txt
python3 generate.py [input_dir] [output_dir] [how many do ya want]
```
