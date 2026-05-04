import pytest


@pytest.fixture(scope="session")
def splinter_window_size():
    """Tall enough that the autocomplete box never opens off-screen."""
    return (1280, 2000)
