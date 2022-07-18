def list_non_empty(self, attr, val):
    if len(val) == 0:
        raise ValueError("Empty list")


def md_ordered(self, attr, val):
    if any((s1.md > s2.md for s1, s2, in zip(val[:-1], val[1:]))):
        raise ValueError("Invalid depth order")


def lte(value):
    def impl(self, attr, val):
        if val > value:
            raise ValueError(f"{attr.name} has to be less than or equal {value} (got {val})")
    return impl


def gte(value):
    def impl(self, attr, val):
        if val < value:
            raise ValueError(f"{attr.name} has to be greater than or equal {value} (got {val})")
    return impl
