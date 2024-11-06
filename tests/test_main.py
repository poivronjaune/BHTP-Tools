import sys
import bhtp

def test_package_installed():
    assert 'bhtp' in sys.modules

def test_version():
    assert bhtp.__version__ is not None
    assert bhtp.version is not None

def test_get_version():
    assert bhtp.get_version() is not None
 
