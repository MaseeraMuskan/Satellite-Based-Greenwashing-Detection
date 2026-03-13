import cv2
import numpy as np

def detect_vegetation(image_path):

    image = cv2.imread(image_path)

    if image is None:
        return None, None, None, "Invalid Image"

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    r = image[:,:,0].astype(float)
    g = image[:,:,1].astype(float)
    b = image[:,:,2].astype(float)

    # Excess Green Vegetation Index
    exg = 2*g - r - b

    exg_norm = (exg - np.min(exg)) / (np.max(exg) - np.min(exg))

    vegetation_mask = exg_norm > 0.35

    vegetation_pixels = np.sum(vegetation_mask)
    total_pixels = vegetation_mask.size

    vegetation_percentage = (vegetation_pixels / total_pixels) * 100
    non_vegetation_percentage = 100 - vegetation_percentage

    # Create heatmap
    heatmap = (exg_norm * 255).astype(np.uint8)

    return vegetation_percentage, non_vegetation_percentage, heatmap, "Valid"