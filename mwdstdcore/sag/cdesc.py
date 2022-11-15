from math import sin, sqrt


def coord_descent(xs, e, q, od, xl, xu, dz, bi, ba, eps):
    g = 9.81
    sdx = 1.e0
    mi = 3000000

    b = xl + od / 2.
    t = xu - od / 2.
    x = xs.copy()

    if bi <= 0:
        bi = -10
        ba = 0.
    db = sin(ba) / dz

    ni = 0
    eln = e.shape[0]
    while sqrt(sdx) > eps and ni < mi:
        ni += 1
        sdx = 0.
        for i in range(0, eln - 1):
            if i == 0:
                d0 = 0.
                d1 = 0.
                d2 = (x[i + 2] + x[i] - 2 * x[i + 1]) / dz ** 2
                e0 = 0.
                e1 = e[i]
                e2 = e[i + 1]
            elif i == 1:
                d0 = 0.
                d1 = (x[i + 1] + x[i - 1] - 2 * x[i]) / dz ** 2
                d2 = (x[i + 2] + x[i] - 2 * x[i + 1]) / dz ** 2
                e0 = e[i - 1]
                e1 = e[i]
                e2 = e[i + 1]
            elif i == eln - 2:
                d0 = (x[i] + x[i - 2] - 2 * x[i - 1]) / dz ** 2
                d1 = (x[i + 1] + x[i - 1] - 2 * x[i]) / dz ** 2
                d2 = 0.
                e0 = e[i - 1]
                e1 = e[i]
                e2 = e[i + 1]
            else:
                d0 = (x[i] + x[i - 2] - 2 * x[i - 1]) / dz ** 2 - (db if i == bi + 1 else 0.)
                d1 = (x[i + 1] + x[i - 1] - 2 * x[i]) / dz ** 2 - (db if i == bi else 0.)
                d2 = (x[i + 2] + x[i] - 2 * x[i + 1]) / dz ** 2 - (db if i == bi - 1 else 0.)
                e0 = e[i - 1]
                e1 = e[i]
                e2 = e[i + 1]

            dx = dz ** 2 * ((2 * e1 * d1 - e2 * d2 - e0 * d0) - q[i] * g * dz ** 2) / (e0 + 4 * e1 + e2)

            dx = t[i] - x[i] if (x[i] + dx > t[i]) else dx
            dx = b[i] - x[i] if (x[i] + dx < b[i]) else dx
            x[i] += dx
            sdx += dx * dx

    return x, 1 if ni < mi else 0
