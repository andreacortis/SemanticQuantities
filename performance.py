from timeit import timeit

# --- define the global scope

from quantities import quantity_maker, Limits, Q_
from pint import DimensionalityError
from uncertainties import ufloat, unumpy
from typeguard import typechecked
import numpy as np

Mass = quantity_maker('Mass','kg')
Volume = quantity_maker('Volume','m^3')
Density = quantity_maker('Density','kg/m^3')

h1 = unumpy.uarray([1,2,3],[0.1,0.2,0.3])
m = Mass(r'\bar{m}',quantity=Q_(h1,'kg'))
h2 = unumpy.uarray([10,20,30],[0.1,0.2,0.3])
v = Volume(r'\bar{v}',quantity=Q_(h2,'m^3'))

# --- code snippets
s_vec = [
    "density('r',m,v)",
    "m.value.m / v.value.m", 
    "print(density('r',m,v))"
]

for s in s_vec:
    t = timeit(s, number=100,globals=globals())
    print(f"{s:40s}: {t}")
