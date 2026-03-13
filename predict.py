import numpy as np
from ndvi import calculate_ndvi
from score import greenwashing_score

def predict(image):

    ndvi_score, ndvi_map = calculate_ndvi(image)

    urban = np.mean(image > 0.6)

    pollution = np.mean(image < 0.3)

    score = greenwashing_score(ndvi_score, urban, pollution)

    return ndvi_score, urban, pollution, score, ndvi_map