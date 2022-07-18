from typing import Optional
import attr
from functools import partial


@attr.s(auto_attribs=True)
class QualityFactor:
    name: str
    value: Optional[bool] = None
    severity: Optional[int] = None

    def __bool__(self):
        return bool(self.value)


@attr.s(auto_attribs=True)
class QualityAssessment:
    accuracy: QualityFactor = attr.ib(factory=partial(QualityFactor, 'Solution accuracy', False, 1))
    expectation: QualityFactor = attr.ib(factory=partial(QualityFactor, 'Expected survey quality', False, 1))
    reference: QualityFactor = attr.ib(factory=partial(QualityFactor, 'Reference quality', False, 1))
    correction_possibility: QualityFactor = attr.ib(factory=partial(QualityFactor, 'DSI correction possibility', False, 1))
    model_comparison: QualityFactor = attr.ib(factory=partial(QualityFactor, 'Actual DnI error vs model', False, 1))
    number_of_surveys: QualityFactor = attr.ib(factory=partial(QualityFactor, 'Number of surveys', False, 1))
    linking: QualityFactor = attr.ib(factory=partial(QualityFactor, 'Linked with previous run', None, 0))
    confidence: QualityFactor = attr.ib(factory=partial(QualityFactor, 'Correction confidence', None, 0))  # false: Weak correction confidence, true: Strong correction confidence
    plan: QualityFactor = attr.ib(factory=partial(QualityFactor, 'Plan conformance', None, 0))
    ci_vrf: QualityFactor = attr.ib(factory=partial(QualityFactor, '(HD trajectory ci_vrf)', None, 1))
    srv_freq: QualityFactor = attr.ib(factory=partial(QualityFactor, '(HD trajectory srv_freq)', None, 1))
    msa_conv1: QualityFactor = attr.ib(factory=partial(QualityFactor, 'MSA convergence 1', None, 1))
    msa_conv2: QualityFactor = attr.ib(factory=partial(QualityFactor, 'MSA convergence 2', None, 1))
    sq_last: QualityFactor = attr.ib(factory=partial(QualityFactor, 'Latest five survey quality', None, 0))
    sag_conv: QualityFactor = attr.ib(factory=partial(QualityFactor, 'Sag convergence', None, 1))
    sag_exp: QualityFactor = attr.ib(factory=partial(QualityFactor, 'Sag result vs error model', None, 1))
    str_qc: QualityFactor = attr.ib(factory=partial(QualityFactor, 'Slidesheet conformance', None, 0))

    def __bool__(self):
        return bool(self.accuracy and self.is_eligible)

    # eligibility for multi-run correction
    @property
    def is_eligible(self):
        return bool(self.expectation and self.reference and self.correction_possibility and self.model_comparison
                    and self.number_of_surveys)

    # quality acceptance flag
    @property
    def is_good(self):
        return bool(self.accuracy and self.expectation and self.reference and self.correction_possibility and
                    self.model_comparison and self.number_of_surveys)
