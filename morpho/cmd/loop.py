import os
from pathlib import Path

import cv2

from morpho.cmd.config import Config
from morpho.marker import init_marker
from morpho.reconstruction import Reconstructor, Strategy, ColorModel


_RESULT_WINDOW = 'reconstructed-image'
_RECONSTRUCT_CMD = 'r'
_MODEL_CMD = 'm'
_STRATEGY_CMD = 's'
_BINARY_MODEL = 'b'
_GRAYSCALE_MODEL = 'g'
_EROSION_STRATEGY = 'e'
_DILATION_STRATEGY = 'd'


def loop(cfg: Config) -> None:
    while True:
        _print_main_menu(cfg)
        cmd_acronym = input("Enter cmd> ")
        
        switch = {
            _RECONSTRUCT_CMD: _reconstruct,
            _MODEL_CMD: _switch_model,
            _STRATEGY_CMD: _switch_strategy,
        }
        func = switch.get(cmd_acronym, _raise_error)

        func(cfg)


def _print_main_menu(cfg: Config) -> None:
    print("==== \033[0;32mMain Menu\033[0m ====")
    print("")
    print(f"\033[0;33mreconstruct image\033[0m (Enter {_RECONSTRUCT_CMD})")
    print(f"\033[0;33mchange color model\033[0m (Enter {_MODEL_CMD})")
    print(f"\033[0;33mchange strategy\033[0m (Enter {_STRATEGY_CMD})")
    print("")
    print(f"Current model -> {cfg.rec_cfg.model.value}")
    print(f"Current strategy -> {cfg.rec_cfg.strategy.value}")
    print("")


def _reconstruct(cfg: Config) -> None:
    reconstructor = Reconstructor(cfg.rec_cfg)
    
    img_path = input("Enter img path> ")
    
    mask = cv2.imread(str(img_path), cv2.IMREAD_GRAYSCALE)
    marker = init_marker(mask, cfg.rec_cfg.strategy)
    
    rec_img = reconstructor.reconstruct(mask, marker)
    
    print("Press any key to continue (without closing the window)...")
    cv2.imshow(_RESULT_WINDOW, rec_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    print()


def _switch_model(cfg: Config) -> None:
    print("To select a new color model enter one of:")
    print(f"- {_BINARY_MODEL} ->  \033[0;33mbinary\033[0m")
    print(f"- {_GRAYSCALE_MODEL} ->  \033[0;33mgrayscale\033[0m")
    
    model_acronym = input("Enter model> ")
    
    switch = {
        _BINARY_MODEL: ColorModel.BOOL,
        _GRAYSCALE_MODEL: ColorModel.GRAYSCALE,
    }
    cfg.rec_cfg.model = switch.get(model_acronym, ColorModel.BOOL)
    
    print(f"Switched to \033[0;33m{cfg.rec_cfg.model.value}\033[0m.")
    print()


def _switch_strategy(cfg: Config) -> None:
    print("To select a new strategy enter one of:")
    print(f"- {_EROSION_STRATEGY} -> \033[0;33merosion\033[0m")
    print(f"- {_DILATION_STRATEGY} -> \033[0;33mdilation\033[0m")
    
    strategy_acronym = input("Enter strategy> ")
    
    switch = {
        _EROSION_STRATEGY: Strategy.EROSION,
        _DILATION_STRATEGY: Strategy.DILATION,
    }
    cfg.rec_cfg.strategy = switch.get(strategy_acronym, Strategy.EROSION)
    
    print(f"Switched to \033[0;33m{cfg.rec_cfg.strategy.value}\033[0m.")
    print()


def _raise_error(_) -> None:
    raise Exception("Unexpected cmd received")
