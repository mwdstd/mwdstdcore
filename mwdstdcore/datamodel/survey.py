from __future__ import annotations
import attr


@attr.s(auto_attribs=True, kw_only=True)
class Survey:
    md: float
    gx: float
    gy: float
    gz: float
    bx: float
    by: float
    bz: float
    # temp: float = None  # TODO: Lv4?
    pre_qc: bool = True

    @classmethod
    def listFromArrays(cls, mds, dni_xyz_cor):
        return [
            cls(md = md,
                gx=dni_xyz_cor[i, 0], gy=dni_xyz_cor[i, 1], gz=dni_xyz_cor[i, 2],
                bx=dni_xyz_cor[i, 3], by=dni_xyz_cor[i, 4], bz=dni_xyz_cor[i, 5])
            for i, md in enumerate(mds)]
