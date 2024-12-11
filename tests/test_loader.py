import os
import pytest
import pandas as pd
from bhtp.loader import Loader

#DRIVE_PATH = os.path.abspath('D:\\stockdata')
#DATASET_FOLDER =  'DATA-2023-03'
DRIVE_PATH = os.path.abspath('.\\tests')
DATASET_FOLDER =  'test_data_folder'


def test_class_init():
    l = Loader(root_path=DRIVE_PATH)
    assert l is not None
    assert l.drive == DRIVE_PATH
    assert l.github_instance is not None

def test_fail_class_init():
    with pytest.raises(ValueError) as exc_info:
        l = Loader(root_path='somethingbad')

def test_is_folder_to_load_valid():
    #folder_to_load = 'DATA-2023-03'
    folder_to_load = DATASET_FOLDER
    l = Loader(DRIVE_PATH)
    assert l is not None
    assert l.is_folder_valid(folder_path=folder_to_load)

def test_fail_is_folder_to_load_valid():
    bad_folder = 'DATA-2023-030'
    l = Loader(DRIVE_PATH)
    assert l is not None
    assert not l.is_folder_valid(folder_path=bad_folder)

def test_fail_list_files_in_folder():
    bad_folder = 'DATA-2023-030'
    l = Loader(DRIVE_PATH)
    assert l is not None
    with pytest.raises(ValueError) as exc_info:    
        l.list_files_in_folder(folder_path=bad_folder)

def test_list_files_in_folder():
    #folder_to_load = 'DATA-2023-03'
    folder_to_load = DATASET_FOLDER
    l = Loader(DRIVE_PATH)
    assert l is not None
    files = l.list_files_in_folder(folder_path=folder_to_load)
    assert files is not None
    assert len(files) > 0
    print(f'\n\nNumber of files in folder: {len(files)}')

def test_fail_load_files_from_folder():
    bad_folder = 'DATA-2023-030'
    l = Loader(DRIVE_PATH)
    with pytest.raises(ValueError):
        l.load_files_from_folder(bad_folder)

def test_load_files_from_folder():
    #folder_to_load = 'DATA-2023-03'
    folder_to_load = DATASET_FOLDER
    l = Loader(DRIVE_PATH)
    assert l is not None
    data_df = l.load_files_from_folder(folder_path=folder_to_load, verbose=True)
    assert data_df is not None
    assert isinstance(data_df, pd.DataFrame)
    print(f'Number of prices loaded: {len(data_df)}')