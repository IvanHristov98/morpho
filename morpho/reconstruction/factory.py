from enum import Enum


class ColorModel(Enum):
    BOOL = 0
    GRAYSCALE = 1


class Strategy(Enum):
    EROSION = 0
    DILATION = 1
