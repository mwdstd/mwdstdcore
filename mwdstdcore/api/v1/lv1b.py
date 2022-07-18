from typing import List, Optional
import jsons
import attr

from .core import api
from ..utils import json_call
from ..apierror import RequestMalformed

from .models import Run0 as Run, Reference
from .qc_plan import qc_plan
from .msa import msa_basic

import mwdstdcore.datamodel as rs


@attr.s(auto_attribs=True)
class Params:
    runs: List[Run]
    geomag: str
    head_ref: Reference
    plan: Optional[List[rs.Station]] = None


@attr.s(auto_attribs=True)
class Result:
    corrections: List[Optional[rs.Correction]]


@api.route('/lv1b', methods=['POST'])
@json_call
def api_lv1b(jsn):
    try:
        rq: Params = jsons.load(jsn, Params)
    except:
        raise RequestMalformed

    msa = msa_basic(rq.runs, rq.geomag)

    qc_plan(msa, rq.plan)

    return Result(msa)
