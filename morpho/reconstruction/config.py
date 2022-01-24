from enum import Enum


class ColorModel(Enum):
    BOOL = "binary"
    GRAYSCALE = "grayscale"


class Strategy(Enum):
    EROSION = "erosion"
    DILATION = "dilation"


class Config:
    model: ColorModel
    strategy: Strategy
    
    def __init__(self) -> None:
        self.model = ColorModel.BOOL
        self.strategy = Strategy.EROSION

    def with_model(self, model: ColorModel) -> None:
        self.model = model

    def with_strategy(self, strategy: Strategy) -> None:
        self.strategy = strategy
