from .IGRF2020 import IGRF2020, IGRF2020_header
from .IGRF2020SV import IGRF2020SV
from numpy import asarray

igrf20_header = [IGRF2020_header]
igrf20 = [asarray(IGRF2020)]
igrf20_sv = [asarray(IGRF2020SV)]