# This example is written using requests library

import requests
import json
import uuid
import time
from sys import argv
import os, fnmatch

headers = {                      
    "Luna-Request-Id": f'{int(time.time())},{uuid.uuid1()}',
    "Luna-Account-Id": "0921ad76-0ab5-430e-b857-5ff48baca0c7",
}
url = "http://34.230.67.26:5000/6/detector"

def processImage(imgName,url):  #imgName = "image.jpg" if (len(argv)<2) else argv[1]
    with open(imgName, "rb") as image_file:
        files = {
            "image": (
                imgName,
                image_file.read(),
                "image/jpeg",
            ),            
        }

    params = {
        "multiface_policy": 1,
        "estimate_quality": 1,        
    }

    response = requests.post(
        url, files=files, headers=headers, params=params
    )

    print ("\nProcessing " + imgName + " ---------------------------------------------------------------------------------------\n")
    print ("Params",params)
    print ("Headers",headers)    
    print ("POST Result ---------------------------------------------------------------------------------------")
    print(f'Response Code: {response.status_code}')
    print(response.json())    

print ("Starting Face Detector at " + url + "\n")
images = fnmatch.filter(os.listdir('.'), 'image*.jpg')
for imgName in images:
    processImage(imgName,url)