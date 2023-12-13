import os
import face_recognition
import numpy as np

def crop_all_faces(image_path):
    # Đọc ảnh đầu vào
    image = face_recognition.load_image_file(image_path)

    # Tìm kiếm khuôn mặt trong ảnh
    face_locations = face_recognition.face_locations(image)

    # Mã hóa khuôn mặt của ảnh đầu vào
    face_image_encodes = face_recognition.face_encodings(image)

    if not face_image_encodes:
        print("Không tìm thấy khuôn mặt trong ảnh đầu vào.")
        return []

    # Chuyển đổi list thành NumPy array
    face_image_encodes = np.array(face_image_encodes)

    # Lưu các khuôn mặt vào danh sách
    face_images = []
    for i, face_image_encode in enumerate(face_image_encodes):
        top, right, bottom, left = face_locations[i]
        face_images.append(image[top:bottom, left:right])

    return face_images, face_image_encodes

def compare_faces_with_cropped(image_file, face_image_encodes, image_folder_crops,file):
    # Lấy danh sách các tệp ảnh đã được cắt
    photo_croppeds = [root.strip() for root in os.listdir(image_folder_crops)]

    # Lặp qua từng ảnh đã được cắt để so sánh
    for i, face_image_encode in enumerate(face_image_encodes):
        if face_image_encode.size == 0:
            print(f"Không tìm thấy khuôn mặt trong ảnh đầu vào.")
            continue

        # So sánh mỗi khuôn mặt trong ảnh đầu vào với tất cả ảnh đã được cắt
        for photo_crop_path in photo_croppeds:
            # Đọc ảnh đã được cắt
            photo_crop_image = face_recognition.load_image_file(os.path.join(image_folder_crops, photo_crop_path))
            
            # Mã hóa khuôn mặt của ảnh đã được cắt
            photo_crop_encode = face_recognition.face_encodings(photo_crop_image)

            if not photo_crop_encode:
                print(f"Không tìm thấy khuôn mặt trong {photo_crop_path}.")
                continue

            # Chuyển đổi list thành NumPy array
            photo_crop_encode = np.array(photo_crop_encode)

            # So sánh khuôn mặt và tính toán độ tương đồng
            face_similarity = face_recognition.face_distance([face_image_encode], photo_crop_encode[0])
            
            if len(face_similarity) > 0:
                similarity_percentage = (1 - face_similarity[0]) * 100
                # print(f"Độ tương đồng với {photo_crop_path} - Khuôn mặt {i + 1}: {similarity_percentage}%")
                
                # Nếu độ tương đồng lớn hơn 70%, thông báo kết quả
                if similarity_percentage > 70: 
                    temp = []
                    temp.append(image_file)
                    temp.append(photo_crop_path.split(".")[0])
                    file.write(str(tuple(temp)) + "\n")
                    print(f"Khuôn mặt {image_file} của ảnh đầu vào tương đồng với {photo_crop_path}.")
                    break
            else:
                print(f"Không thể so sánh với {photo_crop_path} - Khuôn mặt {i + 1}.")

# Đường dẫn đến thư mục chứa ảnh của bạn
image_folder = "./1080/"
image_folder_crops = "./cropped_train"

# Lặp qua từng ảnh trong thư mục
with open(f'graph_edges_1080.txt', 'w') as file:
  i=0
  for image_file in os.listdir(image_folder):
      if image_file.lower().endswith(('.jpg', '.jpeg', '.png')):
          # Đường dẫn đầy đủ đến tệp ảnh
          image_path = os.path.join(image_folder, image_file)

          # Gọi hàm crop_all_faces cho mỗi tệp ảnh
          _, face_image_encodes = crop_all_faces(image_path)

          # Gọi hàm compare_faces_with_cropped để so sánh khuôn mặt
          compare_faces_with_cropped(image_file, face_image_encodes, image_folder_crops,file)
      if i==5:
        break
      i+=1