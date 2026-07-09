import csv
import time
from IPython import get_ipython
from pathlib import Path
import os
import pandas as pd

# notebooks = ['Intro', 'CenterSpread', 'Spatial', 'TimeSeries']
# lang = ['R', 'Python']

# def nb_file(notebook: str,
#             lang: str):
#     files = os.listdir()
#     files_df = pd.DataFrame({'names': files})
#     files_df = files_df.loc[(files_df['names'].str.contains(lang)) == True]
#     nb = files_df.loc[(files_df['names'].str.contains(notebook)) == True]
#     return nb.iloc[0,0]

# notebook = nb_file(notebook = 'Intro', lang = 'Python').removesuffix('.ipynb')

# # note sure if needed
# ip = get_ipython()
# nb_path = (ip.user_ns['_dh'][0]/notebook)

def log_cell_csv(result):
    with open(f"meta_{notebook}_{time.strftime('%Y_%m_%d')}.csv", "a", newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            time.strftime("%Y-%m-%d %H:%M:%S"), 
            result.info.raw_cell, 
            "Error" if result.error_in_exec else "Success"
        ])

with open(f"meta_{notebook}_{time.strftime('%Y_%m_%d')}.csv", "w", newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Timestamp", "Code_Executed", "Status"])

get_ipython().events.register('post_run_cell', log_cell_csv)

print(f"Logger is now active! Run any cell to see it update meta_{notebook}_{time.strftime('%Y_%m_%d')}.csv")