from typing import List, Optional
import jsons
import attr

from .core import api
from ..utils import json_call
from ..apierror import RequestMalformed

import mwdstdcore.datamodel as rs
from .models import Run2 as Run, Reference, Result0 as Result
from .sag import sag_basic
from .qc_plan import qc_plan
from .msa import msa_basic


@attr.s(auto_attribs=True)
class Params:
    runs: List[Run]
    geomag: str
    head_ref: Reference
    plan: Optional[List[rs.Station]] = None


@api.route('/lv2b', methods=['POST'])
@json_call
def api_lv2b(jsn):
    try:
        rq: Params = jsons.load(jsn, Params)
    except:
        raise RequestMalformed

    corrs = msa_basic(rq.runs, rq.geomag)

    sag_basic(rq.runs, corrs)
    qc_plan(corrs, rq.plan)
    
    return Result(corrs)
