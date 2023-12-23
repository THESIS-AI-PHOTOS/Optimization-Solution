
import pickle
import json
import numpy as np
import pandas as pd
import dlib
from skimage import io
import cv2
import os
from datetime import datetime
import csv

# Initialize face detector, shape predictor, and face recognition model
detector = dlib.get_frontal_face_detector()
shape_predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")  # Adjust the path as needed
face_recognizer = dlib.face_recognition_model_v1("dlib_face_recognition_resnet_model_v1.dat")  # Adjust the path as needed

def get_face_encoding(file_path):
    image = io.imread(file_path)
    
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
def classify_faces(source_folder,face_encoding):
    # Load the DataFrame from the JSON file
    df = pd.read_json(source_folder)
    classify_faces_array=[]
    for index in range(len(df)):
        face_encoding_in_df  = df['encode'].iloc[index]
        
        if len(face_encoding_in_df):
            # Check if there's a folder for this person
                face_encoding_df = np.array(face_encoding_in_df)
                face_encoding_testing = np.array(face_encoding)

                # Compare encodings to determine if it belongs to the same person
                if cv2.norm(face_encoding_df, face_encoding_testing, cv2.NORM_L2) < 0.4:
                    classify_faces_array.append(df['name'].iloc[index])
                    
     
    return classify_faces_array

# graph_file_path = f'saved_graph_{QUANLITY}.pkl'

# with open(graph_file_path, 'rb') as file:
#     G = pickle.load(file)

# result = []
# for target_node in photo_cropped:
#     related_nodes = [node for node in G.neighbors(target_node)]
#     result.append({"meta": {"croppedId": target_node}, "results": [{"photoName": node} for node in related_nodes]})

# with open(f'{PATH_DIR}{RESULT_GNN_FILE_NAME}.txt', 'w') as file:
#     json.dump(result, file)

QUANLITY='user-000001'
SOURCE_FOLDER=f'./crop_face_encode_user-000001.json'
IMAGE_PATH= './user-000001/'
photos= os.listdir(IMAGE_PATH)
photo_cropped_id_df=[]
for photo in photos:
  photo_test_path= os.path.join(IMAGE_PATH,photo)

  face_encoding = get_face_encoding(photo_test_path) 
  if face_encoding!=None:
    start_time_class = datetime.now()
    photo_cropped_ids = classify_faces(SOURCE_FOLDER,face_encoding)
    end_time_class = datetime.now()
    photo_cropped_id_df.append({
      "photo":photo,
      "photo_cropped_ids":photo_cropped_ids,
      "start_time_class":start_time_class,
      "end_time_class":end_time_class
      })
    


graph_file_path = f'saved_graph_user-000001.pkl'

with open(graph_file_path, 'rb') as file:
    G = pickle.load(file)
    # print(G.nodes())
df =[]

for photo_cropped in photo_cropped_id_df:
    result=[]
    photo_cropped_ids = photo_cropped['photo_cropped_ids']
    photo_test_name=photo_cropped['photo']
    start_time_class=photo_cropped['start_time_class']
    end_time_class=photo_cropped['end_time_class']
    start_test = datetime.now()
    for target_node in photo_cropped_ids:
         # Data testing
        start_time = datetime.now()
        related_nodes = [node for node in G.neighbors(target_node)]
        actual = related_nodes
        # Get the end time
        end_time = datetime.now()
        # Calculate the duration
        duration = end_time - start_time
        photo_name_node = target_node
        result.append(
        {
        "target_node": target_node,
        "results": [{"photoName": node} for node in related_nodes],
        'start_time':start_time,
        'end_time':end_time,  
        })
    end_test = datetime.now()
    time_cropped= abs((start_time_class-end_time_class).total_seconds() )
    time_predict= abs((start_test-end_test).total_seconds() )
    total_time=time_cropped+time_predict
    df.append({
        'photo_test_name':photo_test_name,
        'time_cropped':time_cropped,
        'time_predict':time_predict,
        'total_time':total_time,
        'result':result   
        })

df_json = pd.DataFrame(df)
df_json.to_json(f'result_user-000001.json')