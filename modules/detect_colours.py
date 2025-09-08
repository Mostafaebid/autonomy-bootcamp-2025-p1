"""
BOOTCAMPERS TO COMPLETE.

Detects colours on a map of landing pads.
"""

from pathlib import Path
import cv2
import numpy as np

# Bootcampers remove the following lines:
# Allow linters and formatters to pass for bootcamp maintainers
# pylint: disable=unused-argument,unused-variable,used-before-assignment


class DetectBlue:
    """
    Detects blue objects from an image.
    """

    __create_key = object()

    @classmethod
    def create(cls) -> "DetectBlue":
        """Factory method to create DetectBlue instance."""
        return DetectBlue(cls.__create_key)

    def __init__(self, class_create_private_key: object) -> None:
        """Private constructor, use create() method."""
        assert class_create_private_key is DetectBlue.__create_key, "Use create() method"

    def run(self, image: str, output_path: Path, return_mask: bool = False) -> None | np.ndarray:
        """
        Detects blue from an image and shows the annotated result.
        """
        img = cv2.imread(str(image))  # robust for Path inputs

        # ============
        # ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
        # ============
        # Convert to HSV
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # Blue range (OpenCV Hue ∈ [0,180])
        lower_blue = np.array([105, 140, 70], dtype=np.uint8)
        upper_blue = np.array([135, 255, 255], dtype=np.uint8)
        
        # Threshold to uint8 mask (0/255)
        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        kernel = np.ones((3, 3), dtype=np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)   
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=1) 


        # Optional visualization of masked image
        res = cv2.bitwise_and(img, img, mask=mask)
        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        # Annotate detections on the original image
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(img, contours, -1, (0, 255, 0), 2)

        # Save annotated image
        cv2.imwrite(str(output_path), img)

        # Tests depend on this return behavior
        return mask if return_mask else None


class DetectRed:
    """
    Detects red objects from an image.
    """

    __create_key = object()

    @classmethod
    def create(cls) -> "DetectRed":
        """Factory method to create DetectRed instance."""
        return DetectRed(cls.__create_key)

    def __init__(self, class_create_private_key: object) -> None:
        """Private constructor, use create() method."""
        assert class_create_private_key is DetectRed.__create_key, "Use create() method"

    def run(self, image: str, output_path: Path, return_mask: bool = False) -> None | np.ndarray:
        """
        Detects red from an image and shows the annotated result.
        """
        img = cv2.imread(str(image))  # robust for Path inputs

        # ============
        # ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
        # ============
        # Convert to HSV
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # Red wraps around 0° → two bands, then combine
        lower_red1 = np.array([0, 50, 50], dtype=np.uint8)
        upper_red1 = np.array([10, 255, 255], dtype=np.uint8)
        lower_red2 = np.array([170, 50, 50], dtype=np.uint8)
        upper_red2 = np.array([180, 255, 255], dtype=np.uint8)

        mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        mask = cv2.bitwise_or(mask1, mask2)

        # Optional visualization
        res = cv2.bitwise_and(img, img, mask=mask)

        # Use the mask for contours
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        cv2.drawContours(img, contours, -1, (0, 255, 0), 2)
        cv2.imwrite(str(output_path), img)

        # ============
        # ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
        # ============
        # Return mask like DetectBlue
        return mask if return_mask else None
        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============
