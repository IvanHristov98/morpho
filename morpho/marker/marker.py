import numpy as np

from morpho.marker.sample import sample, Point
from morpho.reconstruction import Strategy


_BLACK = 0
_WHITE = 255


def init_marker(mask: np.ndarray, strategy: Strategy) -> np.ndarray:
    bg_color = _background_color(strategy)
    
    marker = np.ndarray(shape=mask.shape, dtype=np.uint8)
    marker.fill(bg_color)
    
    _mark_pixels(mask, marker)

    return marker


def _background_color(strategy: Strategy) -> int:
    if strategy == Strategy.EROSION:
        return _BLACK
    
    return _WHITE


def _mark_pixels(mask: np.ndarray, marker: np.ndarray) -> np.ndarray:
    points = sample(mask)

    for point in points:
        intensity = mask.item((point.y, point.x))
        marker.itemset((point.y, point.x), intensity)
