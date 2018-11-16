import pytest

from app import create_app


@pytest.fixture
def app():
    app = create_app()
    app.debug = True
    app.config['TESTING'] = True
    return app.test_client()
