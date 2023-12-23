# import urllib.request
# import bz2
# import os

# def download_file(url, output_file):
#     try:
#         print(f"Downloading file from {url}")
#         urllib.request.urlretrieve(url, output_file)
#         print(f"Download completed. File saved as {output_file}")
#     except Exception as e:
#         print(f"Error downloading file: {e}")

# def unzip_bz2_file(zipped_file_name):
#     try:
#         print(f"Unzipping file: {zipped_file_name}")
#         with bz2.BZ2File(zipped_file_name, 'rb') as zipfile:
#             data = zipfile.read()
#             new_file_path = zipped_file_name[:-4]  # discard .bz2 extension
#             open(new_file_path, 'wb').write(data)
#             print(f"Unzip completed. File saved as {new_file_path}")
#     except Exception as e:
#         print(f"Error unzipping file: {e}")

# # URL of the file to download
# url = "http://dlib.net/files/dlib_face_recognition_resnet_model_v1.dat.bz2"

# # Local filename to save the downloaded file
# output_file = "dlib_face_recognition_resnet_model_v1.dat.bz2"

# # Call the function to download the file
# download_file(url, output_file)

# # Call the function to unzip the file
# unzip_bz2_file(output_file)

import urllib.request
import bz2
import os

def download_file(url, output_file):
    try:
        print(f"Downloading file from {url}")
        urllib.request.urlretrieve(url, output_file)
        print(f"Download completed. File saved as {output_file}")
    except Exception as e:
        print(f"Error downloading file: {e}")

def unzip_bz2_file(zipped_file_name):
    try:
        print(f"Unzipping file: {zipped_file_name}")
        with bz2.BZ2File(zipped_file_name, 'rb') as zipfile:
            data = zipfile.read()
            new_file_path = zipped_file_name[:-4]  # discard .bz2 extension
            open(new_file_path, 'wb').write(data)
            print(f"Unzip completed. File saved as {new_file_path}")
    except Exception as e:
        print(f"Error unzipping file: {e}")

# URL of the file to download
url = "http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2"

# Local filename to save the downloaded file
output_file = "shape_predictor_68_face_landmarks.dat.bz2"

# Call the function to download the file
download_file(url, output_file)

# Call the function to unzip the file
unzip_bz2_file(output_file)
