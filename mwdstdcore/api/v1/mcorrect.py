from typing import List, Optional
import jsons
import attr
import numpy as np

from .core import api
from ..utils import json_call
from ..apierror import RequestMalformed

from mwdstdcore.datamodel import DnIParams, Reference, Survey, Qc, QcBoundary, BHA, RefParams
from mwdstdcore.datamodel.cor_survey import ManualCorrectedSurvey
from mwdstdcore.datamodel.calc.station import calc_station, calc_corrected_station, calc_gbd
from mwdstdcore.datamodel.ref import get_default_boundaries
from mwdstdcore.auto.autocor import remap
from mwdstdcore.core.common.srvmath import dni_correct
from mwdstdcore.errormods.gmagmod import gmagmod
from mwdstdcore.msa.qc import qc as fac


@attr.s(auto_attribs=True)
class Params:
    dni_cs: DnIParams
    surveys: List[Survey]
    reference: List[Reference]
    sag: Optional[List[float]] = None
    geomag: str = None
    ref_cs: RefParams = None
    bha: Optional[BHA] = None


@api.route('/mcorrect', methods=['POST'])
@json_call
def api_mcorrect(jsn):
    try:
        rq: Params = jsons.load(jsn, Params)
    except:
        raise RequestMalformed

    if rq.sag is None:
        rq.sag = [0.] * len(rq.surveys)
    
    if rq.geomag is not None:
        rq.geomag = rq.geomag.upper()
    
    stations = [calc_station(s, r.dec, r.grid) for s, r in zip(rq.surveys, rq.reference)]
    mds = [s.md for s in rq.surveys]
    dni_xyz = np.array([[s.gx, s.gy, s.gz, s.bx, s.by, s.bz] for s in rq.surveys])
    dni_xyz_cor = dni_correct(dni_xyz, rq.dni_cs.toarray())
    cor_surveys = ManualCorrectedSurvey.listFromArrays(mds, dni_xyz_cor)
    cor_stations = [calc_corrected_station(s, st, r.dec, r.grid, sg)
                    for s, st, r, sg in zip(cor_surveys, stations, rq.reference, rq.sag)]

    if rq.ref_cs is not None and rq.geomag in gmagmod:
        [bnd, bnd_norm] = fac(dni_xyz_cor, np.array([[r.g, r.b, r.dip] for r in rq.reference]), rq.ref_cs.toarray(),
                              ref_mod=gmagmod[rq.geomag])
        sqc = remap(np.array(mds), bnd_norm)
        for i, (su, r) in enumerate(zip(cor_surveys, rq.reference)):
            gbd = calc_gbd(su)
            su.min = QcBoundary(g=r.g + bnd[i, 1], b=r.b + bnd[i, 3], dip=r.dip + bnd[i, 5])
            su.max = QcBoundary(g=r.g + bnd[i, 0], b=r.b + bnd[i, 2], dip=r.dip + bnd[i, 4])
            su.qc_pass = Qc.fromValBnd(gbd, su.min, su.max)
            su.qc = sqc[i]
    else:
        bnd = get_default_boundaries()

        for su, r in zip(cor_surveys, rq.reference):
            gbd = calc_gbd(su)
            su.min = QcBoundary(g=r.g - bnd.g, b=r.b - bnd.b, dip=r.dip - bnd.dip)
            su.max = QcBoundary(g=r.g + bnd.g, b=r.b + bnd.b, dip=r.dip + bnd.dip)
            su.qc_pass = Qc.fromValBnd(gbd, su.min, su.max)
            su.qc = 0 if su.qc_pass.g and su.qc_pass.b and su.qc_pass.dip else 2
        
    return {'surveys': cor_surveys, 'stations': cor_stations}
