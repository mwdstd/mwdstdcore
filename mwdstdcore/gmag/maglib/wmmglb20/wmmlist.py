from .WMM2020 import WMM2020, WMM2020_header
from .WMM2020SV import WMM2020SV
from numpy import asarray

wmm20_header = [WMM2020_header]
wmm20 = [asarray(WMM2020)]
wmm20_sv = [asarray(WMM2020SV)]