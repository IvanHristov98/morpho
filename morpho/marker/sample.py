from pathlib import Path
from typing import List, NamedTuple, Callable, Any, Tuple

import numpy as np
import cv2


_WINDOW_NAME = "sample-image"
_MAX_WINDOW_WIDTH = 640
_MAX_WINDOW_HEIGHT = 480
_LEFT_CLICK = 1
_QUIT_KEY = 'd'


class Point(NamedTuple):
    x: int
    y: int


def sample(img_path: Path) -> List[Point]:
    print("Click on pixels from the image.")
    print(f"Stop selection by pressing '{_QUIT_KEY}' or '{_QUIT_KEY.upper()}'.")

    img = cv2.imread(str(img_path), cv2.IMREAD_GRAYSCALE)
    
    points = []
    point_collector = _point_collector(points)
    
    window_width, window_height = _window_size(img)
    
    cv2.namedWindow(_WINDOW_NAME, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(_WINDOW_NAME, window_width, window_height)

    cv2.setMouseCallback(_WINDOW_NAME, point_collector)
    
    cv2.imshow(_WINDOW_NAME, img)
    _listen_for_quit()

    cv2.destroyAllWindows()
    
    return points


def _point_collector(points: List[Point]) -> Callable[[int, int, int, Any, Any], None]:
    def collect_points(event, x, y, flags, params) -> None:
        if event != _LEFT_CLICK:
            return
        
        points.append(Point(x, y))
    
    return collect_points


def _window_size(img: np.ndarray) -> Tuple[int, int]: 
    width_scale = _MAX_WINDOW_WIDTH / img.shape[1]
    height_scale = _MAX_WINDOW_HEIGHT / img.shape[0]
    scale = min(width_scale, height_scale)
    
    window_width = int(img.shape[1] * scale)
    window_height = int(img.shape[0] * scale)
    
    return window_width, window_height


def _listen_for_quit() -> None:
    while True:
        key = cv2.waitKey(0)
            
        if key == ord(_QUIT_KEY) or key == ord(_QUIT_KEY.upper()):
            break
        
        print("Invalid key...")
