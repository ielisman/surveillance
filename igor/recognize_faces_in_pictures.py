import face_recognition

# Load the jpg files into numpy arrays
igor_image = face_recognition.load_image_file("img/igor.jpg")
aj_image = face_recognition.load_image_file("img/aj.jpg")
unknown_image = face_recognition.load_image_file("img/aj2.jpg")

# Get the face encodings for each face in each image file
# Since there could be more than one face in each image, it returns a list of encodings.
# But since I know each image only has one face, I only care about the first encoding in each image, so I grab index 0.
try:
    igor_face_encoding = face_recognition.face_encodings(igor_image)[0]
    aj_face_encoding = face_recognition.face_encodings(aj_image)[0]
    unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0]
except IndexError:
    print("I wasn't able to locate any faces in at least one of the images. Check the image files. Aborting...")
    quit()

known_faces = [
    igor_face_encoding,
    aj_face_encoding
]

# results is an array of True/False telling if the unknown face matched anyone in the known_faces array
results = face_recognition.compare_faces(known_faces, unknown_face_encoding)

print("Is the unknown face a picture of Igor? {}".format(results[0]))
print("Is the unknown face a picture of Aj? {}".format(results[1]))
print("Is the unknown face a new person that we've never seen before? {}".format(not True in results))
