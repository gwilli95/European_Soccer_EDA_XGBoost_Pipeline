import os
import kaggle
import pandas as pd
import pathlib
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
#from config import DATA_PATH
import sqlite3




import kagglehub
import shutil
import os
import sqlite3
import pandas as pd

def ingest_soccer_data(path):
    # 1. Download (No auth setup needed if you have kaggle.json)
    download_path = kagglehub.dataset_download(path)
    
    # 2. Find the sqlite file in the kagglehub cache
    files = os.listdir(download_path)
    sqlite_file = next(f for f in files if f.endswith('.sqlite'))
    full_path = os.path.join(download_path, sqlite_file)
    
    # 3. Move it to your local project folder for the team to use
    local_data_dir = "./data"
    os.makedirs(local_data_dir, exist_ok=True)
    local_file_path = os.path.join(local_data_dir, "database.sqlite")
    
    shutil.copy(full_path, local_file_path)
    print(f"Database ready at: {local_file_path}")
    
    # 4. Quick check
    conn = sqlite3.connect(local_file_path)
    df = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table';", conn)
    conn.close()
    return df