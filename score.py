def greenwashing_score(ndvi, urban, pollution):

    vegetation_factor = 1 - ndvi
    urban_factor = urban
    pollution_factor = pollution

    score = (vegetation_factor*0.4 +
             urban_factor*0.3 +
             pollution_factor*0.3)

    return round(score*100,2)