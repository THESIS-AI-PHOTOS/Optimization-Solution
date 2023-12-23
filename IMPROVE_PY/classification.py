import cv2
import os
import numpy as np
import pandas as pd
from skimage import io
from PIL import Image

def classify_faces(source_folder, output_folder):
    # Load the DataFrame from the JSON file
    df = pd.read_json(source_folder)
    face_encodings = {}
    face_groups = {}

    for index in range(len(df)):
        # Get face encoding from the DataFrame
        vector = np.array(df['image_encode'].iloc[index], dtype=np.uint8)
        face_encoding = df['encode'].iloc[index]
        
        if len(face_encoding):
            # Check if there's a folder for this person
            person_folder = f"Person_{len(face_encodings) + 1}"
            for person, encoding in face_encodings.items():
                face_encoding_np = np.array(face_encoding)
                encoding_np = np.array(encoding)
                # Compare encodings to determine if it belongs to the same person
                if cv2.norm(face_encoding_np, encoding_np, cv2.NORM_L2) < 0.4:
                    person_folder = person
                    break

            if person_folder not in face_encodings:
                face_groups[person_folder] = []
                # If there's no folder for this person, create a new one
                face_encodings[person_folder] = face_encoding

            face_groups[person_folder].append(df['name'].iloc[index])

            if vector.shape[2] == 1:
                vector = vector.squeeze()

            # saved_image_path = os.path.join(person_folder, f"{df['name'].iloc[index]}.png")
            # Image.fromarray(vector).save(saved_image_path)
    return face_groups
   


  
source_folder = "crop_face_encode_user-000001.json"
output_folder = "./similar-user-000001/"

face_groups = classify_faces(source_folder, output_folder)

with open('graph_nodes_user-000001.txt', 'w') as node:
  name_file_pairs = []
  for person_folder, names in face_groups.items():
        print(f"Group: {person_folder}")
        files = []
        
        for cropped in names:
            filename, extension = os.path.splitext(cropped)
      
              # Remove "_face_i" from the filename
            filename_without_suffix = filename.split('_face')[0]
            image = filename_without_suffix+extension
            node.write(cropped+ ',')
            node.write(image+ ',')
            for name in names:
                if cropped != name:
                    name_file_pairs.append((name,image)) 
  with open('graph_edges_user-000001.txt', 'w') as egdes:
    for pair in name_file_pairs:
        egdes.write(repr(pair) + '\n')
