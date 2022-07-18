from math import pi
from enum import Enum

# MGI, m/s2, global gravity reference error
# MBI, nT, global total B reference error
# MDI, rad, global Dip reference error
# DEC, rad, global fixed portion of declination error
# DBH, rad.nT, global horizontal component dependent portion of declination error
# GRE, m/s2, gravity measurement random noise
# BRE, nT, random total B reference error
# DRE, rad, random Dip reference error
# DCR, rad, random fixed portion of declination error
# DHR, rad.nT, random horizontal component dependent portion of declination error

wmm = {'MGI': 0.01, 'MBI': 152., 'MDI': 0.22 * pi / 180, 'DEC': 0.23 * pi / 180, 'DBH': 5430. * pi / 180,
       'GRE': 0.0015, 'BRE': 60., 'DRE': 0.08 * pi / 180, 'DCR': 0.1 * pi / 180, 'DHR': 3000. * pi / 180}

bggm = {'MGI': 0.01, 'MBI': 130., 'MDI': 0.2 * pi / 180, 'DEC': 0.36 * pi / 180, 'DBH': 5000. * pi / 180,
        'GRE': 0.0015, 'BRE': 60., 'DRE': 0.08 * pi / 180, 'DCR': 0.1 * pi / 180, 'DHR': 3000. * pi / 180}

hdgm = {'MGI': 0.01, 'MBI': 107., 'MDI': 0.16 * pi / 180, 'DEC': 0.3 * pi / 180, 'DBH': 4118. * pi / 180,
        'GRE': 0.0015, 'BRE': 60., 'DRE': 0.08 * pi / 180, 'DCR': 0.1 * pi / 180, 'DHR': 3000. * pi / 180}

ifr1 = {'MGI': 0.01, 'MBI': 50., 'MDI': 0.1 * pi / 180, 'DEC': 0.15 * pi / 180, 'DBH': 1500. * pi / 180,
        'GRE': 0.0015, 'BRE': 60., 'DRE': 0.08 * pi / 180, 'DCR': 0.1 * pi / 180, 'DHR': 3000. * pi / 180}

ifr2 = {'MGI': 0.01, 'MBI': 45., 'MDI': 0.08 * pi / 180, 'DEC': 0.15 * pi / 180, 'DBH': 1250. * pi / 180,
        'GRE': 0.0015, 'BRE': 15., 'DRE': 0.02 * pi / 180, 'DCR': 0.05 * pi / 180, 'DHR': 750. * pi / 180}

gmagmod = {'WMM': wmm, 'IGRF': wmm, 'MVSD': bggm, 'BGGM': bggm, 'MVHD': hdgm, 'HDGM': hdgm, 'EMM': hdgm, 'IFR1': ifr1,
           'IFR2': ifr2}


class GeoMagMod(str, Enum):
    WMM = 'WMM'
    IGRF = 'IGRF'
    EMM = 'EMM'
    MVSD = 'MVSD'
    BGGM = 'BGGM'
    HDGM = 'HDGM'
    MVHD = 'MVHD'
    IFR1 = 'IFR1'
    IFR2 = 'IFR2'

