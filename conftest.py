import pytest
import os


@pytest.fixture(scope='session')
def splinter_webdriver():
    """Override splinter webdriver name with BROWSER env variable."""
    return os.environ.get('BROWSER', 'firefox')
