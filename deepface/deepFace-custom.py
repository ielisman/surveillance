import os

# disables gpu (CUDA) - os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
# it seems it runs slower than cpu on my machine https://towardsdatascience.com/installing-tensorflow-with-cuda-cudnn-and-gpu-support-on-windows-10-60693e46e781
# https://datascience.stackexchange.com/questions/58845/how-to-disable-gpu-with-tensorflow
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
#os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' # disables unneccesary logging

import time
import datetime
from tqdm import tqdm
import customDfLib as cdl
import customDfDetector as cdd
import customDfMatching as cmatch

from deepface.commons import functions, realtime, distance as dst
from deepface.basemodels import VGGFace, OpenFace, Facenet, FbDeepFace, DeepID, DlibWrapper, ArcFace, Boosting

import numpy as np
import matplotlib.pyplot as plt

tic = time.time()

# dirs and files
dir = "C:\\development\\surveilance\\code\\deepface\\img"
img1 = dir + "\\image.jpg"
img2 = dir + "\\image3.jpg"
img3 = dir + "\\image4.jpg"
img4 = dir + "\\image2.jpg"

# model, detector, distance, etc
model_name = 'ArcFace' # 'VGG-Face', 'Facenet', 'OpenFace', 'DeepFace', 'ArcFace', 'DeepID', 'Ensemble' 'Dlib' (Dlib requires install of CMake and pip install dlib --user)
detector_backend = 'mtcnn' # mtcnn, opencv, ssd, dlib, retinaface
distance_metric = 'euclidean_l2' # 'cosine', euclidean, euclidean_l2
model = None 
enforce_detection = True

resp_objects = []
model_names = []
models = {}
metrics = []

img_list, bulkProcess = cdl.initialize_input(img1, img2)
cdd.initialize_detector(detector_backend = detector_backend)

metrics.append(distance_metric)
model_names.append(model_name)

# loading model
model = cdl.build_model(model_name)
models[model_name] = model

# represent of images: here you can load initial images of tenant faces
def represent(img_path, model_name = 'VGG-Face', model = None, enforce_detection = True, detector_backend = 'mtcnn'):

    input_shape     = input_shape_x, input_shape_y= cdl.find_input_shape(model) #decide input shape
    img             = cdl.preprocess_face(img = img_path, target_size=(input_shape_y, input_shape_x), enforce_detection = enforce_detection, detector_backend = detector_backend)
    embedding       = model.predict(img)[0].tolist() # represent
    return embedding


tic = time.time()
img1_representation = represent(img_path = img1, model_name = model_name, model = model, enforce_detection = enforce_detection, detector_backend = detector_backend)
print("\n\n =========== finished loading base image", datetime.datetime.now(), time.time()-tic)
tic = time.time()


img2_representation = represent(img_path = img2, model_name = model_name, model = model, enforce_detection = enforce_detection, detector_backend = detector_backend)
res = cmatch.calculateMatchingResult (img1_representation = img1_representation, img2_representation = img2_representation, distance_metric = distance_metric, model_name = model_name)
print("\n\n =========== finished representing and comparing image 1 and 2", datetime.datetime.now(), time.time()-tic)
print (res)
tic = time.time()

img3_representation = represent(img_path = img3, model_name = model_name, model = model, enforce_detection = enforce_detection, detector_backend = detector_backend)
res = cmatch.calculateMatchingResult (img1_representation = img1_representation, img2_representation = img3_representation, distance_metric = distance_metric, model_name = model_name)
print("\n\n =========== finished representing and comparing image 1 and 3", datetime.datetime.now(), time.time()-tic)
print (res)
tic = time.time()

img4_representation = represent(img_path = img4, model_name = model_name, model = model, enforce_detection = enforce_detection, detector_backend = detector_backend)
res = cmatch.calculateMatchingResult (img1_representation = img1_representation, img2_representation = img4_representation, distance_metric = distance_metric, model_name = model_name)
print("\n\n =========== finished representing and comparing image 1 and 4", datetime.datetime.now(), time.time()-tic)
print (res)
tic = time.time()

"""
import tensorflow as tf
tf.test.is_gpu_available( # testing if cuda is available
    cuda_only=False, min_cuda_compute_capability=None
)
try: # disabling GPUs for CPU --- or import os; os.environ["CUDA_VISIBLE_DEVICES"] = "-1" or empty
    # Disable all GPUS
    tf.config.set_visible_devices([], 'GPU')
    visible_devices = tf.config.get_visible_devices()
    for device in visible_devices:
        assert device.device_type != 'GPU'
except:
    # Invalid device or cannot modify virtual devices once initialized.
    pass
"""