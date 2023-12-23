import os
import dlib
from skimage import io
import cv2

_class="user-000001_train"
output_folder = f"cropped_{_class}"
output_path = os.path.join(output_folder)
# Set the path to the folder containing photos
folder_path = "./dataset/user-000001/"

# Initialize face detector, shape predictor, and face recognition model
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")  # Adjust the path as needed
face_recognizer = dlib.face_recognition_model_v1("dlib_face_recognition_resnet_model_v1.dat")  # Adjust the path as needed

# Iterate over each file in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(('.jpg', '.jpeg', '.png')):  # Adjust the file extensions as needed
        file_path = os.path.join(folder_path, filename)

        # Load the image
        image = io.imread(file_path)

        # Detect faces in the image
        faces = detector(image)

        # Iterate over each detected face
        for i, face in enumerate(faces):
            # Get the facial landmarks for the face
            landmarks = predictor(image, face)

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
            resized_face = cv2.resize(cropped_face, (100, 100))

            filename_n, file_extension = os.path.splitext(filename)
            name = f"{filename_n}_face_{i}{file_extension}"
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
            # Save or display the resized face
            output = os.path.join(output_path, name) # Adjust the output folder as needed
            io.imsave(output, resized_face)
