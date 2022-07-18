from math import pi
from time import time
import numpy as np
from numpy.linalg import inv
from matplotlib.pyplot import plot, show
from mwdstdcore.sag.cdesc import coord_descent


def solver(od_bit, od, q, ei, z_max):
    obs_vect = np.asarray([[od_bit/2],
                           [od/2 + q*z_max**4/(24*ei)],
                           [q*z_max**3/(6*ei)],
                           [q*z_max**2/(2*ei)],
                           [od_bit/2 + (q/24/ei)*0.1**4],
                           [od_bit/2 + (q/24/ei)*0.05**4]])
    obs_mat = np.asarray([[1., 0., 0., 0.],
                          [1., z_max, z_max**2, z_max**3],
                          [0., 1., 2.*z_max, 3.*z_max**2],
                          [0., 0., 2., 6.*z_max],
                          [1., 0.1, 0.1**2, 0.1**3],
                          [1., 0.05, 0.05**2, 0.05**3]])
    p = inv(obs_mat.T @ obs_mat) @ obs_mat.T @ obs_vect
    return p


def x_z(z, p, q, ei):
    x = p[0, 0] + p[1, 0] * z + p[2, 0] * z ** 2 + p[3, 0] * z ** 3 - (q / 24 / ei) * z ** 4
    return x


# solve the problem by static equilibrium method
dz = 0.1
L_bit = 0.1
L_mwd = 7.1
OD_bit = 0.16
OD = 0.12
ID = 0.04
J = pi * (OD ** 4 - ID ** 4) / 64
e_stl = 2.e11
EJ = e_stl * J
ro_steel = 7800
ro_mud = 1200
Q = pi * (ro_steel - ro_mud) * (OD ** 2 - ID ** 2) / 4
L = L_mwd + L_bit

P = solver(OD_bit, OD, Q, EJ, L)
num = int(L/dz) + 1
Z = np.linspace(0, L, num)
X = x_z(Z, P, Q, EJ)
sag_force = 180 / pi * (X[1:] - X[:-1]) / dz
# plot(Z[1:], sag_force, 'g')
plot(Z, X, 'g')

# solve the problem by energy minimization
bit_ind = int(L_bit / dz)
num = int((L_bit + L_mwd) / dz) + 1
z = np.cumsum(dz * np.ones(num)) - dz

upper_wall = 1.04 * OD_bit * np.ones(num)
lower_wall = 0. * np.ones(num)

ei = np.zeros(num)
ei[:] = EJ

linear_weight = np.zeros(num)
linear_weight[:] = Q

dls_offset = np.zeros_like(ei)

outer_diameter = np.zeros(num)
outer_diameter[:bit_ind] = OD_bit
outer_diameter[bit_ind:] = OD

x0 = lower_wall + outer_diameter / 2

t = time()
x_opt = coord_descent(x0, ei, linear_weight, outer_diameter, lower_wall, upper_wall, dz=dz,
                      bi=0, ba=0., do=dls_offset, wob=0., eps=1.e-10)
t = time() - t
sag_energy = 180 / pi * (x_opt[1:] - x_opt[:-1]) / dz
# plot(z[1:], sag_energy, 'r')
plot(z, x_opt, 'r')
show()
