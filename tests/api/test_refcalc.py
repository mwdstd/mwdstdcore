import pytest
from flask.testing import FlaskClient
from mwdstdcore.server import app


@pytest.fixture()
def client():
    return app.test_client()

def test_point(client: FlaskClient):
    response = client.post('/v1/refcalc', json={
        'latitude': 0,
        'longitude': 0,
        'altitude': 0,
        'date': '2020-09-01T00:00:00.000Z',
        'gmag_mod': 'WMM2020',
        'crustal_field': False,
    })
    assert response.status_code == 200
    assert response.is_json
    assert response.json['err_model']['name'] == 'WMM'
    assert 'base_point' in response.json
    assert 'points' not in response.json

def test_traj(client: FlaskClient):
    response = client.post('/v1/refcalc', json={
        'latitude': 0,
        'longitude': 0,
        'altitude': 0,
        'date': '2020-09-01T00:00:00.000Z',
        'gmag_mod': 'WMM2020',
        'crustal_field': False,
        'plan': [
            {'md': 0, 'inc': 0, 'az': 0},
            {'md': 0, 'inc': 0, 'az': 0},
        ]
    })
    assert response.status_code == 200
    assert response.is_json
    assert response.json['err_model']['name'] == 'WMM'
    assert 'base_point' in response.json
    assert 'points' in response.json