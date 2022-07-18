from typing import List
from math import sqrt, pi
import numpy as np
from mwdstdcore.datamodel import BHA, Material


bha_element = {'od': 0., 'id': 0., 'length': 0., 'weight': 0., 'mat': 0.}
stab_blades = {'od': 0., 'length': 0., 'dist2bit': 0.}


def bha2input(bha: BHA, dz: float):
    ro_steel = 7850  # kg/m3
    e_steel = 2.05e11  # Young's modulus for construction steel
    e_nmag = 1.90e11  # Young's modulus for non-magnetic steel
    dni2uphole = 25.  # m

    # map cumulative length
    cum_length = []
    length = 0.
    for elmnt in bha.structure:
        length += elmnt.length
        cum_length.append(length)

    # stabilizer conversion
    blade_pos: List[int] = []
    blade_length: List[int] = []
    blade_od: List[float] = []
    for blade in bha.blades:
        blade_length.append(1. if round(blade.length / dz) == 0. else round(blade.length / dz))
        blade_pos.append(round(blade.center_to_bit / dz))
        blade_od.append(blade.od)

    # convert BHA elements to finite elements
    young_modulus = []
    apparent_inner_diameter = []
    linear_weight = []
    outer_diameter = []
    inner_diameter = []

    model_length = dz / 2
    num_elmnt = len(bha.structure)
    elmnt_ind = 0
    while elmnt_ind < num_elmnt:
        young_modulus.append(e_steel if bha.structure[elmnt_ind].material == Material.steel else e_nmag)
        OD = bha.structure[elmnt_ind].od
        Q = bha.structure[elmnt_ind].weight / bha.structure[elmnt_ind].length
        ID2 = OD ** 2 - 4 * Q / pi / ro_steel
        ID = sqrt(ID2) if ID2 > 0. else 0.

        outer_diameter.append(OD)
        linear_weight.append(Q)
        apparent_inner_diameter.append(ID)
        inner_diameter.append(bha.structure[elmnt_ind].id)

        model_length += dz
        if model_length >= cum_length[elmnt_ind]:
            elmnt_ind += 1

        # get only dni2uphole offset above D&I
        if model_length > bha.dni_to_bit + dni2uphole + dz:
            break
    young_modulus = np.asarray(young_modulus)
    outer_diameter = np.asarray(outer_diameter)
    linear_weight = np.asarray(linear_weight)
    apparent_inner_diameter = np.asarray(apparent_inner_diameter)
    inner_diameter = np.asarray(inner_diameter)
    inertia_momentum = pi * (outer_diameter ** 4 - apparent_inner_diameter ** 4) / 64.

    # add stabilizers' blades
    num_stab = len(bha.blades)
    for ind in range(0, num_stab):
        start = blade_pos[ind]
        stop = blade_pos[ind] + int(blade_length[ind])
        if stop >= outer_diameter.shape[0]:
            continue
        inertia_momentum[start:stop] += (blade_od[ind] ** 3 * outer_diameter[start] / 36 +
                                         blade_od[ind] * outer_diameter[start] ** 3 / 324)
        outer_diameter[start:stop] = blade_od[ind]

    ei = young_modulus * inertia_momentum

    # calculate bend position
    bend_ind = int(-10 if round(bha.bend_to_bit / dz) <= 0. else round(bha.bend_to_bit / dz))

    return [ei, outer_diameter, inner_diameter, linear_weight, bend_ind]
