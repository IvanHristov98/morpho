from typing import Callable

import numpy as np
import cv2

from morpho.reconstruction.config import Config, Strategy, ColorModel


_KERNEL_DIM_SIZE = 3


class Reconstructor:
    _cfg: Config
    
    def __init__(self, cfg: Config) -> None:
        self._cfg = cfg

    def reconstruct(self, mask: np.ndarray, marker: np.ndarray) -> np.ndarray:
        if self._cfg.model == ColorModel.RGB:
            return self._reconstruct_rgb_img(mask, marker)
    
        if self._cfg.strategy == Strategy.EROSION and self._cfg.model == ColorModel.BOOL:
            return self._reconstruct_binary_img_through_erosion(mask, marker)

        if self._cfg.strategy == Strategy.DILATION and self._cfg.model == ColorModel.BOOL:
            return self._reconstruct_binary_img_through_dilation(mask, marker)

        if self._cfg.strategy == Strategy.EROSION and self._cfg.model == ColorModel.GRAYSCALE:
            return self._reconstruct_grayscale_img_through_erosion(mask, marker)

        if self._cfg.strategy == Strategy.DILATION and self._cfg.model == ColorModel.GRAYSCALE:
            return self._reconstruct_grayscale_img_through_dilation(mask, marker)

        return None

    def _reconstruct_rgb_img(self, mask: np.ndarray, marker: np.ndarray) -> np.ndarray:
        laplacian_img = np.ndarray(shape=mask.shape, dtype=np.uint8)
        cv2.Laplacian(mask, cv2.CV_16S, laplacian_img)
        
        cv2.imshow(laplacian_img)
        cv2.waitKey(0)
        
        return mask

    def _reconstruct_binary_img_through_erosion(self, mask: np.ndarray, marker: np.ndarray) -> np.ndarray:
        def op(mask: np.ndarray, prev: np.ndarray, kernel: np.ndarray) -> np.ndarray:
            eroded_prev = cv2.erode(prev, kernel)
            return cv2.bitwise_or(eroded_prev, mask)
        
        return self._reconstruct_img(mask, marker, op)

    def _reconstruct_binary_img_through_dilation(self, mask: np.ndarray, marker: np.ndarray) -> np.ndarray:
        def op(mask: np.ndarray, prev: np.ndarray, kernel: np.ndarray) -> np.ndarray:
            dilated_prev = cv2.dilate(prev, kernel)
            return cv2.bitwise_and(dilated_prev, mask)
        
        return self._reconstruct_img(mask, marker, op)

    def _reconstruct_grayscale_img_through_erosion(self, mask: np.ndarray, marker: np.ndarray) -> np.ndarray:
        def op(mask: np.ndarray, prev: np.ndarray, kernel: np.ndarray) -> np.ndarray:
            eroded_prev = cv2.erode(prev, kernel)
            return cv2.max(eroded_prev, mask)
        
        return self._reconstruct_img(mask, marker, op)

    def _reconstruct_grayscale_img_through_dilation(self, mask: np.ndarray, marker: np.ndarray) -> np.ndarray:
        def op(mask: np.ndarray, prev: np.ndarray, kernel: np.ndarray) -> np.ndarray:
            dilated_prev = cv2.dilate(prev, kernel)
            return cv2.min(dilated_prev, mask)

        return self._reconstruct_img(mask, marker, op)

    def _reconstruct_img(self, mask: np.ndarray, marker: np.ndarray, op: Callable[[np.ndarray, np.ndarray, np.ndarray], np.ndarray]) -> np.ndarray:
        kernel = self._kernel()
        prev = marker
        
        while True:
            curr = op(mask, prev, kernel)
            
            if self._equal(prev, curr):
                break
            
            prev = curr
        
        return prev

    def _kernel(self) -> np.ndarray:
        return np.ones((_KERNEL_DIM_SIZE, _KERNEL_DIM_SIZE), np.uint8)
    
    def _equal(self, a: np.ndarray, b: np.ndarray) -> bool:
        diff_a = cv2.subtract(a, b)
        diff_b = cv2.subtract(b, a)
        return cv2.countNonZero(diff_a) == 0 and cv2.countNonZero(diff_b) == 0
