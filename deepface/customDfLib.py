import cv2
import customDfDetector as cdd
import numpy as np
import os

from deepface.basemodels import VGGFace, OpenFace, Facenet, FbDeepFace, DeepID, DlibWrapper, ArcFace, Boosting

from tensorflow import keras
from tensorflow.keras.preprocessing.image import load_img, save_img, img_to_array
from tensorflow.keras.applications.imagenet_utils import preprocess_input
from tensorflow.keras.preprocessing import image

import matplotlib.pyplot as plt

def build_model(model_name):

    model = None
    if   (model_name == 'ArcFace'):
        model = ArcFace.loadModel
    elif (model_name == 'DeepID'):
        model = DeepID.loadModel
    elif (model_name == 'DeepFace'):
        model = FbDeepFace.loadModel
    elif (model_name == 'Dlib'):
        model = DlibWrapper.loadModel
    elif (model_name == 'Facenet'):
        model = Facenet.loadModel
    elif (model_name == 'OpenFace'):
        model = OpenFace.loadModel
    elif (model_name == 'VGG-Face'):
        model = VGGFace.loadModel

    return model()

def find_input_shape(model):

    #face recognition models have different size of inputs
    #my environment returns (None, 224, 224, 3) but some people mentioned that they got [(None, 224, 224, 3)]. I think this is because of version issue.

    input_shape = model.layers[0].input_shape
    
    if type(input_shape) == list:
        input_shape = input_shape[0][1:3]
    else:
        input_shape = input_shape[1:3]

    if type(input_shape) == list: #issue 197: some people got array here instead of tuple
        input_shape = tuple(input_shape)        

    return input_shape

#detect and align
def preprocess_face(img, target_size=(224, 224), grayscale = False, enforce_detection = True, detector_backend = 'opencv', return_region = False):

    img = load_image(img)
    base_img = img.copy()

    # detecting face
    img, region = cdd.detect_face(img = img, detector_backend = detector_backend, grayscale = grayscale, enforce_detection = enforce_detection)

    # aligning face
    if img.shape[0] > 0 and img.shape[1] > 0:        
        img = cdd.align_face(img = img, detector_backend = detector_backend)
    else:
        if enforce_detection == True:
            raise ValueError("Detected face shape is ", img.shape,". Consider to set enforce_detection argument to False.")
        else: #restore base image
            img = base_img.copy()

    #post-processing
    if grayscale == True:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    img = cv2.resize(img, target_size)
    img_pixels = image.img_to_array(img)
    img_pixels = np.expand_dims(img_pixels, axis = 0)
    img_pixels /= 255 #normalize input in [0, 1]

    if return_region == True:
        return img_pixels, region
    else:
        return img_pixels

def loadBase64Img(uri):
   encoded_data = uri.split(',')[1]
   nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
   img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
   return img

def load_image(img):

	exact_image = False
	if type(img).__module__ == np.__name__:
		exact_image = True

	base64_img = False
	if len(img) > 11 and img[0:11] == "data:image/":
		base64_img = True

	#---------------------------

	if base64_img == True:
		img = loadBase64Img(img)

	elif exact_image != True: #image path passed as input
		if os.path.isfile(img) != True:
			raise ValueError("Confirm that ",img," exists")

		img = cv2.imread(img)

	return img

def initialize_input(img1_path, img2_path = None):

	if type(img1_path) == list:
		bulkProcess = True
		img_list = img1_path.copy()
	else:
		bulkProcess = False

		if (
			(type(img2_path) == str and img2_path != None) #exact image path, base64 image
			or (isinstance(img2_path, np.ndarray) and img2_path.any()) #numpy array
		):
			img_list = [[img1_path, img2_path]]
		else: #analyze function passes just img1_path
			img_list = [img1_path]

	return img_list, bulkProcess