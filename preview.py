import csv
import os

# Đọc dữ liệu từ file CSV
csv_file_path = "result_face_detect.csv"
data = []

with open(csv_file_path, mode='r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        data.append(row)

# Tạo mã HTML
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Result Table</title>
    <style>
        table {
            border-collapse: collapse;
            width: 100%;
        }
        th, td {
            border: 1px solid #dddddd;
            text-align: left;
            padding: 8px;
        }
        th {
            background-color: #f2f2f2;
        }
    </style>
</head>
<body>
    <h2>Result Table</h2>
    <table>
        <thead>
            <tr>
                <th>Photo Name</th>
                <th>Actual</th>
                <th>Total number</th>
                <th>Number correct</th>
                <th>Number incorrect</th>
                <th>Accuracy</th>
                <th>Precision</th>
                <th>Recall</th>
                <th>F1-Score</th>
                <th>Time</th>
            </tr>
        </thead>
        <tbody>
"""

for record in data:
    displayActual = []
    for img in record['actual'].replace('[', '').replace(']', '').split(","):
        displayActual.append(f"<img style='margin-left: 20px' width=70 height=70 src={img} />")
    html_content += f"""
            <tr>
                <td>{record['photo_name']}</td>
                <td>{"".join(displayActual)}</td>
                <td class=total_number></td>
                <td class=number_correct></td>
                <td class=number_incorrect></td>
                <td class=accuracy></td>
                <td class=precision></td>
                <td class=recall></td>
                <td class=f1_score></td>
                <td class=time>{record['time']}</td>
            </tr>
"""

html_content += """
        </tbody>
    </table>
</body>
</html>
"""

# Ghi mã HTML vào file
html_file_path = "result_table_template.html"
with open(html_file_path, 'w') as html_file:
    html_file.write(html_content)
