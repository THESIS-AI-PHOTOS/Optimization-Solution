import os
import face_recognition

USER_ID = 1080
PATH_DIR = ''
OUTPUT_FILE_PATH = ''
GRAPH_NODE_FILE_NAME = f'graph_node_{USER_ID}'
GRAPH_EDGE_FILE_NAME = f'graph_edges_{USER_ID}'

path = f"{PATH_DIR}{USER_ID}"
image_folder_path = f"./cropped_train/"
full_images_folder = f"./1080"
cropped_ids=[]
photo_cropped = os.listdir(image_folder_path) 
photo_cropped = [root.strip() for root in photo_cropped]
cropped_ids =  photo_cropped

network=[]

def find_and_create(image_path):

    image_of_person1 = face_recognition.load_image_file(image_path)
    person1_face_encoding = face_recognition.face_encodings(image_of_person1)
    if len(person1_face_encoding) < 1:
        return
    person1_face_encoding = person1_face_encoding[0]
    # Iterate through the full images
    for full_image_filename in os.listdir(full_images_folder):
        print('full_image_filename: ' + str(full_image_filename))
        # có Id cropped
        if full_image_filename == '.DS_Store':
            continue
        full_image_path = os.path.join(full_images_folder, full_image_filename)
        if os.path.isfile(full_image_path):
            # Load the current full image
            image_of_full = face_recognition.load_image_file(full_image_path)
            
            # Encode the face of the current full image
            full_image_face_encoding = face_recognition.face_encodings(image_of_full)
            if len(full_image_face_encoding) > 0:
                # Compare the face encodings and get a similarity score
                face_similarity = face_recognition.face_distance([person1_face_encoding], full_image_face_encoding[0])
                similarity_percentage = (1 - face_similarity[0]) * 100
                print("percent: " + str(similarity_percentage))
                # Filter images with similarity > 70%
                if similarity_percentage > 70:
                    network.append(full_image_filename.split(".")[0])
    
    print("Image filtering and organization completed.")

with open(f'{OUTPUT_FILE_PATH}{GRAPH_NODE_FILE_NAME}.txt', 'w') as file:
    # Get the list of full image filenames
    full_image_filenames = [filename.split('.')[0] for filename in os.listdir(full_images_folder) if filename != '.DS_Store']

    # Write full image filenames to the file
    file.write(','.join(full_image_filenames))

    # Check if full_image_filenames is not empty and cropped_ids is not empty
    if full_image_filenames and cropped_ids:
        # Write a comma only if full_image_filenames is not empty
        file.write(',')

    # Get the list of cropped image filenames
    cropped_filenames = [filename.split('.')[0] for filename in cropped_ids]

    # Write cropped image filenames to the file
    file.write(','.join(cropped_filenames))
with open(f'{OUTPUT_FILE_PATH}{GRAPH_EDGE_FILE_NAME}.txt', 'w') as file:
    for image_filename in cropped_ids:
        if image_filename == '.DS_Store':
            continue
        image_path = os.path.join(image_folder_path, image_filename)
        # print(image_filename.split('.'))
        find_and_create(image_path)
        print(image_filename.split(".")[0])
        print('network: ' + str(network))
        if (len(network) != 0):
            for n in network:
                temp = []
                temp.append(n)
                temp.append(image_filename.split(".")[0])
                file.write(str(tuple(temp)) + "\n")
        network=[]