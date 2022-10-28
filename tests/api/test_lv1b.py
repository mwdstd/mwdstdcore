import pytest
from flask.testing import FlaskClient
from mwdstdcore.server import app


@pytest.fixture()
def client():
    return app.test_client()

def test_main(client: FlaskClient):
    response = client.post("/v1/lv1b", json={})
    assert response.status_code == 400
