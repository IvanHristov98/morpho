import os
from pathlib import Path

import cv2

from morpho.cmd.config import Config
from morpho.marker import init_marker


def callback(event, x, y, flags, params):
    print(type(event), type(x), type(y), type(flags), type(params))
    
    print(flags)
    
    if event == 1:
        print("left click", x, y)


def loop(cfg: Config) -> None:
    img_dir = Path(os.environ["IMG_DIR"])
    dots_path = Path(img_dir, "dots_and_squares.png")
    
    mask = cv2.imread(str(dots_path), cv2.IMREAD_GRAYSCALE)
    
    marker = init_marker(mask, cfg.strategy)
    
    cv2.imshow('h', marker)
    cv2.waitKey(0)
    
    # print(points)
