import pytest
from flask.testing import FlaskClient
from mwdstdcore.server import app


@pytest.fixture()
def client():
    return app.test_client()

def test_ver(client: FlaskClient):
    response = client.get("/v1/ver")
    assert response.json['name'] == 'mwdstdcore'
