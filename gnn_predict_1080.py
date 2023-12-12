
import pickle
import json
import argparse
from modules.utils.cropped_by_id import find_cropped_id

RESULT_GNN_FILE_NAME = 'result_gnn_1080'
SAVED_MODEL_FILE_NAME = 'saved_graph_1080'
PATH_DIR = './'
UPLOAD_DIR = './1080'

photo_cropped = find_cropped_id(f'{UPLOAD_DIR}')
print(photo_cropped)

graph_file_path = f'{PATH_DIR}{SAVED_MODEL_FILE_NAME}.pkl'

with open(graph_file_path, 'rb') as file:
    G = pickle.load(file)

result = []
for target_node in photo_cropped:
    related_nodes = [node for node in G.neighbors(target_node)]
    result.append({"meta": {"croppedId": target_node}, "results": [{"photoName": node} for node in related_nodes]})

with open(f'{PATH_DIR}{RESULT_GNN_FILE_NAME}.txt', 'w') as file:
    json.dump(result, file)
