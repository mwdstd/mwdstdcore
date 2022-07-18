import numpy as np


# vectorized differential evolution algorithm
def de(qfunc, min_pos, max_pos, particle_num=250, boxed=True):
    # algorithm parameters
    init = True
    num_of_particles = particle_num
    num_of_dim = min_pos.shape[0]  # number of dimensions of the problem
    max_iter_num = 10000
    diff_weight = 0.4
    crossover_prob = 0.9
    next_gen_prob = 0.05
    mutation_prob = 0.01

    # algorithm init
    index = np.arange(0, num_of_particles)
    particles_pos_cur = (max_pos - min_pos) * np.random.rand(num_of_dim, num_of_particles) + min_pos
    # particles_pos_new = np.zeros_like(particles_pos_cur)

    # add zero initial position to random variety
    # zero_pos = (max_pos + min_pos) / 2.
    # particles_pos_cur[:, 0] = zero_pos[:, 0]

    particles_err_cur = (qfunc(particles_pos_cur)).copy()
    # particles_err_new = np.zeros_like(particles_err_cur)

    global_best_err = -1
    global_best_pos = np.zeros((num_of_dim, 1))

    # convergence setup
    convergence_delay = 125
    convergence_dist = 1e-9
    delay = convergence_delay
    previous_global_best_pos = np.zeros((num_of_dim, 1))

    # optimization loop
    i = 0
    while i < max_iter_num:
        previous_global_best_pos[:, 0] = global_best_pos[:, 0]

        # intermediate multivector: v = v1 + F * (v2 - v3)
        np.random.shuffle(index)
        particles_pos_new = particles_pos_cur[:, index]
        np.random.shuffle(index)
        particles_pos_new += diff_weight * particles_pos_cur[:, index]
        np.random.shuffle(index)
        particles_pos_new -= diff_weight * particles_pos_cur[:, index]
        # crossover current multivector with intermediate one
        crossover_mask = (np.random.rand(num_of_dim, num_of_particles) < crossover_prob)
        particles_pos_new = np.logical_not(crossover_mask) * particles_pos_cur + crossover_mask * particles_pos_new
        # mutate current multivector
        mutation_mask = (np.random.rand(num_of_dim, num_of_particles) < mutation_prob)
        mutation_vect = (max_pos - min_pos) * np.random.rand(num_of_dim, num_of_particles) + min_pos
        particles_pos_new = np.logical_not(mutation_mask) * particles_pos_new + mutation_mask * mutation_vect
        if boxed:
            test_min = (particles_pos_new < min_pos)
            particles_pos_new = test_min * min_pos + np.logical_not(test_min) * particles_pos_new
            test_max = (particles_pos_new > max_pos)
            particles_pos_new = test_max * max_pos + np.logical_not(test_max) * particles_pos_new
        particles_err_new = qfunc(particles_pos_new)
        # update positions
        next_gen_mask = (np.random.rand(1, num_of_particles) < next_gen_prob)
        mask = np.reshape((particles_err_new < particles_err_cur), (1, num_of_particles))
        mask = np.logical_or(mask, next_gen_mask)
        particles_pos_cur = np.logical_not(mask) * particles_pos_cur + mask * particles_pos_new
        particles_err_cur = np.logical_not(mask) * particles_err_cur + mask * particles_err_new

        # find global best position and error
        index_of_min_err = np.argmin(particles_err_cur)
        iter_min_err = particles_err_cur[0, index_of_min_err]
        if init or global_best_err >= iter_min_err:
            init = False
            global_best_err = iter_min_err
            global_best_pos[:, 0] = particles_pos_cur[:, index_of_min_err]

        # check for convergence criteria
        dist = np.linalg.norm(global_best_pos - previous_global_best_pos)
        if dist <= convergence_dist:
            delay -= 1
            if delay == 0:
                break
        else:
            delay = convergence_delay
        i += 1

    return [global_best_pos, global_best_err]
