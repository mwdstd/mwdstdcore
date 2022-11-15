import pytest
from flask.testing import FlaskClient
from mwdstdcore.server import app


@pytest.fixture()
def client():
    return app.test_client()

def test_main(client: FlaskClient):
    response = client.post("/v1/lv2b", json={
        'runs': [
            {
                'surveys': [
                    {'md': 0, 'gx': 1, 'gy': 1, 'gz': 1, 'bx': 1, 'by': 2, 'bz': 2,}
                ],
                'reference': [
                    {'g': 0, 'b': 0, 'dip': 0}
                ],
                'dni_rigid': True,
                'bha': {
                    'structure': [
                        {'type': 'bit', 'od': 1, 'id': 0, 'weight': 10, 'length': 10, 'material': 'steel'}
                    ],
                    'blades': [],
                    'dni_to_bit': 0,
                },
                'mud_weight': 0,
            }
        ],
        'geomag': 'hdgm',
        'head_ref': {'g': 0, 'b': 0, 'dip': 0},
    })

    assert response.status_code == 200
    assert response.is_json
    assert 'corrections' in response.json
