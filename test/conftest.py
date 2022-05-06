import pytest
from padaria.app import create_app

@pytest.fixture(scope='module')
def app():
    """instance of main flask app"""
    return create_app()