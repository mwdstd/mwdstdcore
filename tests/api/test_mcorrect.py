import pytest
from flask.testing import FlaskClient
from mwdstdcore.server import app


@pytest.fixture()
def client():
    return app.test_client()

def test_mcorrect(client: FlaskClient):
    response = client.post('/v1/mcorrect', json={
        'dni_cs': {
            'ABX': 0, 'ABY': 0, 'ABZ': 0,
            'ASX': 0, 'ASY': 0, 'ASZ': 0,
            'MBX': 0, 'MBY': 0, 'MBZ': 0,
            'MSX': 0, 'MSY': 0, 'MSZ': 0,
            'MXY': 0, 'MXZ': 0, 'MYZ': 0,
        },
        'surveys': [
            {'md': 0, 'gx': 1, 'gy': 1, 'gz': 1, 'bx': 1, 'by': 2, 'bz': 2,}
        ],
        'reference': [
            {'g': 0, 'b': 0, 'dip': 0}
        ]
    })
    assert response.status_code == 200
    assert response.is_json
    assert 'surveys' in response.json
    assert 'stations' in response.json
    assert len(response.json['surveys']) == 1
    assert len(response.json['stations']) == 1

