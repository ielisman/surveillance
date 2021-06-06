from deepface.commons import functions
import matplotlib.pyplot as plt

import os
from deepface import DeepFace
os.environ["CUDA_VISIBLE_DEVICES"] = "-1" # will suppress using CUDA
dir = "C:\\development\\surveilance\\code\\deepface\\img"
img1 = dir + "\\image.jpg"
img2 = dir + "\\image3.jpg"
result  = DeepFace.verify(img1, img2, model_name="ArcFace", distance_metric="euclidean_l2", enforce_detection=False, detector_backend="mtcnn")

"""
img = functions.load_image("../img/image.jpg")
backends = ['opencv', 'ssd', 'dlib', 'mtcnn'] # works for opencv, dlib only (3rd step for mtcnn does not work)
detector_backend = "dlib"

detected_face = functions.detect_face(img = img, detector_backend = detector_backend)
retrieved_img = detected_face[0][:, :, ::-1]
plt.imshow(retrieved_img)
plt.show()

aligned_face = functions.align_face(img = retrieved_img, detector_backend = detector_backend)
plt.imshow(aligned_face)
plt.show()

processed_img = functions.detect_face(img = aligned_face, detector_backend = detector_backend)
retrieved_img = processed_img[0]
plt.imshow(retrieved_img)
plt.show()
"""