# This example is written using requests library

import requests

baseUri = "http://34.230.67.26:5000/6"

headers = {
    "Luna-Request-Id": "1536751345,8b8b5937-2c9e-4c8b-a7a7-5caf86621b5a",
    "Luna-Account-Id": "0921ad76-0ab5-430e-b857-5ff48baca0c7",
    "Content-Type": "image/jpeg",
}

with open("face_warp.jpg", "rb") as image_file:
    image = image_file.read()

url = f"{baseUri}/samples/faces"
response = requests.post(url, data=image, headers=headers)

print(response.status_code)
print(response.json())
