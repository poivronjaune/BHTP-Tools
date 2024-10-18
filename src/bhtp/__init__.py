__version__ = "0.0.5"
version = __version__

from bhtp import github

def get_version():
    """
    Retrieve the current version of the package.

    Returns:
        str: The version string of the package, as specified by the `__version__` variable.
    """    
    return __version__
