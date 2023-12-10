import csv
import pickle
import json
from datetime import datetime
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../"))

RESULT_GNN_FILE_NAME = 'result_gnn'
SAVED_MODEL_FILE_NAME = 'saved_graph'

PATH_DIR = './'
UPLOAD_DIR = './TRAIN/'

photo_cropped = "407120167_3639339696355377_4868142843296156780_n".split(",")
photo_cropped = [path.strip() for path in photo_cropped]

graph_file_path = f'{PATH_DIR}{SAVED_MODEL_FILE_NAME}.pkl'

photo_name = ""
expected = []
actual = []
duration = 0

with open(graph_file_path, 'rb') as file:
    G = pickle.load(file)

result = []
for target_node in photo_cropped:
    # Get the start time
    start_time = datetime.now()
    related_nodes = [node for node in G.neighbors(target_node)]
    result.append({"meta": {"croppedId": target_node}, "results": [{"photoName": node} for node in related_nodes]})
    actual = [node for node in related_nodes]
    # Get the end time
    end_time = datetime.now()
    # Calculate the duration
    duration = end_time - start_time
    photo_name = target_node

with open(f'{PATH_DIR}{RESULT_GNN_FILE_NAME}.txt', 'w') as file:
    json.dump(result, file)

print(actual)
# Giả sử bạn có một danh sách các bản ghi như sau
data = [
    {"photo_name": photo_name, "actual": actual, 'time': duration},
]

# Tạo và ghi vào file CSV
csv_file_path = "result_face_detect.csv"
header = ["photo_name", "actual", "time"]

with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=header)
    
    # Viết header vào file
    writer.writeheader()

    # Viết từng dòng dữ liệu vào file
    for record in data:
        writer.writerow(record)

print(f"File CSV đã được tạo thành công tại: {csv_file_path}")
