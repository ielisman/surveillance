#! /usr/bin/python3

from deepface import DeepFace
import time

tik = time.time()
embedding = DeepFace.represent("img/igor1.jpg", model_name = 'ArcFace')
print ("embedding",embedding, time.time() - tik)

result  = DeepFace.verify( "img/katya1.jpg", 
                           "img/katya2.jpg", 
                           model_name = 'ArcFace', 
                           detector_backend = 'retinaface') # 'retinaface'
print("Is verified: ", result["verified"], time.time() - tik)


