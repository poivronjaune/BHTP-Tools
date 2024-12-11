import sys
import bhtp

def test_package_installed():
    assert 'bhtp' in sys.modules

def test_version():
    assert bhtp.__version__ is not None
    assert bhtp.version is not None

def test_get_version():
    assert bhtp.get_version() is not None
 
def test_load_ohclv_from_file():
    local_file_path = '.\\tests\\test_data.csv'
    df = bhtp.load_prices_from_csv(local_file_path)
    assert df is not None
