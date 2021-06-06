#! /usr/bin/python3

# this implementation only returns 96.87% accuracy, 
# It uses TensorFlow Light to speed up results (pip install arcface)
# it uses pre-trained model based on ResNet50
# need to do face detection and alignment (See if_test.py)

from arcface import ArcFace

face_rec = ArcFace.ArcFace()
emb1 = face_rec.calc_emb("img/igor1_out.jpg")
print (emb1)

emb2 = face_rec.calc_emb("img/igor2_out.jpg")
dist = face_rec.get_distance_embeddings(emb1, emb2)

print ("Distance", dist)
