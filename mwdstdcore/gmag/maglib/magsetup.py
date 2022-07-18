import numpy as np
from math import floor
from .magmod import MagneticModel
from .date import Date
from .wmmglb10.wmmlist import wmm10_header, wmm10, wmm10_sv
from .wmmglb15.wmmlist import wmm15_header, wmm15, wmm15_sv
from .wmmglb20.wmmlist import wmm20_header, wmm20, wmm20_sv
from .dgrfglb15.dgrflist import dgrf15_header, dgrf15, dgrf15_sv
from .igrfglb20.igrflist import igrf20_header, igrf20, igrf20_sv


class MagSetup:
    __is_init = False
    __crustal_field = True
    model_name = ''
    start_epoch = 0.
    stop_epoch = 0.
    EPOCH_LENGTH = 6
    epochs = np.zeros(0)
    gmm_headers = []
    gmm_glb_coeffs = []
    gmm_sv_coeffs = []
    act_model = MagneticModel()

    @staticmethod
    def get_mag_model(date: Date, gmag_mod='WMM2020', crustal_field=False) -> MagneticModel:

        if not MagSetup.__is_init or MagSetup.model_name != gmag_mod or MagSetup.__crustal_field != crustal_field:
            MagSetup.__mag_models_init(gmag_mod=gmag_mod, crustal_field=crustal_field)
            MagSetup.__is_init = True
            MagSetup.__crustal_field = crustal_field

        if not (MagSetup.start_epoch <= date.DecimalYear <= MagSetup.stop_epoch + 1):
            raise Exception('Class MagSetup method get_mag_model: input date is out of mag model range')

        num_of_epochs = len(MagSetup.gmm_headers)
        index = int(floor(date.DecimalYear - MagSetup.gmm_headers[0][0]))
        if index > num_of_epochs - 1:
            index = num_of_epochs - 1
        epoch = MagSetup.gmm_headers[index][0]

        nterms_gf = MagSetup.gmm_glb_coeffs[0].shape[0]
        main_field_coeff_g = MagSetup.gmm_glb_coeffs[index][:, 2]
        main_field_coeff_h = MagSetup.gmm_glb_coeffs[index][:, 3]
        sec_var_coeff_g = MagSetup.gmm_sv_coeffs[index][:, 2]
        sec_var_coeff_h = MagSetup.gmm_sv_coeffs[index][:, 3]

        MagSetup.act_model.Main_Field_Coeff_G[1:nterms_gf + 1] = main_field_coeff_g + (date.DecimalYear - epoch) * \
            sec_var_coeff_g
        MagSetup.act_model.Main_Field_Coeff_H[1:nterms_gf + 1] = main_field_coeff_h + (date.DecimalYear - epoch) * \
            sec_var_coeff_h

        MagSetup.act_model.Secular_Var_Coeff_G[1:] = sec_var_coeff_g
        MagSetup.act_model.Secular_Var_Coeff_H[1:] = sec_var_coeff_h

        MagSetup.act_model.EditionDate = epoch
        MagSetup.act_model.epoch = epoch

        MagSetup.act_model.SecularVariationUsed = True

        return MagSetup.act_model

    @staticmethod
    def __mag_models_init(gmag_mod='WMM2020', crustal_field=False):
        if gmag_mod == 'WMM2020':
            MagSetup.gmm_glb_coeffs = wmm20
            MagSetup.gmm_sv_coeffs = wmm20_sv
            MagSetup.gmm_headers = wmm20_header
        elif gmag_mod == 'WMM2010':
            MagSetup.gmm_glb_coeffs = wmm10
            MagSetup.gmm_sv_coeffs = wmm10_sv
            MagSetup.gmm_headers = wmm10_header
        elif gmag_mod == 'WMM2015':
            MagSetup.gmm_glb_coeffs = wmm15
            MagSetup.gmm_sv_coeffs = wmm15_sv
            MagSetup.gmm_headers = wmm15_header
        elif gmag_mod == 'DGRF2015':
            MagSetup.gmm_glb_coeffs = dgrf15
            MagSetup.gmm_sv_coeffs = dgrf15_sv
            MagSetup.gmm_headers = dgrf15_header
        elif gmag_mod == 'IGRF2020':
            MagSetup.gmm_glb_coeffs = igrf20
            MagSetup.gmm_sv_coeffs = igrf20_sv
            MagSetup.gmm_headers = igrf20_header
        else:
            raise Exception('Class MagSetup method mag_model_init(): wrong gmag_mod input')
        MagSetup.act_model.ModelName = gmag_mod
        MagSetup.model_name = gmag_mod

        MagSetup.start_epoch = MagSetup.gmm_headers[0][0]
        MagSetup.stop_epoch = MagSetup.gmm_headers[-1][0] + MagSetup.EPOCH_LENGTH

        MagSetup.act_model.CoefficientFileEndDate = MagSetup.stop_epoch

        if crustal_field:
            nterms_cf = crustal_coeffs.shape[0]
            nmax = int(crustal_coeffs[-1, 0])
            nmax_sv = int(MagSetup.gmm_glb_coeffs[0][-1, 0])
            nterms_gf = MagSetup.gmm_glb_coeffs[0].shape[0]
            MagSetup.act_model.nMax = nmax
            MagSetup.act_model.nMaxSecVar = nmax_sv
            MagSetup.act_model.Main_Field_Coeff_G = np.zeros(nterms_gf + nterms_cf + 1)
            MagSetup.act_model.Main_Field_Coeff_H = np.zeros(nterms_gf + nterms_cf + 1)
            MagSetup.act_model.Main_Field_Coeff_G[nterms_gf + 1:] = crustal_coeffs[:, 2]
            MagSetup.act_model.Main_Field_Coeff_H[nterms_gf + 1:] = crustal_coeffs[:, 3]
        else:
            nmax = int(MagSetup.gmm_glb_coeffs[0][-1, 0])
            nmax_sv = nmax
            nterms_gf = MagSetup.gmm_glb_coeffs[0].shape[0]
            MagSetup.act_model.nMax = nmax
            MagSetup.act_model.nMaxSecVar = nmax_sv
            MagSetup.act_model.Main_Field_Coeff_G = np.zeros(nterms_gf + 1)
            MagSetup.act_model.Main_Field_Coeff_H = np.zeros(nterms_gf + 1)
        MagSetup.act_model.Secular_Var_Coeff_G = np.zeros(nterms_gf + 1)
        MagSetup.act_model.Secular_Var_Coeff_H = np.zeros(nterms_gf + 1)
        return
