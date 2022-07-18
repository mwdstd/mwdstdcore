import numpy as np
from mwdstdcore.errormods.codes import def_pattern
from mwdstdcore.errormods.unknown import unknown


class Run:
    def __init__(self):
        self.pre_qc = np.zeros(0)  # preliminary expectation on survey quality from outer system or user
        self.md = np.zeros(0)
        self.dni_xyz = np.zeros((0, 6))
        self.ref = np.zeros((0, 3))
        self.survey_status = np.zeros(0)
        self.axis_status = np.zeros(0)
        self.time = np.zeros(0)
        self.faxis = -1
        self.bha = []
        self.dni2bit = -100.
        self.edi = 0.
        self.dni_rigid = True
        self.casing_depth = -100.
        self.exti_interval = [-100., -100.]

        # parameters of correction
        self.correct_pattern = def_pattern.copy()  # define error terms to correct: def pattern is zero-hypothesis
        self.dni_cor = np.zeros(len(self.correct_pattern))  # correction vector for DnI error terms
        self.ref_cor = np.zeros(3)  # reference correction calculated based on the run
        self.fax_cor = np.zeros(0)  # recalculated an axis for failed surveys
        self.fax_ind = np.zeros(0)  # failed axis correction indexes
        self.apr_unc = unknown  # define apriori uncertainties for error terms
        self.mode = 'model'
        self.eterm_sigma = 1.  # number of error term sigma for model mode for apr_unc calculation
        self.min_inc_err = 0.  # rad, minimal inclination error for angle mode for apr_unc calculation
        self.min_az_err = 0.  # rad, minimal inclination error for angle mode for apr_unc calculation
        self.ref_cov_mat = np.zeros((0, 0))  # surveys' covariance matrix for correction

    def run2dict(self) -> dict:
        run_dict = Run.__to_dict(self)
        return run_dict

    def dict2run(self, run_dict: dict):
        self.md = np.asarray(run_dict['md'])
        self.dni_xyz = np.asarray(run_dict['dni_xyz'])
        self.ref = np.asarray(run_dict['ref'])
        self.survey_status = np.asarray(run_dict['survey_status'])
        self.axis_status = np.asarray(run_dict['axis_status'])
        self.time = np.asarray(run_dict['time'])
        self.pre_qc = np.asarray(run_dict['pre_qc'])
        self.faxis = int(run_dict['faxis'])
        try:
            self.bha = run_dict['bha']
            self.dni2bit = float(run_dict['dni2bit'])
        except:
            self.bha = []
            self.dni2bit = -100.
        self.edi = float(run_dict['edi'])
        self.casing_depth = float(run_dict['casing_depth'])
        self.exti_interval = run_dict['exti_interval']
        self.dni_rigid = bool(run_dict['dni_rigid'])
        self.correct_pattern = run_dict['correct_pattern'].copy()
        self.dni_cor = np.asarray(run_dict['dni_cor'])
        self.ref_cor = np.asarray(run_dict['ref_cor'])
        self.fax_cor = np.asarray(run_dict['fax_cor'])
        self.fax_ind = np.asarray(run_dict['fax_ind'])
        self.apr_unc = run_dict['apr_unc'].copy()
        self.mode = run_dict['mode']
        self.eterm_sigma = run_dict['eterm_sigma']
        self.min_inc_err = run_dict['min_inc_err']
        self.min_az_err = run_dict['min_az_err']
        self.ref_cov_mat = np.asarray(run_dict['covmat'])

    def clone(self):
        run_dict = self.run2dict()
        run = Run()
        run.dict2run(run_dict)
        return run

    @staticmethod
    def construct(run):
        run_dict = Run.__to_dict(run)
        new_run = Run()
        new_run.dict2run(run_dict)
        return new_run

    @staticmethod
    def __to_dict(run):
        return {
            'md': run.md.tolist(),
            'dni_xyz': run.dni_xyz.tolist(),
            'ref': run.ref.tolist(),
            'survey_status': run.survey_status.tolist(),
            'axis_status': run.axis_status.tolist(),
            'time': run.time.tolist(),
            'pre_qc': run.pre_qc.tolist(),
            'faxis': run.faxis,
            'bha': run.bha,
            'dni2bit': run.dni2bit,
            'edi': run.edi,
            'dni_rigid': run.dni_rigid,
            'casing_depth': run.casing_depth,
            'exti_interval': run.exti_interval,
            'correct_pattern': run.correct_pattern.copy(),
            'dni_cor': run.dni_cor.tolist(),
            'ref_cor': run.ref_cor.tolist(),
            'fax_cor': run.fax_cor.tolist(),
            'fax_ind': run.fax_ind.tolist(),
            'apr_unc': run.apr_unc.copy(),
            'mode': run.mode,
            'eterm_sigma': run.eterm_sigma,
            'min_inc_err': run.min_inc_err,
            'min_az_err': run.min_az_err,
            'covmat': run.ref_cov_mat.tolist()
        }

