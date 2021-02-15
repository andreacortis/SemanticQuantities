import numpy as np
from typeguard import typechecked
from IPython.display import display, Latex
import numbers
from uncertainties import ufloat
import uncertainties
from pint import UnitRegistry, DimensionalityError
ureg = UnitRegistry()
ureg.default_format = "~P"
Q_=ureg.Quantity
from interval import interval, inf, imath

esc = lambda s: s.replace('"\"','"\\"')

@typechecked
class Limits:
    def __init__(self, limits:(tuple,list)):
        assert len(limits)==2
        lower, upper = limits
        try:
            assert lower.dimensionality == upper.dimensionality
        except DimensionalityError as exc:
            raise exc
        try:
            assert isinstance(lower.m, numbers.Number)
            assert isinstance(upper.m, numbers.Number)
        except AssertionError as e:
            print('lower and upper limits must be integer of floats')
            raise e
        lower.ito_base_units()
        upper.ito_base_units()
        self.value = interval([lower.m, upper.m])
        self.units = lower.units
    
    def __mul__(self,other):
        if isinstance(other, numbers.Number):
            return self.__create_from_interval__(self.value*other)
        elif isinstance(other, Limits):
            return self.__create_from_interval__(self.value*other.value)

    def __rmul__(self,other):
        return self.__create_from_interval__(self.__mul__(other))
    
    def __truediv__(self,other):
        if isinstance(other, numbers.Number):
            return self.__create_from_interval__(self.value/other)
        elif isinstance(other, Limits):
            return self.__create_from_interval__(self.value/other.value)

    def __create_from_interval__(self, I):
        return Limits((Q_(I[0][0],self.units),Q_(I[0][1],self.units)))

    def __str__(self):
        h = [(x[0].inf,x[0].sup) for x in self.value.components]
        h = "&".join([f"{x}\, — {y}" for x,y in h])
        return h + '\\, '+ self.units.__str__()
    
    def __repr__(self):
        s = f"$${self.__str__()}$$"
        display(Latex(s))
        return ""    

@typechecked
def __zeta__(x1:ufloat, x2:ufloat) -> bool:
    z = abs(x1.n -x2.n)/(x1.s**2 + x2.s**2)**0.5
    return z < 2.0 
    
class BaseQuantity:
    __significant_digits__ = 3
    units = '1'
    class_units = Q_(f"{units}")
    def __init__(self, name="", **kwargs):
        c1 = set(kwargs.keys()) == {'magnitude','units'}
        c2 = set(kwargs.keys()) == {'quantity'}
        self.name = name

        assert c1 ^ c2
        if c1:
            magnitude = kwargs['magnitude']
            units = kwargs['units']
            if isinstance(magnitude,numbers.Number):
                self.magnitude = ufloat(magnitude,0)
            else:
                self.magnitude = magnitude
                self.units = units
            self.value = Q_(self.magnitude, self.units)
        if c2:
            quantity = kwargs['quantity']
            self.value = quantity          

        if c1^c2:
            try:
                assert self.class_units.dimensionality == Q_(1,self.units).dimensionality
            except AssertionError:
                raise DimensionalityError(self.class_units.units, self.value.units)

    def __eq__(self, other):
        try:
            x = self.value.to_base_units()
            y = other.value.to_base_units()
            assert x.units == y.units
            assert __zeta__(x.m, y.m)
            return True
        except:
            return False

    def __add__(self,other):
        try:
            return self.value + other.value
        except DimensionalityError as exc:
            raise exc

    def __sub__(self, other):
        try:
            return self.value - other.value
        except DimensionalityError as exc:
            raise exc
            
    def __mul__(self,other):
        if isinstance(other, numbers.Number):
            return self.value*other
        elif isinstance(other, BaseQuantity):
            return self.value*other.value

    def __rmul__(self,other):
        return self.__mul__(other)
    
    def __pow__(self,n):
        return self.value**n
        
    def __truediv__(self,other):
        if isinstance(other, numbers.Number):
            return self.value/other
        elif isinstance(other, BaseQuantity):
            return self.value/other.value
        
    def __str__(self):
        # print('--- DEBUGGING')
        # print(type(self.value))
        if isinstance(self.value, Limits):
            # print('>>> Limits')
            h = [(x[0].inf,x[0].sup) for x in self.value.value.components]
            h = "&".join([f"{x}\, — {y}" for x,y in h])
            h =  h + '\\, '
            u = self.units
        elif isinstance(self.value, ureg.Quantity):
            # print('>>> quantity')
            if isinstance(self.value.m, np.ndarray):
                # print('>>> array')
                h = list(self.value.m).__str__()
                h = "["+", ".join([f"{x:.{self.__significant_digits__}u}" for x in self.value.m])+"]"
            else:
                # print('>>> scalar', type(self.value.m))
                if isinstance(self.value.m, numbers.Number):
                    h = f"{self.value.m:4.{self.__significant_digits__}g}"
                else:
                    if self.value.m.std_dev == 0:
                        h = f"{self.value.m.nominal_value:4.{self.__significant_digits__}g}"
                    else:
                        h = f"{self.value.m:4.{self.__significant_digits__}g}"
            u = self.value.units
        s = f"{self.name} = {h} \\, \\rm{{[{u}]}}, \\, \\rm{{({self.__class__.__name__})}}"
        s = s.replace('+/-',r'\pm')
        return s
    
    def __repr__(self):
        s = f"$${self.__str__()}$$"
        display(Latex(s))
        return ""

def quantity_maker(klass, units, expression=lambda x:Q_('0')):
    return type(klass,(BaseQuantity,),{"class_units":Q_(units),'units':units ,'expression':expression})

if __name__ == '__main__':
    pass