from enum import Enum


class ColorModel(Enum):
    BOOL = 0
    GRAYSCALE = 1


class Strategy(Enum):
    EROSION = 0
    DILATION = 1


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
