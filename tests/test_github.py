import time
import pytest
from bhtp.github import Github

def test_Github_class():
    g1 = Github()
    assert g1 is not None

@pytest.mark.parametrize("owner, repo, branch", [
    ('','DATA-2023-04','main'),
    (None,'DATA-2023-04','main'),
    ('MapleFrogStudio','','main'),
    ('MapleFrogStudio',None,'main'),
    ('MapleFrogStudio','DATA-2023-04',''),
    ('MapleFrogStudio','DATA-2023-04',None),
])
def test_fail_Github_sanity_checks(owner, repo, branch):
    owner = ''
    with pytest.raises(Exception):
        g1 = Github(owner=owner, repository=repo, branch=branch)

@pytest.mark.parametrize("owner, repo, branch", [
    ('MapleFrogStudio','DATA-2023-04','main'),
    ('PoivronJaune','DATA-2024-07','main'),
])
def test_Github__str__(owner, repo, branch):
    g1 = Github(owner=owner, repository=repo, branch=branch)
    assert g1 is not None
    assert g1.owner == owner
    assert g1.repo == repo
    assert g1.branch == branch
    g1.__str__() == f'https://github.com/{owner}/{repo}/tree/{branch}'

def test_api_content_property():
    g1 = Github()
    assert g1.api_content == 'https://api.github.com/repos/MapleFrogStudio/DATA-2023-04/contents/'

def test_repo_content():
    g1 = Github()
    content = g1.repo_content()
    assert content is not None
    assert isinstance(content, list)

def test_fail_Github_sanity_check_load_ohlcv_for_month():
    g1 = Github()
    with pytest.raises(Exception):
        df = g1.load_ohlcv_for_month(year=2022, month=1)

@pytest.mark.parametrize("owner, repo, branch, csv_file", [
    ('MapleFrogStudio','DATA-2023-04','main', 'NASDAQ-BM0-2024-04-28.csv'),
    ('PoivronJaune','DATA-2024-07','main','NASDAQ-BM0-2024-07-AB.csv'),
])
def test_fail_Github_load_ohlcv_for_day(owner, repo, branch, csv_file):
    with pytest.raises(Exception):
        g1 = Github(owner=owner, repository=repo, branch=branch)
        data_df = g1.load_ohlcv_for_day(csv_file, verbose=True)

@pytest.mark.parametrize("owner, repo, branch, csv_file", [
    ('MapleFrogStudio','DATA-2023-04','main', 'NASDAQ-CC0-2023-04-03.csv'),
    ('PoivronJaune','DATA-2024-07','main','NASDAQ-BM0-2024-07-22.csv'),
])
def test_Github_load_ohlcv_for_day(owner, repo, branch, csv_file):
    g1 = Github(owner=owner, repository=repo, branch=branch)
    
    try:
        data_df = g1.load_ohlcv_for_day(csv_file, verbose=True)
    except Exception as e:
        pytest.fail(f"Failed to load CSV file: {e}")
    
    assert not data_df.empty