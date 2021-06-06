import cv2
import numpy as np
from tensorflow.keras.preprocessing import image

def represent(img, target_size):
    
    img = cv2.resize(img, (112, 112)) # target_size
    img_pixels = image.img_to_array(img)
    img_pixels = np.expand_dims(img_pixels, axis = 0)
    img_pixels /= 255 #normalize input in [0, 1]

    return img_pixels
    