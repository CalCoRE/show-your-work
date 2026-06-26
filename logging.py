import csv
import time
from IPython import get_ipython

def log_cell_csv(result):
    with open("study_data.csv", "a", newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            time.strftime("%Y-%m-%d %H:%M:%S"), 
            result.info.raw_cell, 
            "Error" if result.error_in_exec else "Success"
        ])

with open("study_data.csv", "w", newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Timestamp", "Code_Executed", "Status"])

get_ipython().events.register('post_run_cell', log_cell_csv)

print("Logger is now active! Run any cell to see it update study_data.csv")
