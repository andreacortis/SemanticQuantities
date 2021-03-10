from quantities import quantity_maker, Limits, Q_
from pint import DimensionalityError
from uncertainties import ufloat, unumpy
from typeguard import typechecked
import numpy as np

Mass = quantity_maker('Mass','kg')
Volume = quantity_maker('Volume','m^3')
Density = quantity_maker('Density','kg/m^3')
Porosity = quantity_maker('Porosity', 'm^3/m^3')

@typechecked
def density(name:str, m:Mass, v:Volume) -> Density:
    name = f'{name} = \\frac{{{m.name}}}{{{v.name}}}'
    return Density(name = name, quantity = (m/v))

def test_00():
    try:
        m = Mass(name='m', quantity=Q_('6 kg'))
    except DimensionalityError as exc:
        raise exc

    try:
        m = Mass(name='m', magnitude=ufloat(6, 0.1), units='kg')
    except DimensionalityError as exc:
        raise exc

    try:
        m = Mass(name='m', quantity=Limits([Q_('6 kg'), Q_('7 kg')]))
    except DimensionalityError as exc:
        raise exc

    try:
        r = Mass(r'\bar{m}',quantity=Q_(np.array([ufloat(3,0.1),ufloat(4,0.2)]),'kg'))
    except DimensionalityError as exc:
        raise exc

def test_01():
    try:
        m = Mass(name='m', magnitude=ufloat(6, 0.1), units='m')
    except DimensionalityError as exc:
        pass
    
def test_02():
    try:
        m = Mass(name='m', magnitude=ufloat(6, 0.1), units='kg')
        v = Volume(name='v', quantity=Q_(ufloat(3, 0.2),'m^3'))
        rho_1 = density(r'\rho',m,v)
        rho_expected = Density('', quantity = Q_(ufloat(2.00, 0.14), "kg/m^3"))
    except RuntimeError as e:
        raise e
    
def test_03():
    try:
        m = Mass(name=r'\bar{m}', quantity=Limits([Q_('6 kg'), Q_('7 kg')]))
        v = Volume(name=r'\bar{v}', quantity=Limits([Q_('1 m^3'), Q_('3 m^3')]))
        rho = density(r'\rho',m,v)
    except RuntimeError as e:
        raise e

def test_04():
    try:
        h1 = unumpy.uarray([1,2,3],[0.1,0.2,0.3])
        m = Mass(r'\bar{m}',quantity=Q_(h1,'kg'))
        h2 = unumpy.uarray([10,20,30],[0.1,0.2,0.3])
        v = Volume(r'\bar{v}',quantity=Q_(h2,'m^3'))
    except RuntimeError as e:
        raise e

def test_05():
    m = Mass(name='m', magnitude=ufloat(6, 0.1), units='kg')
    v = Volume(name='v', quantity=Q_(ufloat(3, 0.2),'m^3'))
    phi = Porosity(name='phi',quantity=Q_('0.30 '))
    a = m/v
    print(f"a = {a}")
    b = m/phi
    print(f"b = {b}")
    try:
        c = m/v/phi
        print(f"c = {c}")
    except:
        raise RuntimeError 