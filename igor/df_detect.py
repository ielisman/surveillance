#! /usr/bin/python3
from retinaface import RetinaFace

resp = RetinaFace.detect_faces("img/gena1.jpg")
print (resp)
