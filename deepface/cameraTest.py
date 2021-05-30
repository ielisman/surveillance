from deepface import DeepFace

import cv2
import numpy as np
import datetime
import time

tic = time.time()
model_name = 'ArcFace' # 'VGG-Face', 'Facenet', 'OpenFace', 'DeepFace', 'ArcFace', 'DeepID', 'Ensemble' 'Dlib' (Dlib requires install of CMake and pip install dlib --user)
detector_backend = 'dlib' # mtcnn, opencv, ssd or dlib

model = DeepFace.build_model(model_name)


video_capture = cv2.VideoCapture(0)

while True:

    ret, frame = video_capture.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    rgb_small_frame = small_frame[:, :, ::-1] #::-1

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
