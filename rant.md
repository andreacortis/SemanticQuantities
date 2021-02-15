Hello, I introduce myself as I am new to this group. PhD in geophysics from TUDedelft, 8 years at LBNL, and now a data science career in the energy private sector. 
I discovered this very interesting library and as you mention that you would like to have some input here is mine. 
Sorry for the very long post.

\begin{rant}

We are in the very unfortunate situation that, especially in some engineering fields like petroleum engineering, rock physics, 
petrophysics, and other empirical sciences, we still have to deal with publications that allow nonsensical constructs 
like the application of trascendental functions (e.g. log, sin, exp, etc.) to physical quantities

You don't believe me? Try this:

```
In [1]: import numpy as np
In [2]: from pint import UnitRegistry, DimensionalityError
In [3]: ureg = UnitRegistry()
In [4]: Q_ = ureg.Quantity
In [5]: x = Q_('3 m')
In [6]: np.exp(x)
---------------------------------------------------------------------------
DimensionalityError                       Traceback (most recent call last)
<ipython-input-6-564c0efc6b65> in <module>
----> 1 np.exp(x)

[...]

DimensionalityError: Cannot convert from 'meter' ([length]) to 'dimensionless' (dimensionless)
```

The reason of this failure should be obvious, and still I find myself arguing every time with PhD-level colleaugues that it is OK, that this is the way that this has always been done, that we cannot be too picky and blah blah ... someone shut them up pleeeease!

Take for instance as an example the simple correlation found by Olhoeft (1979) between the density of a dry rock, $\rho$ (units of Mass/Volume) and its permittivity, a dimensionless quantity. The relation is [Mavko et al., Rock Physics Handbook 2nd ed., p.422] and for quartz we should have

$$
\kappa = 1.91^{\rho}
$$

with $\rho$ expressed in [g/cm^3].

Really ?!?!?! Let's try:

```
In [7]: rho = Q_('2.31 g/cm^3')

In [8]: 1.91**rho
---------------------------------------------------------------------------
DimensionalityError                       Traceback (most recent call last)
<ipython-input-8-b30888e100ce> in <module>
----> 1 1.91**rho
[...]
DimensionalityError: Cannot convert from 'gram / centimeter ** 3' to 'dimensionless'
```

Same story ... you simply cannot do that. The understanding in all these relationships is that you need:
    1. first to convert the density measurement in units of g/cm^3, 
    2. take the magnitude of that physical value, which turns out to be equal to $2.31$, 
    3. raise the number $1.91$ to the power of $2.31$

```
In [9]: 1.91**2.31
Out[9]: 4.458482623308442
```
of that magnitude and assign a value to the permittivity with a magnitude equal to the result of that computation. 
The obvious disadvantage is that we are in a land where dimensional analysis does not make sense anymore. 

One way of understanding this nonsense is trying to unpack and reconstruct the way the correlation was built


$$
\kappa = 1.91^{\rho}

\ln \kappa = \rho \ln 1.91

\ln \kappa = 0.647 \rho 

\kappa = exp(0.647 \rho)

\kappa = exp( \rho / 1.5455)
$$

which shows a linear relation between the density (measured in g/cm^3) and the logarithm of the permittivity.
But this simply implies that, as it was originally stipulated that $\rho$ must have units of $g/cm^3$ then also coefficient $1.5455$ needs to be a physical quantity with units of $g/cm^3$: it is simply reference density!!!!. 

Let's try

```
In [10]: np.exp(rho / Q_('1.5455 g/cm^3'))
Out[10]: 4.457829202778935 <Unit('dimensionless')>
```

Success!!! 
Now, this is what I call a germaine correlation that does not depend on the choice of units for the density

```
In [11]: np.exp(Q_('2310 kg/m^3') / Q_('1.5455 g/cm^3'))
Out[11]: 4.457829202778937 <Unit('dimensionless')>
```

and now the correlation has perhaps a chance to acquire some meaningful physical interpretation!

Please somebody wake me up from this horror B-movie! Why? Why? 
Why in the world these correlations are not expressed in a form that does not depend on the choice of units? 

\end{rant}

This is why I decided to create a python package that, through syntax expressiveness, is aimed at maintaining the semantics of the physical quantities.
The package (with a provisional name of `quantities`, which I am planning to change to `SemanticQuantities`), depends on `pint`, `uncertainties`, `pyinterval`, and `typeguard`. I have seen on `pypi` that there have been a few attempts 

To give some examples of the expressiveness:

```
# custom physical quantities    
Mass = quantity_maker('Mass','kg')
Time = quantity_maker('Mass','sec')
Length = quantity_maker('Length','m')
```

[Note that even though we are declaring `metric` units, those are jus a placeholder for enforcing the dimensionality and defining `Mass = quantity_maker('Mass','lb')` would also be perfectly acceptable].

I think that it is important that we carry the meaning of what we want to compute. 
For instance, `porosity` is a dimensionless quantity that is defined as a ratio of volumes

```
Porosity = quantity_maker('Porosity','m^3/m^3')
print(Porosity.units)
m^3/m^3
```

but so is the `effective porosity`

```
EffectivePorosity = quantity_maker('EffectivePorosity','m^3/m^3')
```

and if I were to try to calculate a permeability inserting a `total porosity` instead of an `effective porosity` the code should return an error, because that is not what we meant, and we should enforce what we mean.

Actual physical quantities can be defined as a single value, a value with uncertainty, and /or an interval between two values:

```
In [9]: m = Mass(name='m', magnitude=6, units='kg')
In [10]: print(m)
m = 6.0\pm0 \, \rm{[kilogram]}, \, \rm{(Mass)}
```
note that `print` exhibits the LaTeX code, whereas the `display` function would render the same LaTeX code in a juyter notebook.

```
In [9]: v = Volume(name=r'\cal(V)', quantity=Q_(ufloat(6, 0.2),'m^3'))
In [11]: print(v)
\cal(V) = 6.00\pm0.20 \, \rm{[meter ** 3]}, \, \rm{(Volume)}

l0 = Length(name='v_0', limits=Limits([Q_('3.21 m^3'),Q_('3.6 m^3')]))


```



I have not open sourced the repo yet because I am just tasting the waters: if there is an interest in using my package as the foundation for the units (rather than just relying on `pint` as it seems to be right now), I would be more than happy to publish it on github under the most permissive licence (right now I am thinking of MIT, but suggestions are welcome.)

