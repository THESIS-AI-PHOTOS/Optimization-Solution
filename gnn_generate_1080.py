import os
import face_recognition

# Đường dẫn đến thư mục chứa các hình ảnh crop khuôn mặt
folder_path = "/path/to/your/folder"

# Tạo danh sách chứa các mã hóa khuôn mặt của tất cả các hình ảnh
face_encodings_list = []

# Lặp qua tất cả các tệp trong thư mục
for filename in os.listdir(folder_path):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        # Đường dẫn đầy đủ đến hình ảnh
        image_path = os.path.join(folder_path, filename)

        # Tải hình ảnh và xác định khuôn mặt trong hình ảnh
        image = face_recognition.load_image_file(image_path)
        face_locations = face_recognition.face_locations(image)
        face_encodings = face_recognition.face_encodings(image, face_locations)

        # Thêm mã hóa khuôn mặt vào danh sách nếu có ít nhất một khuôn mặt trong hình ảnh
        if len(face_encodings) > 0:
            face_encodings_list.extend(face_encodings)

# face_encodings_list bây giờ chứa mã hóa khuôn mặt của tất cả các hình ảnh trong thư mục
print("Number of face encodings:", len(face_encodings_list))

# Lặp qua tất cả các tệp trong thư mục
for filename in os.listdir(folder_path):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        # Đường dẫn đầy đủ đến hình ảnh
        image_path = os.path.join(folder_path, filename)

        # Tải hình ảnh và xác định khuôn mặt trong hình ảnh
        image = face_recognition.load_image_file(image_path)
        face_locations = face_recognition.face_locations(image)
        face_encodings = face_recognition.face_encodings(image, face_locations)

        # Kiểm tra xem có khuôn mặt trong hình ảnh không
        if len(face_encodings) > 0:
            # Lấy mã hóa của khuôn mặt đầu tiên trong hình ảnh
            face_encodings_list.append(face_encodings[0])

# Chuyển đổi danh sách mã hóa thành mảng numpy
face_encodings_array = np.array(face_encodings_list)

# Số lượng nhóm bạn muốn tạo
num_clusters = 3  # Thay đổi số lượng nhóm theo mong muốn

# Áp dụng thuật toán K-means clustering để gom nhóm các khuôn mặt
kmeans = KMeans(n_clusters=num_clusters)
kmeans.fit(face_encodings_array)

# Tạo một từ điển để lưu trữ các nhóm
image_groups = {i: [] for i in range(num_clusters)}

# Gán từng hình ảnh vào nhóm tương ứng
for filename, label in zip(os.listdir(folder_path), kmeans.labels_):
    image_groups[label].append(filename)

# In thông tin về các nhóm
for group, group_images in image_groups.items():
    print(f"Group {group + 1}: {', '.join(group_images)}")