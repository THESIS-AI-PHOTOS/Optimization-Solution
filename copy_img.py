import os
import shutil

def copy_images(src_folder, dest_folder):
    # Kiểm tra nếu thư mục đích không tồn tại, tạo mới
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    # Duyệt qua tất cả các thư mục con trong thư mục nguồn
    for root, dirs, files in os.walk(src_folder):
        for file in files:
            # Kiểm tra nếu đuôi file là ảnh (có thể thay đổi theo định dạng ảnh bạn đang sử dụng)
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                src_path = os.path.join(root, file)
                dest_path = os.path.join(dest_folder, file)

                # Copy file từ thư mục con sang thư mục đích
                shutil.copy2(src_path, dest_path)
                print(f'Copied: {file}')

# Đường dẫn thư mục nguồn và thư mục đích
src_folder = './TRAIN'
dest_folder = './destination'

# Gọi hàm copy_images để thực hiện việc sao chép
copy_images(src_folder, dest_folder)
