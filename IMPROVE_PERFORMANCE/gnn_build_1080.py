import torch
import torch.nn as nn
import torch.optim as optim
from torch_geometric.nn import GCNConv
from torch_geometric.data import Data, DataLoader
import networkx as nx
import pickle

GRAPH_NODE_FILE_NAME = 'graph_nodes'
GRAPH_EDGE_FILE_NAME = 'graph_edges'
SAVED_MODEL_FILE_NAME = 'saved_graph'
PATH_DIR = './'

# Open a file for reading
with open(f'{PATH_DIR}{GRAPH_NODE_FILE_NAME}.txt', 'r') as file:
    # Read the entire content of the file
    nodes = file.read().split(",")
    nodes.remove(nodes[-1])

with open(f'{PATH_DIR}{GRAPH_EDGE_FILE_NAME}.txt', 'r') as file:
    # Read lines and parse tuples
    edges = [eval(line.strip()) for line in file]

# print('nodes:', nodes)
# print('edges:', edges)

# Generate a synthetic graph
G = nx.Graph()

# Add nodes to the graph with string IDs
G.add_nodes_from(nodes)

# Define edges using string IDs
G.add_edges_from(edges)

# Update the labels and features accordingly
x = torch.tensor([G.degree(node) for node in G.nodes()], dtype=torch.float32).view(-1, 1)
# y = torch.tensor([1 if int(node[-1]) % 2 == 0 else 0 for node in G.nodes()], dtype=torch.long)
y = torch.tensor([1 if node[-1].isdigit() and int(node[-1]) % 2 == 0 else 0 for node in G.nodes()], dtype=torch.long)

# Convert the NetworkX graph to a PyTorch Geometric Data object
# data = Data(x=x, edge_index=torch.tensor([(int(edge[0][-1]), int(edge[1][-1])) for edge in G.edges]).t().contiguous(), y=y)
data = Data(x=x, edge_index = torch.tensor([(int(edge[0][-1]) if edge[0][-1].isdigit() else -1, int(edge[1][-1]) if edge[1][-1].isdigit() else -1) for edge in G.edges]).t().contiguous(), y=y)

# Define a simple Graph Convolutional Network (GCN) model
class GCN(nn.Module):
    def __init__(self, num_features, num_classes):
        super(GCN, self).__init__()
        self.conv1 = GCNConv(num_features, 16)
        self.conv2 = GCNConv(16, num_classes)

    def forward(self, data):
        x, edge_index = data.x, data.edge_index
        x = self.conv1(x, edge_index)
        x = torch.relu(x)
        x = self.conv2(x, edge_index)
        return x

# Create an instance of the GCN model
model = GCN(num_features=1, num_classes=2)

# Define the loss function and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.01)

# Create a DataLoader for batch processing (not necessary for this small dataset)
loader = DataLoader([data], batch_size=1, shuffle=True)

# Training loop
num_epochs = 200
for epoch in range(num_epochs):
    model.train()
    total_loss = 0
    for batch in loader:
        optimizer.zero_grad()
        output = model(batch)  # Here, batch should be a batch of graphs
        loss = criterion(output, batch.y.view(-1))  # Flatten batch.y
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    print(f'Epoch [{epoch + 1}/{num_epochs}], Loss: {total_loss:.4f}')

# Evaluate the model on the entire graph
model.eval()
graph_file_path = f'{PATH_DIR}{SAVED_MODEL_FILE_NAME}.pkl'
with open(graph_file_path, 'wb') as file:
    pickle.dump(G, file)
with torch.no_grad():
    logits = model(data)
    predicted_labels = logits.argmax(dim=1)
    correct = int(predicted_labels.eq(data.y).sum())
    accuracy = correct / len(data.y)
    print(f'Test Accuracy: {accuracy:.4f}')
