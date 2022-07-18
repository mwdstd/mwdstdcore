from math import radians as deg2rad, degrees
from time import time
import numpy as np
from matplotlib.pyplot import plot, fill, show, gca
from mwdstdcore.datamodel.bha import BHA, BhaElement, BhaElementType, Material
from mwdstdcore.datamodel.station import Station
from mwdstdcore.sag.sagcor import sagcor


def traj_points(z, md_bit, traj):
    md = np.flip(traj[:, 0])
    inc = np.flip(traj[:, 1])
    md = -(md - md_bit)  # revert md to z coordinate
    inc_hd = np.interp(z, md, inc)
    sins = np.sin(inc_hd)
    coss = np.cos(inc_hd)
    dz = z[1] - z[0]
    return np.cumsum([sins * dz, coss * dz], axis=1), np.array([-coss, sins])


inc_test_deg = 90
tf = 180.

traj = [[950., deg2rad(inc_test_deg)],
        [980., deg2rad(inc_test_deg)],
        [990., deg2rad(inc_test_deg)],
        [1000., deg2rad(inc_test_deg)]]
traj = [[950., deg2rad(inc_test_deg - 15.)],
        [980., deg2rad(inc_test_deg)],
        [990., deg2rad(inc_test_deg)],
        [1000., deg2rad(inc_test_deg - 5.)]]
# traj = [[950., deg2rad(inc_test_deg - 100.)],
#         [970., deg2rad(inc_test_deg)],
#         [980., deg2rad(inc_test_deg)],
#         [1000., deg2rad(inc_test_deg + 100.)]]
bh_design = [[0., 975., 0.300], [975., 2000., 0.220]]
bh_design = None
md = traj[-1][0]
mud_weight = 1200
wob = 0.e5  # N

traj = [Station(st[0], st[1], 0.) for st in traj]

bha = BHA(
    [BhaElement(BhaElementType.mwd, 0.173, 0.1, 1400, 100, Material.nm_steel)],
    [], 25.
)
ss = 10.
bh_design = [[0., 1100., 3]]

for el in bha.structure:
    el.id *= ss
    el.od *= ss
    el.weight *= ss * ss
for el in bha.blades:
    el.od *= ss

t = time()
r = sagcor(bha, md, traj, deg2rad(tf), mud_weight, wob, borehole_design=bh_design)
t = time() - t
print(f'Time: {t} sec')
print(f'Sag: {degrees(r.sag)} deg')
print(f'Valid: {r.valid}')

z = r.grid
# sag = np.arctan((r.opt[1:] - r.opt[:-1]) / (z[1:] - z[:-1])) * 180 / pi
# plot(z[1:], sag, 'g.')
# if True:
#     # plot(z, r.top, 'r')
#     # plot(z, r.opt + r.od / 2, 'b')
#     # plot(z, r.opt + r.id / 2, 'b')
#     # fill_between(z, r.opt + r.od / 2, r.opt + r.id / 2, color='gray', alpha=0.5)
#     # plot(z, r.opt, 'g')
#     # plot(z, r.opt - r.id / 2, 'b')
#     # plot(z, r.opt - r.od / 2, 'b')
#     # fill_between(z, r.opt - r.od / 2, r.opt - r.id / 2, color='gray', alpha=0.5)
#     # plot(z, r.low, 'r')
gca().set_aspect('equal')
pts, ns = traj_points(z, md, np.asarray([[st.md, st.inc] for st in traj]))
a = 1
scale = 1.
plot(pts[0], pts[1])
plot(pts[0] + scale * r.top * ns[0], pts[1] + scale * r.top * ns[1], 'r-')
plot(pts[0] + scale * r.low * ns[0], pts[1] + scale * r.low * ns[1], 'r-')
plot(pts[0] + scale * r.opt * ns[0], pts[1] + scale * r.opt * ns[1], 'g-')
outer_top_x = pts[0] + scale * (r.opt + r.od / 2) * ns[0]
outer_top_y = pts[1] + scale * (r.opt + r.od / 2) * ns[1]
outer_btm_x = pts[0] + scale * (r.opt - r.od / 2) * ns[0]
outer_btm_y = pts[1] + scale * (r.opt - r.od / 2) * ns[1]
inner_top_x = pts[0] + scale * (r.opt + r.id / 2) * ns[0]
inner_top_y = pts[1] + scale * (r.opt + r.id / 2) * ns[1]
inner_btm_x = pts[0] + scale * (r.opt - r.id / 2) * ns[0]
inner_btm_y = pts[1] + scale * (r.opt - r.id / 2) * ns[1]

plot(outer_btm_x, outer_btm_y, 'b-')
plot(outer_top_x, outer_top_y, 'b-')
plot(inner_top_x, inner_top_y, 'b-')
plot(inner_btm_x, inner_btm_y, 'b-')

fill(np.concatenate((outer_btm_x, np.flip(inner_btm_x))), np.concatenate((outer_btm_y, np.flip(inner_btm_y))),
     color='gray', alpha=0.5)
fill(np.concatenate((outer_top_x, np.flip(inner_top_x))), np.concatenate((outer_top_y, np.flip(inner_top_y))),
     color='gray', alpha=0.5)

show()

