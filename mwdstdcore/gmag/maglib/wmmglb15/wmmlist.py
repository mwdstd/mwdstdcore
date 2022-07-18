from .WMM2015 import WMM2015, WMM2015_header
from .WMM2015SV import WMM2015SV
from numpy import asarray

wmm15_header = [WMM2015_header]
wmm15 = [asarray(WMM2015)]
wmm15_sv = [asarray(WMM2015SV)]
