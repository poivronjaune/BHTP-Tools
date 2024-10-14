import pytest
from bhtp import github

def test_Github_class():
    g1 = github.Github()
    assert g1 is not None

@pytest.mark.parametrize("owner, repo, branch", [
    ('','DATA-2023-04','main'),
    (None,'DATA-2023-04','main'),
    ('MapleFrogStudio','','main'),
    ('MapleFrogStudio',None,'main'),
    ('MapleFrogStudio','DATA-2023-04',''),
    ('MapleFrogStudio','DATA-2023-04',None),
])
def test_Github_fail_sanity_checks(owner, repo, branch):
    owner = ''
    with pytest.raises(Exception):
        g1 = github.Github(owner=owner, repository=repo, branch=branch)

@pytest.mark.parametrize("owner, repo, branch", [
    ('MapleFrogStudio','DATA-2023-04','main'),
    ('PoivronJaune','DATA-2024-07','main'),
])
def test_Github__str__(owner, repo, branch):
    g1 = github.Github(owner=owner, repository=repo, branch=branch)
    assert g1 is not None
    assert g1.owner == owner
    assert g1.repo == repo
    assert g1.branch == branch
    g1.__str__() == f'https://github.com/{owner}/{repo}/tree/{branch}'

def test_api_content_property():
    g1 = github.Github()
    assert g1.api_content == 'https://api.github.com/repos/MapleFrogStudio/DATA-2023-04/contents/'

def test_repo_content():
    g1 = github.Github()
    content = g1.repo_content()
    assert content is not None
    assert isinstance(content, list)
