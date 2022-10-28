import pytest
from flask.testing import FlaskClient
from mwdstdcore.server import app


@pytest.fixture()
def client():
    return app.test_client()

@pytest.mark.parametrize('url', [
    '/v1/lv1b',
    '/v1/lv2b',
    '/v1/lv3b',
    '/v1/mcorrect',
    '/v1/refcalc',
    ])
def test_post_data_not_json(client: FlaskClient, url: str):
    response = client.post(url)
    assert response.status_code == 400
