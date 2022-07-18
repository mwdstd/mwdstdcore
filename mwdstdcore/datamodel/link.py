import attr
from typing import List


@attr.s(auto_attribs=True)
class LinkInd:
    run1: int
    srv1: int
    run2: int
    srv2: int


@attr.s(auto_attribs=True)
class Links:
    ind: List[LinkInd]
    daz: List[float]
    covmat_daz: List[List[float]]

    @property
    def rs_ind(self):
        return list(map(lambda rs: [rs.run1, rs.srv1, rs.run2, rs.srv2], self.ind))

