import os
import cv2

os.environ["CUDA_VISIBLE_DEVICES"] = "-1" # will suppress using CUDA

from mtcnn import MTCNN     # image detector
import modelArcFace         # pre-trained model

import detect
import align
import represent
import time

img_dir = "C:\\development\\surveilance\\code\\deepface\\img"

import matplotlib.pyplot as plt

face_detector   = detect.getDetector("mtcnn")            # face detector face_detector   = MTCNN()
model           = modelArcFace.loadModel()		        # model
input_shape     = model.layers[0].input_shape[0][1:3]	# input shape (112, 112)
proc_this_frame = True
scale           = 4

pTime = 0
cTime = 0

def register(face_detector,model,input_shape,frame,detections):
    print ("Registering")
    l = len(detections)
    if l > 1:
        print ("You should only register one user")
        return None
    elif l < 1:
        print ("No face is found")
        return None

    cv2.imwrite(f"{img_dir}{os.path.sep}registered.jpg", frame)

    print (detections[0])

    img_aln = align.align(detections[0], frame)
    img_rep = represent.represent(img_aln, input_shape)

    retrieved_img = img_rep[0][:, :, ::-1]
    plt.imshow(retrieved_img)
    plt.show()

    return "Registered"

video_capture = cv2.VideoCapture(0)
while True:

    ret, frame      = video_capture.read()
    #small_frame     = cv2.resize(frame, (0, 0), fx=1/scale, fy=1/scale)
    #rgb_small_frame = small_frame[:, :, ::-1]

    cTime = time.time()
    if proc_this_frame:

        #detections = detect.getDetections(rgb_small_frame, face_detector)
        detections = detect.getDetections(frame, face_detector)
        if detections != None:
            orig_frame = frame.copy()
            for detection in detections:
                x, y, w, h = detection["box"]
                #x *= scale
                #y *= scale
                #w *= scale
                #h *= scale
                keypoints = detection["keypoints"]
                cv2.rectangle(frame, (x, y+h), (x+w, y), (0, 0, 255), 2)
                """
                cv2.circle(frame, keypoints["left_eye"],    radius=2, color=(0, 0, 255), thickness=-1)
                cv2.circle(frame, keypoints["right_eye"],   radius=2, color=(0, 0, 255), thickness=-1)
                cv2.circle(frame, keypoints["nose"],        radius=2, color=(0, 0, 255), thickness=-1)
                cv2.circle(frame, keypoints["mouth_left"],  radius=2, color=(0, 0, 255), thickness=-1)
                cv2.circle(frame, keypoints["mouth_right"], radius=2, color=(0, 0, 255), thickness=-1)
                """

                fps = 1/(cTime-pTime)
                pTime = cTime

                cv2.putText(frame, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)
                cv2.imshow('Video', frame)

    proc_this_frame = not proc_this_frame

    keyPress = cv2.pollKey() & 0xFF
    if keyPress == ord('r'):        
        register(face_detector,model,input_shape,orig_frame,detections)        
    elif keyPress == ord('q'): # Hit 'q' on the keyboard to quit!
        print ("..... Quiting")
        break

video_capture.release()
cv2.destroyAllWindows()