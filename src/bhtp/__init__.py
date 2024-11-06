__version__ = "0.0.7"
version = __version__

from bhtp import github

def get_version():
    """
    Retrieve the current version of the package.

    This function returns the version string defined in the `__version__` variable of the package.
    
    Returns:
        str: The version string of the package, as specified by the `__version__` variable.
    
    Example:
        >>> import bhtp
        >>> bhtp.get_version()
        '1.0.0'
    
    Usage:
        This can be used to check the version of the package at runtime:
        
        >>> from bhtp import get_version
        >>> version = get_version()
        >>> print(f"Current package version: {version}")
        Current package version: 1.0.0    
    """
    return __version__
