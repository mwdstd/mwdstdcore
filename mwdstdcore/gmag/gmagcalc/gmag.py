from typing import Tuple
from mwdstdcore.gmag.maglib.date import Date
from mwdstdcore.gmag.maglib.magsetup import MagSetup
from mwdstdcore.gmag.maglib.magmod import MagneticModel
from mwdstdcore.gmag.gmagcalc.sphharm import SphericalHarmonicVariables
from mwdstdcore.gmag.gmagcalc.legfunc import LegendreFunction
from mwdstdcore.gmag.gmagcalc.magres import MagneticResults
from mwdstdcore.gmag.gmagcalc.grad import Gradient
from mwdstdcore.gmag.gmagcalc.magelement import GeoMagneticElement
from mwdstdcore.gmag.geolib.geoidcoord import CoordGeodetic
from mwdstdcore.gmag.geolib.sphcoord import CoordSpherical
from mwdstdcore.gmag.geolib.localcoord import CoordLocal
from mwdstdcore.gmag.geolib.utm import UTMParameters, PS_MAX_LAT_DEGREE, PS_MIN_LAT_DEGREE
from math import radians as deg2rad, degrees as rad2deg, sqrt, cos, sin


def gravity(latitude: float) -> float:
    lat = deg2rad(latitude)
    total_g = 9.7803253359 * (1 + 0.00193185265241 * sin(lat) ** 2) / sqrt(1 - 0.00669437999013 * sin(lat) ** 2)
    return total_g


def grid_conv(latitude: float, longitude: float) -> float:
    geodetic_coords = CoordGeodetic(lat=latitude, long=longitude, alt=0., altitude_type='MSL')
    utm = UTMParameters()
    utm.get_transverse_mercator(geodetic_coords)
    grid = utm.ConvergenceOfMeridians
    return deg2rad(grid)


def gmag_point(latitude: float, longitude: float, altitude: float, date: Date, altitude_type='MSL',
               gmag_mod='WMM2020', crustal_field=False) -> GeoMagneticElement:
    mag_model = MagSetup.get_mag_model(date, gmag_mod=gmag_mod, crustal_field=crustal_field)

    geodetic_coords = CoordGeodetic(lat=latitude, long=longitude, alt=altitude, altitude_type=altitude_type)
    spherical_coords = geodetic_coords.geodetic_to_spherical()

    geo_mag_element = common_gmag_calc(geodetic_coords, spherical_coords, mag_model)

    return geo_mag_element


def gmag_traj(latitude: float, longitude: float, altitude: float, date: Date, local_points: list,
              altitude_type='MSL', gmag_mod='WMM2020', crustal_field=False) -> list:
    if not (-85. <= latitude <= 85):
        raise Exception('Method gmag_traj(): latitude out of range')

    gmag_elements = []

    mag_model = MagSetup.get_mag_model(date, gmag_mod=gmag_mod, crustal_field=crustal_field)

    geodetic_coords = CoordGeodetic(lat=latitude, long=longitude, alt=altitude, altitude_type=altitude_type)
    spherical_coords = geodetic_coords.geodetic_to_spherical()

    point: CoordLocal
    for point in local_points:
        dlat = rad2deg(point.NS / 1000 / spherical_coords.R)
        dlong = rad2deg(point.EW / 1000 / (spherical_coords.R * cos(deg2rad(spherical_coords.Phig))))
        dalt = -point.TVD / 1000
        cur_geodetic_coords = CoordGeodetic(lat=latitude + dlat, long=longitude + dlong, alt=altitude + dalt,
                                            altitude_type=altitude_type)
        cur_spherical_coords = cur_geodetic_coords.geodetic_to_spherical()
        gmag_element = common_gmag_calc(cur_geodetic_coords, cur_spherical_coords, mag_model)
        gmag_elements.append(gmag_element)

    return gmag_elements


def gmag_grad(latitude: float, longitude: float, altitude: float, date: Date, altitude_type='MSL',
              gmag_mod='WMM2020', crustal_field=False) -> Tuple[GeoMagneticElement, Gradient]:
    gradient = Gradient()
    phiDelta = 0.01
    hDelta = -1
    x = [0., 0.]
    y = [0., 0.]
    z = [0., 0.]

    mag_model = MagSetup.get_mag_model(date, gmag_mod=gmag_mod, crustal_field=crustal_field)
    geodetic_coords = CoordGeodetic(lat=latitude, long=longitude, alt=altitude, altitude_type=altitude_type)
    spherical_coords = geodetic_coords.geodetic_to_spherical()
    gmag_element_zero = common_gmag_calc(geodetic_coords, spherical_coords, mag_model)
    gmag_elements = [GeoMagneticElement(), GeoMagneticElement()]
    adj_geodetic_coords = geodetic_coords.clone()

    adj_geodetic_coords.Phi = geodetic_coords.Phi + phiDelta
    adj_spherical_coords = adj_geodetic_coords.geodetic_to_spherical()
    gmag_elements[0] = common_gmag_calc(adj_geodetic_coords, adj_spherical_coords, mag_model)
    [x[0], y[0], z[0]] = UTMParameters.spherical2cartesian(adj_spherical_coords)

    adj_geodetic_coords.Phi = geodetic_coords.Phi - phiDelta
    adj_spherical_coords = adj_geodetic_coords.geodetic_to_spherical()
    gmag_elements[1] = common_gmag_calc(adj_geodetic_coords, adj_spherical_coords, mag_model)
    [x[1], y[1], z[1]] = UTMParameters.spherical2cartesian(adj_spherical_coords)

    distance = sqrt((x[0] - x[1]) ** 2 + (y[0] - y[1]) ** 2 + (z[0] - z[1]) ** 2)
    gradient.set_component('north', gmag_elements, distance)
    adj_geodetic_coords = geodetic_coords.clone()

    adj_spherical_coords = geodetic_coords.geodetic_to_spherical()
    gradient.GradLambda = __grad_y(geodetic_coords, adj_spherical_coords, mag_model, gmag_element_zero)

    adj_geodetic_coords.HeightAboveEllipsoid = geodetic_coords.HeightAboveEllipsoid + hDelta
    adj_geodetic_coords.HeightAboveGeoid = geodetic_coords.HeightAboveGeoid + hDelta
    adj_spherical_coords = adj_geodetic_coords.geodetic_to_spherical()
    gmag_elements[0] = common_gmag_calc(adj_geodetic_coords, adj_spherical_coords, mag_model)
    [x[0], y[0], z[0]] = UTMParameters.spherical2cartesian(adj_spherical_coords)

    adj_geodetic_coords.HeightAboveEllipsoid = geodetic_coords.HeightAboveEllipsoid - hDelta
    adj_geodetic_coords.HeightAboveGeoid = geodetic_coords.HeightAboveGeoid - hDelta
    adj_spherical_coords = adj_geodetic_coords.geodetic_to_spherical()
    gmag_elements[1] = common_gmag_calc(adj_geodetic_coords, adj_spherical_coords, mag_model)
    [x[1], y[1], z[1]] = UTMParameters.spherical2cartesian(adj_spherical_coords)

    distance = sqrt((x[0] - x[1]) ** 2 + (y[0] - y[1]) ** 2 + (z[0] - z[1]) ** 2)
    gradient.set_component('down', gmag_elements, distance)

    return [gmag_element_zero, gradient]


def __grad_y(geodetic_coords: CoordGeodetic, spherical_coords: CoordSpherical, mag_model: MagneticModel,
             gmag_element: GeoMagneticElement) -> GeoMagneticElement:
    sph_harmonics = SphericalHarmonicVariables(mag_model=mag_model, spherical_coords=spherical_coords)
    legendre_func = LegendreFunction(mag_model=mag_model, spherical_coords=spherical_coords)
    grad_y_vect = MagneticResults(mag_model=mag_model, spherical_coords=spherical_coords,
                                  sph_harmonics=sph_harmonics, legendre_func=legendre_func, mode='grad_y')
    grad_y_vect.rotate(geodetic_coords)
    grad_y = GeoMagneticElement()
    grad_y.X = grad_y_vect.Bx
    grad_y.Y = grad_y_vect.By
    grad_y.Z = grad_y_vect.Bz

    grad_y.H = (grad_y.X * gmag_element.X + grad_y.Y * gmag_element.Y) / gmag_element.H
    grad_y.F = (grad_y.X * gmag_element.X + grad_y.Y * gmag_element.Y + grad_y.Z * gmag_element.Z) / gmag_element.F
    grad_y.Decl = rad2deg((gmag_element.X * grad_y.Y - gmag_element.Y * grad_y.X) / (gmag_element.H * gmag_element.H))
    grad_y.Incl = rad2deg((gmag_element.H * grad_y.Z - gmag_element.Z * grad_y.H) / (gmag_element.F * gmag_element.F))
    grad_y.GV = grad_y.Decl
    return grad_y


def common_gmag_calc(geodetic_coords: CoordGeodetic, spherical_coords: CoordSpherical, mag_model: MagneticModel) -> \
        GeoMagneticElement:
    sph_harmonics = SphericalHarmonicVariables(mag_model=mag_model, spherical_coords=spherical_coords)

    legendre_func = LegendreFunction(mag_model=mag_model, spherical_coords=spherical_coords)

    mag_geo = MagneticResults(mag_model=mag_model, spherical_coords=spherical_coords,
                              sph_harmonics=sph_harmonics, legendre_func=legendre_func, mode='geo')
    mag_var = MagneticResults(mag_model=mag_model, spherical_coords=spherical_coords,
                              sph_harmonics=sph_harmonics, legendre_func=legendre_func, mode='var')

    mag_geo.rotate(geodetic_coords)
    mag_var.rotate(geodetic_coords)

    geo_mag_element = GeoMagneticElement(mag_geo=mag_geo, mag_var=mag_var)

    if geodetic_coords.Phi >= PS_MAX_LAT_DEGREE:
        geo_mag_element.GV = geo_mag_element.Decl - deg2rad(geodetic_coords.Lambda)
    elif geodetic_coords.Phi <= PS_MIN_LAT_DEGREE:
        geo_mag_element.GV = geo_mag_element.Decl + deg2rad(geodetic_coords.Lambda)
    else:
        utm_coords = UTMParameters()
        utm_coords.get_transverse_mercator(geodetic_coords)
        geo_mag_element.GV = geo_mag_element.Decl - utm_coords.ConvergenceOfMeridians

    return geo_mag_element
