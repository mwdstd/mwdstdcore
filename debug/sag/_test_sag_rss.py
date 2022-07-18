from math import pi, radians as deg2rad
import sys
from time import time
import jsons
import numpy as np
from matplotlib.pyplot import plot, fill_between, show
from mwdstdcore.sag.sagcor import sagcor
from mwdstdcore.datamodel.bha import BHA
from mwdstdcore.datamodel.station import Station


traj = [[950., deg2rad(90.)],
        [980., deg2rad(90.)],
        [990., deg2rad(90.)],
        [1000., deg2rad(90.)]]

md = traj[-1][0]
mud_weight = 1290.
gtf = 0.
wob = 0.e5

traj = [Station(st[0], st[1], 0.) for st in traj]

with open(f'{sys.path[0]}/__bha_rss__.json') as f:
    bha = jsons.loads(f.read(), BHA)

t = time()
r = sagcor(bha, md, traj, gtf, mud_weight, wob)
t = time() - t

z = r.grid
# sag = np.arctan((r.opt[1:] - r.opt[:-1]) / (z[1:] - z[:-1])) * 180 / pi
# plot(z[1:], sag, 'g.')
opt = np.array(r.opt)
top = np.array(r.top)
mid = np.array(r.mid)
low = np.array(r.low)
od = np.array(r.od)
id = np.array(r.id)

if True:
    plot(z, top + mid, 'r.')
    plot(z, opt + mid + od / 2, 'b')
    plot(z, opt + mid + id / 2, 'b')
    fill_between(z, opt + mid + od / 2, opt + mid + id / 2, color='gray', alpha=0.5)
    plot(z, opt + mid, 'g')
    plot(z, opt + mid - id / 2, 'b')
    plot(z, opt + mid - od / 2, 'b')
    fill_between(z, opt + mid - od / 2, opt + mid - id / 2, color='gray', alpha=0.5)
    plot(z, low + mid, 'r.')
    show()

print(f'BHA SYS PRO sag correction at 7.85 m is -0.15 deg')
print(f'Sag at {bha.dni_to_bit} m is {r.sag * 180 / pi:.3f} deg')
print(f'Calculation time {t} s')
