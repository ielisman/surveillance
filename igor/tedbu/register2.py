import os
import cv2

os.environ["CUDA_VISIBLE_DEVICES"] = "-1" # will suppress using CUDA

from mtcnn import MTCNN     # image detector
import modelArcFace         # pre-trained model

import detect
import align
import represent

img_dir = "C:\\development\\surveilance\\code\\deepface\\img"

import matplotlib.pyplot as plt

face_detector   = detect.getDetector("dlib")
model           = modelArcFace.loadModel()		        # model
input_shape     = model.layers[0].input_shape[0][1:3]	# input shape (112, 112)
proc_this_frame = True
scale           = 4

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

    if proc_this_frame:

        #detections = detect.getDetections(rgb_small_frame, face_detector)
        detections = detect.getDetectionsDlib(frame, face_detector)
        if detections != None:
            orig_frame = frame.copy()
            for d in detections:
                #print (d)
                cv2.rectangle(frame, (d.left(), d.top()), (d.right(), d.bottom()), (0, 0, 255), 2)
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