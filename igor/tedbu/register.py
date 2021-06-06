#!/usr/bin/python3

import os
import cv2

os.environ["CUDA_VISIBLE_DEVICES"] = "-1" # will suppress using CUDA

from mtcnn import MTCNN     # image detector
import modelArcFace         # pre-trained model

import detect
import align
import represent

import matplotlib.pyplot as plt

face_detector   = MTCNN() 			                    # face detector
model           = modelArcFace.loadModel()		        # model
input_shape     = model.layers[0].input_shape[0][1:3]	# input shape (112, 112)
img_dir         = "~/face-recognition/code/igor/img"

def register(face_detector,model,input_shape,frame,detections):
    print ("Registering")
    l = len(detections)
    if l > 1:
        print ("You should only register one user")
        return None
    elif l < 1:
        print ("No face is found")
        return None

    cv2.imwrite(f"{img_dir}/registered.jpg", frame)

    print (detections[0])

    img_aln = align.align(detections[0], frame)
    img_rep = represent.represent(img_aln, input_shape)

    retrieved_img = img_rep[0][:, :, ::-1]
    plt.imshow(retrieved_img)
    plt.show()

    return "Registered"

video_capture = cv2.VideoCapture(0)
while True:

    ret, frame = video_capture.read()

    detections = detect.getDetections(frame, face_detector)
    if detections != None:
        orig_frame = frame.copy()
        for detection in detections:
            x, y, w, h = detection["box"]
            cv2.rectangle(frame, (x, y+h), (x+w, y), (0, 0, 255), 2)
            cv2.imshow('Video', frame)

    keyPress = cv2.waitKey(1) & 0xFF  
    if keyPress == ord('r'):        
        register(face_detector,model,input_shape,orig_frame,detections)        
    elif keyPress == ord('q'): # Hit 'q' on the keyboard to quit!
        print ("..... Quiting")
        break

video_capture.release()
cv2.destroyAllWindows()
