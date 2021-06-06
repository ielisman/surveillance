#! /usr/bin/python3

# pip install insightface
# pip install onnxruntime

import argparse
import cv2
import sys
import numpy as np
import insightface
from insightface.app import FaceAnalysis
import datetime

assert insightface.__version__>='0.2'

parser = argparse.ArgumentParser(description='insightface test')
# general
parser.add_argument('--ctx', default=0, type=int, help='ctx id, <0 means using cpu')
parser.add_argument('--prefix', default="igor1", type=str, help='image name without extension')
args = parser.parse_args()

app = FaceAnalysis(name='antelope')
app.prepare(ctx_id=args.ctx, det_size=(640,640))

prefix = args.prefix
img = cv2.imread(prefix+".jpg")

print ("Retrieving faces from ", prefix, datetime.datetime.now(), "...")
faces = app.get(img)
assert len(faces)==1 #6

print ("Drawing face identifications on ", prefix, datetime.datetime.now(), "...")
rimg = app.draw_on(img, faces)

print ("Saving identifications in other image ", prefix, datetime.datetime.now(), "...")
cv2.imwrite("./"+prefix+"_out.jpg", rimg)

print(len(faces))
for face in faces:
    print(face.bbox)
    print(face.kps)
    print(face.embedding.shape)

print ("all is done", datetime.datetime.now())
