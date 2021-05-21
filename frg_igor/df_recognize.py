#! /usr/bin/python3

from deepface import DeepFace
import time

tik = time.time()
result  = DeepFace.verify( "katya1.jpg", 
                           "katya2.jpg", 
                           model_name = 'ArcFace', 
                           detector_backend = 'retinaface') # 'retinaface'
print("Is verified: ", result["verified"], time.time() - tik)


