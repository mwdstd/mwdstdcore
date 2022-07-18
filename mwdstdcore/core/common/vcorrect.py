import numpy as np


# vectorized DnI correction of multiple survey sets without failed axis correction; optimization for PSO
def vect_dni_cor(dni_xyz: np.ndarray, dni_cor: np.ndarray):
    particle_num = dni_xyz.shape[0]
    dni_xyz_cor = np.empty_like(dni_xyz)
    b_xyz = np.empty_like(dni_xyz[:, :, 0:3])
    one = np.ones((particle_num, 1))

    # accels' correction for sf and biases
    abx = np.reshape(dni_cor[0, :], (particle_num, 1))
    aby = np.reshape(dni_cor[1, :], (particle_num, 1))
    abz = np.reshape(dni_cor[2, :], (particle_num, 1))
    asx = np.reshape(dni_cor[3, :], (particle_num, 1)) + one
    asy = np.reshape(dni_cor[4, :], (particle_num, 1)) + one
    asz = np.reshape(dni_cor[5, :], (particle_num, 1)) + one
    dni_xyz_cor[:, :, 0] = dni_xyz[:, :, 0] / asx - abx
    dni_xyz_cor[:, :, 1] = dni_xyz[:, :, 1] / asy - aby
    dni_xyz_cor[:, :, 2] = dni_xyz[:, :, 2] / asz - abz

    # mags' correction for sf and biases
    mbx = np.reshape(dni_cor[6, :], (particle_num, 1))
    mby = np.reshape(dni_cor[7, :], (particle_num, 1))
    mbz = np.reshape(dni_cor[8, :], (particle_num, 1))
    msx = np.reshape(dni_cor[9, :], (particle_num, 1)) + one
    msy = np.reshape(dni_cor[10, :], (particle_num, 1)) + one
    msz = np.reshape(dni_cor[11, :], (particle_num, 1)) + one
    b_xyz[:, :, 0] = dni_xyz[:, :, 3] / msx - mbx
    b_xyz[:, :, 1] = dni_xyz[:, :, 4] / msy - mby
    b_xyz[:, :, 2] = dni_xyz[:, :, 5] / msz - mbz

    # misalignment correction
    mxy = np.reshape(dni_cor[12, :], (particle_num, 1))
    mxz = np.reshape(dni_cor[13, :], (particle_num, 1))
    myz = np.reshape(dni_cor[14, :], (particle_num, 1))
    dni_xyz_cor[:, :, 3] = b_xyz[:, :, 0] - mxy * b_xyz[:, :, 1] - mxz * b_xyz[:, :, 2]
    dni_xyz_cor[:, :, 4] = b_xyz[:, :, 1] + mxy * b_xyz[:, :, 0] - myz * b_xyz[:, :, 2]
    dni_xyz_cor[:, :, 5] = b_xyz[:, :, 2] + mxz * b_xyz[:, :, 0] + myz * b_xyz[:, :, 1]
    return dni_xyz_cor


# vectorized reference correction of multiple survey sets without failed axis correction; optimization for PSO
def vect_ref_cor(ref: np.ndarray, ref_cor: np.ndarray):
    particle_num = ref.shape[0]
    ref_corrected = np.empty_like(ref)

    g_cor = np.reshape(ref_cor[0, :], (particle_num, 1))
    b_cor = np.reshape(ref_cor[1, :], (particle_num, 1))
    d_cor = np.reshape(ref_cor[2, :], (particle_num, 1))
    ref_corrected[:, :, 0] = ref[:, :, 0] - g_cor
    ref_corrected[:, :, 1] = ref[:, :, 1] - b_cor
    ref_corrected[:, :, 2] = ref[:, :, 2] - d_cor

    return ref_corrected
