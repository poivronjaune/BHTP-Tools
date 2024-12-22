from configparser import NoOptionError
import os
import pandas as pd
from bhtp import load_prices_from_csv
from bhtp.github import Github

class Loader:
    def __init__(self, root_path:str='C:\\stockdata'):
        self.drive = root_path
        if not os.path.exists(self.drive):
            raise ValueError(f'Root path for data files does not exist: {self.drive}')
    
        self.github_instance = Github()     # Github repo to required, use default, we only use ...load_from_raw_link()

    def __str__(self):
        txt = f'Loader drive:{self.drive}'
        return txt

    def is_folder_valid(self, folder_path:str):
        full_path = os.path.join(self.drive, folder_path)
        if os.path.exists(full_path):
            return True
        
        return False

    def list_files_in_folder(self, folder_path:str='DATA-2023-03'):
        full_path = os.path.join(self.drive, folder_path)
        if self.is_folder_valid(folder_path=full_path):
            #files = [os.path.join(full_path, f) for f in os.listdir(full_path) if os.path.isfile(os.path.join(full_path, f))]
            files = [f for f in os.listdir(full_path) if os.path.isfile(os.path.join(full_path, f))]
            return files
        else:
            raise ValueError(f'Invalid data folder to load: {folder_path}')
        
    def load_one_file_from_folder(self, folder_path:str, filename:str):
        all_files = self.list_files_in_folder(folder_path=folder_path)
        if filename in all_files:
            file_path = os.path.join(self.drive, folder_path, filename)
            data_df = self.github_instance.load_ohlcv_from_raw_link(file_path)
            return data_df
        else:
            return None

    def load_files_from_folder(self, folder_path:str, verbose:bool = False, break_after:int = 10000, source:bool=False):    
        files = self.list_files_in_folder(folder_path=folder_path)
        data_df = pd.DataFrame()
        for idx, file_name in enumerate(files):
            file = os.path.join(self.drive, folder_path, file_name)
            if verbose:
                print(f'{idx+1:4}/{len(files)} - Loading file: {file}')
            #data = self.github_instance.load_ohlcv_from_raw_link(file)
            data = load_prices_from_csv(file, source=True)
            data_df = pd.concat([data_df, data], ignore_index=True)
            if idx+1 >= break_after:
                break

        return data_df


if __name__ == '__main__':
    print('======================================')
    #folder_to_load = 'DATA-2023-03'
    l = Loader('D:\\stockdata')
    #data_df = l.load_files_from_folder(folder_path=folder_to_load, verbose=True)
    #print(data_df) 

