import pandas as pd
import os

# Đọc dữ liệu từ file CSV
json_file_path = "./result_user-000001.json"
data = pd.read_json(json_file_path)

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
                <th>Photo Test</th>
                <th colspan="5">Cropped Source</th>
                <th>Image predict</th>
                <th>Time Crop</th>
                <th>Time Predict</th>
                <th>Total time</th>
                <th>Total number</th>
                <th>Number correct</th>
                <th>Number incorrect</th>
                <th>Accuracy</th>
                <th>Precision</th>
                <th>Recall</th>
                <th>F1-Score</th>
            </tr>
        </thead>
        <tbody>
"""
source_image = "./dataset/user-000001/"
cropped = "./cropped_user-000001_train"
cropped_test = "./user-000001"

for index, record in data.iterrows():
    try:
      photo_test_name= record['photo_test_name']
      time_cropped= record['time_cropped']
      time_predict= record['time_predict']
      total_time= record['total_time']
      result =record['result']        
      photo_source =''
      for item in result:
         image = item['target_node']
         photo_source_result_node=''
         for detail in item['results']:
            photo_source_result_node+=f"""
                      <img style='margin-left: 20px' width=70 height=70 src="{source_image+ detail['photoName']}" />                  
              """
         photo_source+=f"""
                      <tr rowspan={len(item['results'])}>
                          <td>
                             <img style='margin-left: 20px' width=70 height=70 src="{cropped+'/'+ image}" />
                          </td>  
                      </tr>
                      
            """
      html_content += f"""
              <tr>
                <td>
                    <img style='margin-left: 20px' width=70 height=70 src="{cropped_test+'/'+ photo_test_name}" />
                </td>
                <td colspan="5">
                  <table>
                  <tr>
                  </tr>
                    {photo_source}
                   </table>
                </td>
                  <td class=number_incorrect>
                    {photo_source_result_node}
                    </td>
                  <td class=time_cropped>{time_cropped} s</td>
                  <td class=time_predict>{time_predict} s</td>
                  <td class=total_time>{total_time} s</td>
                  <td class=total_number>{len(result)}</td>
                  <td class=correct></td>
                  <td class=incorrect></td>
                  <td class=accuracy></td>
                  <td class=precision></td>
                  <td class=recall></td>
                  <td class=f1_score></td>
              </tr>
            """
    except:
       continue

html_content += """
        </tbody>
    </table>
</body>
</html>
"""

# Ghi mã HTML vào file
html_file_path = "result_table_user-000001.html"
with open(html_file_path, 'w', encoding='utf-8') as html_file:
    html_file.write(html_content)
