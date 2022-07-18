from mwdstdcore.gmag.gmagcalc.gmag import gmag_point, Date
from mwdstdcore.errormods.gmagmod import gmagmod, GeoMagMod

b = 57106
dec = 17.85
dip = 76.02
date = Date(1, 1, 2022)

gmod = gmagmod[GeoMagMod.MVSD]

res = gmag_point(60, 60, 0, date)
if abs(b - res.F) < 1. and abs(dip - res.Incl) < 0.01 and abs(dec - res.Decl) < 0.01:
    print('pass')
else:
    print('fail')
