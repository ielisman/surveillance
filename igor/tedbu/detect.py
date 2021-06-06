import cv2

def getDetector(detector):
    face_detector = None
    if (detector == "mtcnn"):
        from mtcnn import MTCNN
        face_detector = MTCNN()
    elif (detector == "dlib"):
        import dlib
        from pathlib import Path
        face_detector = dlib.get_frontal_face_detector()
        dlib.shape_predictor(str(Path.home())+"/.deepface/weights/shape_predictor_5_face_landmarks.dat")
    return face_detector


def getDetections(img, face_detector):    
    img_rgb  = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    detections = face_detector.detect_faces(img_rgb)
    if len(detections) > 0:
        return detections
    else:
        return None

def getDetectionsDlib(img, face_detector):
    detections = face_detector(img, 1)
    if len(detections) > 0:
        return detections
    else:
        return None

"""
DLIB:
            for idx, d in enumerate(detections):
				left = d.left(); right = d.right()
				top = d.top(); bottom = d.bottom()

				detected_face = img[top:bottom, left:right]

				return detected_face, [left, top, right - left, bottom - top]
"""