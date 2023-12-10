import os
import face_recognition
# import argparse

# parser = argparse.ArgumentParser()
# parser.add_argument('--USER_ID', action="store", default="user-000001")
# parser.add_argument('--PHOTO_CROPPED', action="store", default="DSC09667_crop_1,DSC09264_crop_7,DSC09261_crop_2,DSC09261_crop_3,DSC09264_crop_6,DSC09667_crop_2,DSC09641_crop_0,DSC09264_crop_4,DSC09261_crop_0,DSC09265_crop_10,DSC09264_crop_5,DSC09641_crop_1,DSC09667_crop_3,_DSC6033_crop_0,DSC09821_crop_8,DSC09461_crop_3,DSC09821_crop_10,DSC09637_crop_2,DSC09626_crop_0,DSC09637_crop_3,DSC09461_crop_2,_DSC6033_crop_1,DSC09821_crop_9,DSC09461_crop_0,DSC09264_crop_2,DSC09637_crop_1,DSC09261_crop_7,DSC09637_crop_0,DSC09461_crop_1,IMG_4013_crop_0,DSC09652_crop_0,test_crop_0,DSC09643_crop_0,_DSC6395_crop_0,DSC09646_crop_0,IMG_4240_crop_0,DSC09368_crop_8,DSC09368_crop_5,DSC09460_crop_3,DSC09265_crop_1,DSC09640_crop_4,DSC09271_crop_5,DSC09368_crop_6,DSC09368_crop_7,DSC09264_crop_10,DSC09640_crop_3,DSC09640_crop_2,DSC09666_crop_0,DSC09264_crop_11,DSC09268_crop_7,DSC09640_crop_0,DSC09265_crop_4,DSC09640_crop_1,DSC09271_crop_2,DSC09821_crop_7,DSC09639_crop_1,DSC09821_crop_6,DSC09639_crop_3,DSC09261_crop_8,DSC09821_crop_1,DSC09821_crop_0,DSC09639_crop_4")
# parser.add_argument('--ACTIVE_CONFIG', action="store", default="local")

# args = parser.parse_args()
# print("var1 = %s" % args.USER_ID)
# print("var2 = %s" % args.PHOTO_CROPPED)
# print("var3 = %s" % args.ACTIVE_CONFIG)

# USER_ID = args.USER_ID
# PHOTO_CROPPED = args.PHOTO_CROPPED
# ACTIVE_CONFIG = args.ACTIVE_CONFIG
# PATH_DIR = ''
# OUTPUT_FILE_PATH = ''
USER_ID = 1
PHOTO_CROPPED = os.listdir('./cropped_train')
GRAPH_NODE_FILE_NAME = 'graph_node'
GRAPH_EDGE_FILE_NAME = 'graph_edges'
PATH_DIR = './destination'
OUTPUT_FILE_PATH = './'

photo_cropped = PHOTO_CROPPED
path = f"{PATH_DIR}{USER_ID}"
image_folder_path = './cropped_train'
full_images_folder = PATH_DIR
cropped_ids=[]
cropped_ids = photo_cropped    

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

with open(f'{OUTPUT_FILE_PATH}{GRAPH_NODE_FILE_NAME}_{USER_ID}.txt', 'w') as file:
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
with open(f'{OUTPUT_FILE_PATH}{GRAPH_EDGE_FILE_NAME}_{USER_ID}.txt', 'w') as file:
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
