import numpy as np

def calculate_ndvi(image):

    red = image[:,:,0]
    green = image[:,:,1]

    ndvi_map = (green - red) / (green + red + 0.0001)

    ndvi_score = float(np.mean(ndvi_map))

    return ndvi_score, ndvi_map