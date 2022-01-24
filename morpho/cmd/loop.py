import os
from pathlib import Path

from morpho.cmd.config import Config
from morpho.marker import sample


def callback(event, x, y, flags, params):
    print(type(event), type(x), type(y), type(flags), type(params))
    
    print(flags)
    
    if event == 1:
        print("left click", x, y)


def loop(cfg: Config) -> None:
    img_dir = Path(os.environ["IMG_DIR"])
    dots_path = Path(img_dir, "dots_and_squares.png")
    
    points = sample(dots_path)
    
    print(points)
