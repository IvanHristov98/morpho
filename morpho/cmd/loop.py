import os
from pathlib import Path

import cv2

from morpho.cmd.config import Config
from morpho.marker import init_marker
from morpho.reconstruction import Reconstructor


def callback(event, x, y, flags, params):
    print(type(event), type(x), type(y), type(flags), type(params))
    
    print(flags)
    
    if event == 1:
        print("left click", x, y)


def loop(cfg: Config) -> None:
    reconstructor = Reconstructor(cfg.rec_cfg)
    
    img_dir = Path(os.environ["IMG_DIR"])
    dots_path = Path(img_dir, "colibri.png")
    
    mask = cv2.imread(str(dots_path), cv2.IMREAD_GRAYSCALE)
    marker = init_marker(mask, cfg.rec_cfg.strategy)
    
    rec_img = reconstructor.reconstruct(mask, marker)
    cv2.imshow('s', rec_img)
    cv2.waitKey(0)
