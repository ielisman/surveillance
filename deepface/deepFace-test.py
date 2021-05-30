from deepface import DeepFace
import time
import datetime

#dir = "C:\\development\\centos8-vm-shared\\tmp\\"
#dir = "C:\\development\\tools\\msys64\\home\\ielis\\camera-test"
dir = "C:\\development\\surveilance\\code\\deepface\\img"
img1 = dir + "\\image.jpg"
img2 = dir + "\\image3.jpg"


#result  = DeepFace.verify(img1, img2, model_name="ArcFace")
#print("Is verified: ", result["verified"], time.time()-tic)

#df = DeepFace.find(img_path = img1, db_path = dir, model_name = 'ArcFace', enforce_detection=False) # "C:/workspace/my_db"
#print (df.to_string(max_colwidth=250))
#model = DeepFace.build_model('DeepFace')
# embedding = DeepFace.represent(img1, model_name = 'ArcFace')

tic = time.time()
model_name = 'ArcFace' # 'VGG-Face', 'Facenet', 'OpenFace', 'DeepFace', 'ArcFace', 'DeepID', 'Ensemble' 'Dlib' (Dlib requires install of CMake and pip install dlib --user)
detector_backend = 'dlib' # mtcnn, opencv, ssd, dlib, retinaface
result  = DeepFace.verify(img1, img2, model_name=model_name, detector_backend=detector_backend, enforce_detection=False) # distance_metric = 'euclidean_l2' # mtcnn, opencv, ssd or dlib
print("\n\n =========== finished verifying", datetime.datetime.now(), time.time()-tic)


#print(f"starting to build model {model_name}", datetime.datetime.now())
#model = DeepFace.build_model(model_name)
#print("finished building model", datetime.datetime.now(), time.time()-tic)

#print(f"starting to verify {img1} vs {img2}", datetime.datetime.now())