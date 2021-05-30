import numpy as np
import customDfDistance as dst

def calculateMatchingResult(img1_representation, img2_representation, distance_metric, model_name):

    if distance_metric == 'cosine':
        distance = dst.findCosineDistance(img1_representation, img2_representation)
    elif distance_metric == 'euclidean':
        distance = dst.findEuclideanDistance(img1_representation, img2_representation)
    elif distance_metric == 'euclidean_l2':
        distance = dst.findEuclideanDistance(dst.l2_normalize(img1_representation), dst.l2_normalize(img2_representation))    
    else:
        raise ValueError("Invalid distance_metric passed - ", distance_metric)

    distance = np.float64(distance)
    threshold = dst.findThreshold(model_name, distance_metric) # ensures euclid works

    if distance <= threshold:
        identified = True
    else:
        identified = False

    resp_obj = {
        "verified": identified
        , "distance": distance
        , "max_threshold_to_verify": threshold
        , "model": model_name
        , "similarity_metric": distance_metric
    }

    return resp_obj