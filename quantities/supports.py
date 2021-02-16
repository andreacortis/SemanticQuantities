import pandas as pd
import numpy as np

class Support:
    def __init__(self, support:np.ndarray, qarray:Quantity):
        assert len(support)==len(qarray)

    def __add__(self, other):
        pass

    def __sub__(self, other):
        pass

    def __mul__(self, other):
        pass

    __rmul__ = __mul__(other, self)
    __radd__ = __add__(other, self)

    def __mul__(self, other):
        pass

    def interpolate(self, new_support):
        pass

class TimeSeries(Support):
    pass

class SpaceTrajectory(Support):
    pass

class VolumeArray(Support):
    pass
