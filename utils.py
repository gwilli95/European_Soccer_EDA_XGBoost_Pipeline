import os
import shutil
import kagglehub
import sqlite3
import pandas as pd
from config import DATA_PATH

def ingest_kaggle_database(path):
    #1. Retrieve the download path
    try:
        download_path = kagglehub.dataset_download(path)
    except StopIteration as error:
        print(error, "Try using kagglehub.dataset_download(path, force_download = True) once to force-download the dataset into current cache. After the first time, leaving force_download activated will cause unnecessary re-downloads each time it is called.")
        return
        
    #2. Access the database file name
    downloaded_files = os.listdir(download_path) #Lists downloaded files
    sqlite_file = next(f for f in downloaded_files if f.endswith(".sqlite")) #Gets the first .sqlite file
    
    #3. Create the full file path (.sqlite file alone insufficient for access)
    full_path = os.path.join(download_path, sqlite_file)
    
    #4. Create data folder for the path to go in
    os.makedirs(DATA_PATH, exist_ok = True)
    
    #5. Copy full file path into the folder (using .move method instead may cause file conflict error)
    shutil.copy(full_path, DATA_PATH)
    
def join_player_attributes(all_attributes, core_attributes):
    """
    all_attributes: a list of all attributes to query, including goalkeeper attributes
    core_attributes: a list of the core attributes to query for all players, not including goalkeeper attributes
    
    This function is specific to the structure of this particular data and use case and is placed in utils.py to reduce
    clutter in the notebook.
    """
    
    #Establish connection for pd.read_sql in the loop
    db_name = "database.sqlite"
    path = DATA_PATH.joinpath(db_name)
    con = sqlite3.connect(path)
    
    #Initialize list of DataFrames for concatenation
    dfs = []

    #Joining loop
    for team in ["home", "away"]:
        for num in range(1, 12):
            query_1 = f"SELECT match_api_id, date AS match_date, {team}_player_{num} FROM Match;"
            
            df1 = pd.read_sql(sql = query_1, con = con) #Get raw DataFrame for joining stats to that player
            df1.match_date = pd.to_datetime(df1.match_date) #Convert to datetime
            df1 = df1.sort_values(by = "match_date") #Sort by date for pd.merge_asof
            df1[f"{team}_player_{num}"] = df1[f"{team}_player_{num}"].astype(float) #Required to prevent an error

            #Adding goalkeeper attributes only for goal keepers
            if num == 1:
                query_2 = f"SELECT player_api_id, date AS {team}_{num}_stat_date, {", ".join(all_attributes)} FROM Player_Attributes;"
                rename_dict = dict(zip(all_attributes, [f"{team}_{num}_{att}" for att in all_attributes]))
            else:
                query_2 = f"SELECT player_api_id, date AS {team}_{num}_stat_date, {", ".join(core_attributes)} FROM Player_Attributes;"
                rename_dict = dict(zip(core_attributes,[f"{team}_{num}_{att}" for att in core_attributes]))
        
            df2 = pd.read_sql(sql = query_2, con = con) #Get the stats for that player (with player_api_id and date for joining)
            df2 = df2.rename(columns = rename_dict)
            df2.player_api_id = df2.player_api_id.astype(float) #Requireed to prevent an error
            df2[f"{team}_{num}_stat_date"] = pd.to_datetime(df2[f"{team}_{num}_stat_date"]) #Convert to datetime
            df2 = df2.sort_values(by = f"{team}_{num}_stat_date") #Sort by date for pd.merge_asof
            
            #Merge the two DataFrames and add that to the list for concatenation after all player stats have been joined
            df3 = pd.merge_asof(df1, df2, left_by = f"{team}_player_{num}", right_by = "player_api_id", left_on = "match_date", right_on = f"{team}_{num}_stat_date", direction = "backward")
            df3 = df3.drop(columns = ["player_api_id", f"{team}_player_{num}"])
            if not (num == 1) & (team == "home"):
                df3 = df3.drop(columns = ["match_date", "match_api_id"]) #Match date is needed in merge_asof lookup but no longer needed in DataFrame after first iteration of this loop (would create duplicate columns)
            dfs.append(df3)
            
        #Concatenate DataFrames and drop nulls
        df = pd.concat(dfs, axis = 1)
        df = df.dropna()
    return df