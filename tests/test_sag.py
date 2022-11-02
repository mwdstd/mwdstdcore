import pytest
from numpy import deg2rad
from mwdstdcore.datamodel import BHA, Station
from mwdstdcore.sag.sagcor import sagcor, x2sag
from tests.params import bha_rss, bha_xcd

@pytest.mark.parametrize('bha', [bha_rss])
def test_rss(bha: BHA):
    traj = [
        Station(950., deg2rad(90.), 0),
        Station(1000., deg2rad(90.), 0)
    ]

    md = traj[-1].md
    mud_weight = 1290.
    gtf = 0.
    r = sagcor(bha, md, traj, gtf, mud_weight)

    assert abs(r.sag - deg2rad(-0.15)) < deg2rad(.005)

@pytest.mark.parametrize('bha', [bha_xcd])
def test_xcd(bha: BHA):
    traj = [
        Station(950., deg2rad(81.), 0),
        Station(1000., deg2rad(81.), 0)
    ]

    md = traj[-1].md
    mud_weight = 1290.
    gtf = 0.
    r = sagcor(bha, md, traj, gtf, mud_weight)
    sag1 = r.sag
    sag2 = x2sag(.75, r.opt, 19)

    diff = abs(sag1 - sag2)

    assert abs(diff - deg2rad(0.55)) < deg2rad(.05)
