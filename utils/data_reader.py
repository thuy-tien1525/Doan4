import csv
import os

def read_csv_data(file_name):
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(project_dir, file_name)

    with open(file_path, mode="r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)  # bỏ dòng header
        return list(reader)
