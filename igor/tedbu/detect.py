import cv2
from mtcnn import MTCNN

def getDetections(img, face_detector):
    img_rgb  = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    detections = face_detector.detect_faces(img_rgb)
    if len(detections) > 0:
        return detections
    else:
        return None