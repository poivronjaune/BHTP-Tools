Github Module
--------------

The github module (github.py) contains a "Github" Class that implements methods to retreive content information from a repository 
or download csv stock price files from github data source files.  

Github api return a json structure similr to this:

repo_content = 
[
    {'name': 'NASDAQ-BM0-2023-04-01.csv', 
     'path': 'NASDAQ-BM0-2023-04-01.csv', 
     'sha': '79355f8fdb3ef2386916102d9d937218df9d794e', 
     'size': 1154429, 
     'url': 'https://api.github.com/repos/MapleFrogStudio/DATA-2023-04/contents/NASDAQ-BM0-2023-04-01.csv?ref=main', 
     'html_url': 'https://github.com/MapleFrogStudio/DATA-2023-04/blob/main/NASDAQ-BM0-2023-04-01.csv', 
     'git_url': 'https://api.github.com/repos/MapleFrogStudio/DATA-2023-04/git/blobs/79355f8fdb3ef2386916102d9d937218df9d794e', 
     'download_url': 'https://raw.githubusercontent.com/MapleFrogStudio/DATA-2023-04/main/NASDAQ-BM0-2023-04-01.csv', 
     'type': 'file', 
    '_links': {
        'self': 'https://api.github.com/repos/MapleFrogStudio/DATA-2023-04/contents/NASDAQ-BM0-2023-04-01.csv?ref=main', 
        'git': 'https://api.github.com/repos/MapleFrogStudio/DATA-2023-04/git/blobs/79355f8fdb3ef2386916102d9d937218df9d794e', 
        'html': 'https://github.com/MapleFrogStudio/DATA-2023-04/blob/main/NASDAQ-BM0-2023-04-01.csv'
      }
    }, 
    {'name': 'NASDAQ-BM0-2023-04-02.csv', 
     'path': 'NASDAQ-BM0-2023-04-02.csv', 
     'sha': 'c6d79a4e0fb2a45acdeca0e4f0909c200a9a283e', 
     'size': 1154427, 'url': 'https://api.github.com/repos/MapleFrogStudio/DATA-2023-04/contents/NASDAQ-BM0-2023-04-02.csv?ref=main', 
     'html_url': 'https://github.com/MapleFrogStudio/DATA-2023-04/blob/main/NASDAQ-BM0-2023-04-02.csv', 
     'git_url': 'https://api.github.com/repos/MapleFrogStudio/DATA-2023-04/git/blobs/c6d79a4e0fb2a45acdeca0e4f0909c200a9a283e', 
     'download_url': 'https://raw.githubusercontent.com/MapleFrogStudio/DATA-2023-04/main/NASDAQ-BM0-2023-04-02.csv', 
     'type': 'file', 
     '_links': {
        'self': 'https://api.github.com/repos/MapleFrogStudio/DATA-2023-04/contents/NASDAQ-BM0-2023-04-02.csv?ref=main', 
        'git': 'https://api.github.com/repos/MapleFrogStudio/DATA-2023-04/git/blobs/c6d79a4e0fb2a45acdeca0e4f0909c200a9a283e', 
        'html': 'https://github.com/MapleFrogStudio/DATA-2023-04/blob/main/NASDAQ-BM0-2023-04-02.csv'
      }
    }, 
    {'name': 'NASDAQ-BM0-2023-04-03.csv', 
    'path': 'NASDAQ-BM0-2023-04-03.csv', 
    'sha': '985ae0310f2aeb95fe5d6c94acfcde81ad243a92', 
    'size': 1154434, 
    'url': 'https://api.github.com/repos/MapleFrogStudio/DATA-2023-04/contents/NASDAQ-BM0-2023-04-03.csv?ref=main', 
    'html_url': 'https://github.com/MapleFrogStudio/DATA-2023-04/blob/main/NASDAQ-BM0-2023-04-03.csv', 
    'git_url': 'https://api.github.com/repos/MapleFrogStudio/DATA-2023-04/git/blobs/985ae0310f2aeb95fe5d6c94acfcde81ad243a92', 
    'download_url': 'https://raw.githubusercontent.com/MapleFrogStudio/DATA-2023-04/main/NASDAQ-BM0-2023-04-03.csv', 
    'type': 'file', 
    '_links': {
        'self': 'https://api.github.com/repos/MapleFrogStudio/DATA-2023-04/contents/NASDAQ-BM0-2023-04-03.csv?ref=main', 
        'git': 'https://api.github.com/repos/MapleFrogStudio/DATA-2023-04/git/blobs/985ae0310f2aeb95fe5d6c94acfcde81ad243a92', 
        'html': 'https://github.com/MapleFrogStudio/DATA-2023-04/blob/main/NASDAQ-BM0-2023-04-03.csv'}
    }, 
    {'name': 'NASDAQ-BM0-2023-04-04.csv', 
     'path': 'NASDAQ-BM0-2023-04-04.csv', 
     'sha': '47627c18a760fef67396b508ded5cf1123d7c539', 
     'size': 1195480, 
     'url': 'https://api.github.com/repos/MapleFrogStudio/DATA-2023-04/contents/NASDAQ-BM0-2023-04-04.csv?ref=main', 
     'html_url': 'https://github.com/MapleFrogStudio/DATA-2023-04/blob/main/NASDAQ-BM0-2023-04-04.csv', 
     'git_url': 'https://api.github.com/repos/MapleFrogStudio/DATA-2023-04/git/blobs/47627c18a760fef67396b508ded5cf1123d7c539', 
     'download_url': 'https://raw.githubusercontent.com/MapleFrogStudio/DATA-2023-04/main/NASDAQ-BM0-2023-04-04.csv', 
     'type': 'file', 
     '_links': {
        'self': 'https://api.github.com/repos/MapleFrogStudio/DATA-2023-04/contents/NASDAQ-BM0-2023-04-04.csv?ref=main', 
        'git': 'https://api.github.com/repos/MapleFrogStudio/DATA-2023-04/git/blobs/47627c18a760fef67396b508ded5cf1123d7c539', 
        'html': 'https://github.com/MapleFrogStudio/DATA-2023-04/blob/main/NASDAQ-BM0-2023-04-04.csv'
      }
    }
]

.. automodule:: bhtp.github
   :members:
   :undoc-members:
   :show-inheritance:
