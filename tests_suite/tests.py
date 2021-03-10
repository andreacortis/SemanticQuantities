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

def test_00a():
    try:
        m = Mass(name='m', quantity=Q_('6 kg'))
    except DimensionalityError as exc:
        raise exc

def test_00b():
    try:
        m = Mass(name='m', magnitude=ufloat(6, 0.1), units='kg')
    except DimensionalityError as exc:
        raise exc

def test_00c():
    try:
        m = Mass(name='m', quantity=Limits([Q_('6 kg'), Q_('7 kg')]))
    except DimensionalityError as exc:
        raise exc

def test_00d():
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
    from quantities import quantity_maker, Limits, Q_
    from pint import DimensionalityError
    from uncertainties import ufloat, unumpy
    from typeguard import typechecked
    import numpy as np

    Mass = quantity_maker('Mass','kg')
    Volume = quantity_maker('Volume','m^3')
    Density = quantity_maker('Density','kg/m^3')
    Porosity = quantity_maker('Porosity', 'm^3/m^3')
    m = Mass(name='m', magnitude=ufloat(6, 0.1), units='kg')
    v = Volume(name='v', quantity=Q_(ufloat(3, 0.2),'m^3'))
    phi = Porosity(name='phi',quantity=Q_('0.30 '))
    a = m/v/phi
    print(f"a = {a}")
    b = m/phi
    print(f"b = {b}")
    try:
        c = m/v/phi
        print(f"c = {c}")
    except:
        raise RuntimeError 

# -------------------------------------------------------------------
def test_06():
    d = {
        'FlowRate':'m^3/s',
        'Velocity':'m/s',
        'Area':'m^2',
        'Length':'m',
        'Porosity':'m^3/m^3',
        'Permeability':'m^2',
        'Density':'kg/cm^3',
        'Viscosity':'Pa*sec',
        'Reynolds':'1'
    }

    for k,v in d.items():
        globals()[k] = quantity_maker(k,v)

    q = FlowRate(name='q', quantity=Q_('1e-3 liters/hours'))
    phi = Porosity(name='phi',quantity=Q_('0.23'))
    h = Length(name='h', quantity=Q_('60 um'))
    b = Length(name='b', quantity=Q_('0.6 cm'))
    rho = Density(name='rho', quantity=Q_('1 gr/cm^3'))
    eta = Viscosity(name='eta', quantity=Q_('0.89e-3 Pa*sec'))
    K = Permeability(name='K',quantity=Q_('50e-12 m^2'))
    A = Area(name='A', semantic_quantity=b*h)
    v = Velocity(name='v', semantic_quantity=q/A/phi)
    Re = Reynolds(name='re',semantic_quantity=rho/eta*v*K**0.5)
    assert Re.__str__() == "re = 0.00173 \\, \\rm{[]}, \\, \\rm{(Reynolds)}"