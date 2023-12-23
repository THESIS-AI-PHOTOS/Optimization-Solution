#!/bin/bash
# 
# Danh sách các tệp Python cần chạy
python_files=("crop_face_test.py" "crop_face_encoding.py" "classification.py" "gnn_build.py" "predict.py" "preview.py")

# Lặp qua từng tệp và chạy chúng
for file in "${python_files[@]}"; do
    echo "Running $file..."
    python3 "$file"
    echo "----------------------------------------"
done