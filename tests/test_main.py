import sys
import bhtp

def test_version():
    assert bhtp.__version__ is not None

def test_package_installed():
    assert 'bhtp' in sys.modules

    
