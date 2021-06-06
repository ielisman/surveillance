#! /usr/bin/python3

import cv2
from mtcnn.mtcnn import MTCNN
detector = MTCNN()
img = cv2.imread('img/gena1.jpg')
faces = detector.detect_faces(img)# result
#to draw faces on image
for result in faces:
    x, y, w, h = result['box']
    x1, y1 = x + w, y + h
    cv2.rectangle(img, (x, y), (x1, y1), (0, 0, 255), 2)
