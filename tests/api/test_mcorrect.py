import pytest
from flask.testing import FlaskClient
from mwdstdcore.server import app


@pytest.fixture()
def client():
    return app.test_client()

def test_mcorrect(client: FlaskClient):
    response = client.post('/v1/mcorrect')
    assert response