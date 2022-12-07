from typing import List
from .models import Interval, Run0 as Run, ManualCorrectionIn
from ..logs import DebugTimer
from ..utils import getitem
import mwdstdcore.datamodel as rs
from mwdstdcore.auto.autocor import autocor
from mwdstdcore.auto.manualcor import manualcor


def msa_basic(runs: List[Run], geomag: str):
    msa = []
    for ri, run in enumerate(runs):
        if isinstance(run.correction, rs.Correction):
            corr = run.correction
        elif isinstance(run.correction, ManualCorrectionIn) or isinstance(run.correction, rs.ManualCorrection):
            corr = manualcor(rs.Run(
                    surveys=run.surveys, 
                    dni_rigid=run.dni_rigid, 
                    edi=0., 
                    reference=run.reference,
                    correction=run.correction
                ))
        else:
            with DebugTimer(f"MSA{ri}: {{:0.2f}}"):
                corr = autocor(
                    rs.Run(
                        surveys=run.surveys, 
                        dni_rigid=True,
                        edi=0., 
                        reference=run.reference, 
                        exti_interval=getitem(run.interference_intervals, 0, Interval()),
                        casing_depth=run.casing_depth
                    ), geomag.upper()
                )
        msa += [corr]
    return msa
