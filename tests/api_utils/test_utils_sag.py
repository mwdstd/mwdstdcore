from mwdstdcore.datamodel import Station
from mwdstdcore.api.v1.sag import calc_dls


def test_calcdls_empty():
    dlss = calc_dls([])
    assert dlss == []


def test_calcdls_single():
    dlss = calc_dls([Station(0, 0, 0)])
    assert dlss == [(0, 0)]


def test_calcdls_pair():
    dlss = calc_dls([
        Station(0, 0, 0),
        Station(30, 30, 0),
    ])
    assert dlss == [(0.5, 1), (1, 0.5)]

def test_calcdls_near():
    dlss = calc_dls([
        Station(0, 0, 0),
        Station(10, 5, 0),
        Station(20, 20, 0),
        Station(30, 30, 0),
    ])
    assert dlss == [(0.5, 1), ((30.-5.)/40., (30.-5.)/20.), (1, .5), ((30.-5.)/20., (30.-5.)/40.)]


def test_calcdls_rehash():
    stations = [
        Station(0, 0, 0),
        Station(10, 5, 0),
        Station(20, 20, 0),
        Station(30, 30, 0),
        Station(60, 30, 0),
        Station(75, 35, 0),
        Station(100, 10, 0),
    ]
    dlss_full = calc_dls(stations)
    dlss_1 = calc_dls(stations[:-1])
    dlss_2 = calc_dls(stations[:-2])
    dlss_3 = calc_dls(stations[:-3])

    assert dlss_full[:-2] == dlss_1[:-1]
    assert dlss_full[:-3] == dlss_2[:-1]
    assert dlss_full[:-5] == dlss_3[:-2]
