from .WMM2010 import WMM2010, WMM2010_header
from .WMM2010SV import WMM2010SV
from numpy import asarray

wmm10_header = [WMM2010_header]
wmm10 = [asarray(WMM2010)]
wmm10_sv = [asarray(WMM2010SV)]
