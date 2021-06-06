import func as distance
import numpy as np
import math
from PIL import Image

import matplotlib.pyplot as plt

def align(detection,img):
    x, y, w, h = detection["box"]
    detected_face = img[int(y):int(y+h), int(x):int(x+w)]
    
    if detected_face.shape[0] > 0 and detected_face.shape[1] > 0:
        keypoints = detection["keypoints"]
        left_eye_x, left_eye_y  = left_eye = keypoints["left_eye"]
        right_eye_x, right_eye_y = right_eye = keypoints["right_eye"]
        
        if left_eye_y > right_eye_y:
            point_3rd = (right_eye_x, left_eye_y)
            direction = -1 #rotate same direction to clock
        else:
            point_3rd = (left_eye_x, right_eye_y)
            direction = 1
        
        a = distance.findEuclideanDistance(np.array(left_eye), np.array(point_3rd))
        b = distance.findEuclideanDistance(np.array(right_eye), np.array(point_3rd))
        c = distance.findEuclideanDistance(np.array(right_eye), np.array(left_eye))
        
        if b != 0 and c != 0: #this multiplication causes division by zero in cos_a calculation
            cos_a = (b*b + c*c - a*a)/(2*b*c)
            angle = np.arccos(cos_a) #angle in radian
            angle = (angle * 180) / math.pi #radian to degree

            if direction == -1: #rotate base image
                angle = 90 - angle

            img = Image.fromarray(img)   # Image.fromarray(detected_face) 
            img = np.array(img.rotate(direction * angle))

            return img

    return None
            