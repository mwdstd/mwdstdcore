from .DGRF2015 import DGRF2015, DGRF2015_header
from .DGRF2015SV import DGRF2015SV
from numpy import asarray

dgrf15_header = [DGRF2015_header]
dgrf15 = [asarray(DGRF2015)]
dgrf15_sv = [asarray(DGRF2015SV)]
