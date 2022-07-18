import attr


@attr.s(auto_attribs=True)
class Interval:
    start: float = -100.
    stop: float = -100.

    def __getitem__(self, item):
        if item == 0:
            return self.start
        if item == 1:
            return self.stop
        return None
