from math import pi, radians as deg2rad
import sys
from time import time
import jsons
from mwdstdcore.sag.sagcor import sagcor
from mwdstdcore.datamodel.bha import BHA
from mwdstdcore.datamodel.station import Station
from matplotlib.pyplot import plot, fill_between


traj = [[950., deg2rad(88.)],
        [980., deg2rad(90.)],
        [990., deg2rad(90.)],
        [1000., deg2rad(92.)]]

md = traj[-1][0]
mud_weight = 1290.
gtf = 0.
wob = 0.e5

traj = [Station(st[0], st[1], 0.) for st in traj]
bh_design = [[0., 2000., 0.220]]

with open(f'{sys.path[0]}/__bha_test__.json') as f:
    bha = jsons.loads(f.read(), BHA)

t = time()
r = sagcor(bha, md, traj, gtf, mud_weight, wob, bh_design)
t = time() - t

z = r.grid
# sag = np.arctan((r.opt[1:] - r.opt[:-1]) / (z[1:] - z[:-1])) * 180 / pi
# plot(z[1:], sag, 'g.')
if True:
    plot(z, r.top + r.mid, 'r.')
    plot(z, r.opt + r.mid + r.od / 2, 'b')
    plot(z, r.opt + r.mid + r.id / 2, 'b')
    fill_between(z, r.opt + r.mid + r.od / 2, r.opt + r.mid + r.id / 2, color='gray', alpha=0.5)
    plot(z, r.opt + r.mid, 'g')
    plot(z, r.opt + r.mid - r.id / 2, 'b')
    plot(z, r.opt + r.mid - r.od / 2, 'b')
    fill_between(z, r.opt + r.mid - r.od / 2, r.opt + r.mid - r.id / 2, color='gray', alpha=0.5)
    plot(z, r.low + r.mid, 'r.')

print(f'BHA SYS PRO sag correction at 7.85 m is -0.15 deg')
print(f'Sag at {bha.dni_to_bit} m is {r.sag * 180 / pi:.3f} deg')
