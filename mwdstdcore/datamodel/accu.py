import attr


@attr.s(auto_attribs=True, kw_only=True)
class Accuracy:
    inc_unc: float
    az_unc: float
    inc_unc_ref: float
    az_unc_ref: float
    inc_pass: bool
    az_pass: bool
