import time
import pytest
from bhtp import load_prices_from_csv
from bhtp.github import Github

@pytest.fixture(scope="session")
def g1():
    # default: repository='DATA-2023-04'
    return Github()

def test_Github_class(g1):
    #g1 = Github()
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
    g2 = Github(owner=owner, repository=repo, branch=branch)
    assert g2 is not None
    assert g2.owner == owner
    assert g2.repo == repo
    assert g2.branch == branch
    g2.__str__() == f'https://github.com/{owner}/{repo}/tree/{branch}'

def test_api_content_property(g1):
    #g1 = Github()
    assert g1.api_content == 'https://api.github.com/repos/MapleFrogStudio/DATA-2023-04/contents/'

def test_repo_content(g1):
    #g1 = Github()
    content = g1.repo_content()
    assert content is not None
    assert isinstance(content, list)
    one_item = content[0]
    assert isinstance(one_item, dict)
    assert 'type' in one_item
    assert 'name' in one_item

def test_select_files(g1):
    #TODO add this test
    json_content = g1.repo_content()
    assert json_content is not None
    files = g1.select_files(repo_content = json_content)
    assert len(files) == len(json_content)

@pytest.mark.parametrize("owner, repo, branch, csv_file", [
    ('MapleFrogStudio','DATA-2023-04','main', 'NASDAQ-BM0-2023-04-02.csv'),
    ('PoivronJaune','DATA-2024-07','main','TSX-2024-07-14.csv'),
])
def test_Github_load_ohlcv_from_raw_link(owner, repo, branch, csv_file):
    raw_link = f'https://raw.githubusercontent.com/{owner}/{repo}/refs/heads/{branch}/{csv_file}'
    g3 = Github(owner=owner, repository=repo, branch=branch)
    assert g3 is not None
    #df = g3.load_ohlcv_from_raw_link(raw_link)
    df = load_prices_from_csv(raw_link)
    assert df is not None
    assert len(df) > 1000

@pytest.mark.parametrize("owner, repo, branch, csv_file", [
    ('MapleFrogStudio','DATA-2023-04','main', 'NASDAQ-BM0-2023-AA-02.csv'),
    ('PoivronJaune','DATA-2024-07','main','TSX-2024-AA-14.csv'),
])
def test_fail_Github_load_ohlcv_from_raw_link(owner, repo, branch, csv_file):
    raw_link = f'https://raw.githubusercontent.com/{owner}/{repo}/refs/heads/{branch}/{csv_file}'
    g4 = Github(owner=owner, repository=repo, branch=branch)
    with pytest.raises(Exception):
        df = g4.load_ohlcv_from_raw_link(raw_link)
        df = load_prices_from_csv(raw_link)

def test_fail_Github_sanity_check_load_ohlcv_for_month():
    #g1 = Github()
    with pytest.raises(Exception):
        df = g1.load_ohlcv_for_month(year=2022, month=1)

@pytest.mark.parametrize("owner, repo, branch, csv_file", [
    ('MapleFrogStudio','DATA-2023-04','main', 'NASDAQ-BM0-2024-04-28.csv'),
    ('PoivronJaune','DATA-2024-07','main','NASDAQ-BM0-2024-07-AB.csv'),
])
def test_fail_Github_load_ohlcv_from_file(owner, repo, branch, csv_file):
    with pytest.raises(Exception):
        g5 = Github(owner=owner, repository=repo, branch=branch)
        _ = g5.load_ohlcv_from_file(csv_file, verbose=True)

@pytest.mark.parametrize("owner, repo, branch, csv_file", [
    ('MapleFrogStudio','DATA-2023-04','main', 'NASDAQ-CC0-2023-04-03.csv'),
    ('PoivronJaune','DATA-2024-07','main','NASDAQ-BM0-2024-07-22.csv'),
])
def test_Github_load_ohlcv_from_file(owner, repo, branch, csv_file):
    g6 = Github(owner=owner, repository=repo, branch=branch)
    
    try:
        data_df = g6.load_ohlcv_from_file(csv_file, verbose=True)
    except Exception as e:
        pytest.fail(f"Failed to load CSV file: {e}")
    
    assert not data_df.empty

@pytest.mark.parametrize("day_str", [
    2023, '2023-04-01',
])
def test_Github_fail_load_ohlcv_for_day(day_str):
    with pytest.raises(Exception) as e_info:
        g1.load_ohlcv_for_day(full_dt=day_str)

