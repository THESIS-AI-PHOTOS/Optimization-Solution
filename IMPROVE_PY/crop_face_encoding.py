import os
import dlib
from skimage import io
import cv2
from PIL import Image
import numpy as np
import pandas as pd

# Set the path to the folder containing photos
folder_path = "./dataset/user-000001/"

# Initialize face detector, shape predictor, and face recognition model
detector = dlib.get_frontal_face_detector()
shape_predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")  # Adjust the path as needed
face_recognizer = dlib.face_recognition_model_v1("dlib_face_recognition_resnet_model_v1.dat")  # Adjust the path as needed

store = []

def get_face_encoding(image):
    # Sử dụng dlib để lấy mã hóa khuôn mặt
    dets = detector(image, 1)

    if len(dets) > 0:
        shape = shape_predictor(image, dets[0])
        face_descriptor = face_recognizer.compute_face_descriptor(image, shape)

        # Convert dlib vector to a NumPy array and then to a list
        face_descriptor_list = np.array(face_descriptor).tolist()

        return face_descriptor_list
    else:
        return None
# Iterate over each file in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(('.jpg', '.jpeg', '.png')):
        file_path = os.path.join(folder_path, filename)

        # Load the image
        image = io.imread(file_path)

        # Detect faces in the image
        faces = detector(image)

        # Iterate over each detected face
        for i, face in enumerate(faces):
            # Get the facial landmarks for the face
            landmarks = shape_predictor(image, face)

            # Extract the coordinates of the bounding box
            left = min(landmarks.part(i).x for i in range(68))
            top = min(landmarks.part(i).y for i in range(68))
            right = max(landmarks.part(i).x for i in range(68))
            bottom = max(landmarks.part(i).y for i in range(68))

            # Calculate the new coordinates for cropping a square region around the face
            new_left = max(0, left)
            new_top = max(0, top)
            new_right = min(image.shape[1], right)
            new_bottom = min(image.shape[0], bottom)

            # Crop the face
            cropped_face = image[new_top:new_bottom, new_left:new_right]


            # Resize the cropped face to 100x100 pixels
            resized_face = cv2.resize(cropped_face, (100, 100), interpolation=cv2.INTER_AREA)

            
            # Get face encoding
            face_encoding = get_face_encoding(resized_face)

            if face_encoding:
                # Save face encoding and image details
                filename_n, file_extension = os.path.splitext(filename)
                name = f"{filename_n}_face_{i}{file_extension}"
                store.append({
                    "name": name,
                    "encode": face_encoding,
                    "image_encode": resized_face,
                })
        
# Create a DataFrame and save it to a JSON file
df = pd.DataFrame(store)
df.to_json(f'crop_face_encode_user-000001.json')
