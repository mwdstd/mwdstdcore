import numpy as np


# setup function for delta calculation
def set_delta_func(particle_num: int, survey_num: int, err_term_num: int):
    if err_term_num != 0:
        bayes = True
    else:
        bayes = False
    dev_vector = np.zeros((3 * survey_num + err_term_num, particle_num))  # solution deviation vector

    # delta vector vectorized calculation: optimized for PSO
    def v_delta(dni_xyz: np.ndarray, ref: np.ndarray, cor_set=np.zeros(0)):
        g = np.sqrt(dni_xyz[:, :, 0] ** 2 + dni_xyz[:, :, 1] ** 2 + dni_xyz[:, :, 2] ** 2)
        b = np.sqrt(dni_xyz[:, :, 3] ** 2 + dni_xyz[:, :, 4] ** 2 + dni_xyz[:, :, 5] ** 2)
        d = np.arcsin((dni_xyz[:, :, 0] * dni_xyz[:, :, 3] + dni_xyz[:, :, 1] * dni_xyz[:, :, 4] +
                       dni_xyz[:, :, 2] * dni_xyz[:, :, 5]) / g / b)
        dev_vector[0:survey_num, :] = (ref[:, :, 0] - g).T
        dev_vector[survey_num:2 * survey_num, :] = (ref[:, :, 1] - b).T
        dev_vector[2 * survey_num:3 * survey_num, :] = (ref[:, :, 2] - d).T

        if bayes:
            dev_vector[-err_term_num:, :] = cor_set

        return dev_vector

    return v_delta


# stand alone PSO vectorized delta function
def vect_delta(dni_xyz: np.ndarray, ref: np.ndarray, cor_set: np.ndarray = np.zeros(0)):
    particle_num = dni_xyz.shape[0]
    survey_num = dni_xyz.shape[1]
    err_term_num = cor_set.shape[0]
    if err_term_num != 0:
        bayes = True
    else:
        bayes = False
    dev_vector = np.zeros((3 * survey_num + err_term_num, particle_num))  # solution deviation vector

    g = np.sqrt(dni_xyz[:, :, 0] ** 2 + dni_xyz[:, :, 1] ** 2 + dni_xyz[:, :, 2] ** 2)
    b = np.sqrt(dni_xyz[:, :, 3] ** 2 + dni_xyz[:, :, 4] ** 2 + dni_xyz[:, :, 5] ** 2)
    d = np.arcsin((dni_xyz[:, :, 0] * dni_xyz[:, :, 3] + dni_xyz[:, :, 1] * dni_xyz[:, :, 4] +
                   dni_xyz[:, :, 2] * dni_xyz[:, :, 5]) / g / b)
    dev_vector[0:survey_num, :] = (ref[:, :, 0] - g).T
    dev_vector[survey_num:2 * survey_num, :] = (ref[:, :, 1] - b).T
    dev_vector[2 * survey_num:3 * survey_num, :] = (ref[:, :, 2] - d).T

    if bayes:
        dev_vector[-err_term_num:, :] = cor_set

    return dev_vector
