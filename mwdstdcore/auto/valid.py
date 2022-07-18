import numpy as np
from mwdstdcore.errormods.dnistd import dni_std
from mwdstdcore.datamodel import QualityAssessment

MIN_SRV_CNT = 4


def validation(pre_qc, mag_qc, apr_unc, dni_cor, ref_cor, ref_mod, survey_status, inc_stat, az_stat, edi_val=0.,
               edi_unc=0.):
    res = QualityAssessment()
    pre_qc_indexes = np.argwhere(pre_qc).flatten()
    if pre_qc_indexes.shape[0] != 0:
        sqc = survey_status[pre_qc_indexes]
        mqc = mag_qc[pre_qc_indexes]
        pre_qc_ratio = float(np.sum((sqc == 0) * mqc + (sqc <= 1) * (~mqc))) / pre_qc_indexes.shape[0]
        res.expectation.value = True if pre_qc_ratio >= 0.8 else False
    else:
        res.expectation.value = None

    res.reference.value = True if (abs(ref_cor[0]) <= 2 * ref_mod['MGI'] and abs(ref_cor[1]) <= 2 * ref_mod['MBI'] and
                                   abs(ref_cor[2]) <= 2 * ref_mod['MDI']) else False
    res.correction_possibility.value = True if (apr_unc['MBX'] > dni_std['MBX'] and apr_unc['MBY'] > dni_std['MBY'] and
                                                apr_unc['MBZ'] > dni_std['MBZ']) else False
    res.model_comparison.value = True
    i = 0
    for e in dni_std:
        sigma = 2 * dni_std[e] if (e == 'MBZ' or e == 'MBX' or e == 'MBY') else dni_std[e]
        if e == 'MBZ' and edi_unc > 0.:
            right_bond = (edi_val + 3 * edi_unc) if edi_val >= 0. else (3 * edi_unc)
            left_bond = (edi_val - 3 * edi_unc) if edi_val < 0. else (-3 * edi_unc)
            if not ((left_bond <= dni_cor[i] <= right_bond) or abs(dni_cor[i]) <= 3 * sigma):
                res.model_comparison.value = False
        else:
            if abs(dni_cor[i]) > 3 * sigma:
                res.model_comparison.value = False
        i += 1
    # accuracy analysis
    std_indexes = np.argwhere(survey_status == 0).flatten()
    res.accuracy.value = bool(np.prod(inc_stat[std_indexes]) * np.prod(az_stat[std_indexes]))
    res.number_of_surveys.value = True if std_indexes.shape[0] >= MIN_SRV_CNT else False
    # TODO: exclude preqc_false
    if survey_status.shape[0] >= 5:
        res.sq_last.value = np.sum(survey_status[-5:] == 0) >= 3
        res.sq_last.severity = 1 if np.sum(survey_status[-5:] == 0) == 0 else 0
    return res
