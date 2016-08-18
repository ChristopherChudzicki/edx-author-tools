from collections import defaultdict
import numbers
import random

def isclose(a, b, rtol=1e-05, atol=1e-08):
    """Determine if two numbers are close.
    Modeled after numpy.isclose (which edX does not have because it uses old version of numpy) 
    http://docs.scipy.org/doc/numpy/reference/generated/numpy.isclose.html
    """
    return abs(a - b) <= (atol + rtol * abs(b))



class DimensionMismatchError(Exception):
    """Raise error when adding/subtracting two dimensions that do not match.
    """
    pass
class DimensionArgumentError(Exception):
    """Raise this error when the argument x of a function f(x) has nontrivial dimension.
    """
    pass
class DimensionPowerError(Exception):
    """Raise this error during x^y when y has nontrivial dimensions
    """
    pass
class IndeterminateDimensionError(Exception):
    """Some possible answer strings have dimensions that depend on variable values. E.g., if
            [v] = length / time
            [L] = [L0] = length
        then the dimensions of
            v^(L/L0)
        depend on the values of L and L0.
        
        I do not know of any situations in which this actually occurs.
    
        NOTE: In this case, we could still tell that e.g.,
            v^(L/L0)
            w^(L/L0)
        have the same dimensions.
    """
    pass

class Dimension(object):
    """docstring for Dimension"""
    def __init__(self, dims):
        if isinstance(dims, self.__class__):
            self.dims = dims.dims
        else:
            self.dims = defaultdict(float)
            self.dims.update(dims)
    def __repr__(self):
        key_list = [ "{unit}^{power}".format(unit=key, power=power ) for key, power in self.dims.iteritems() ]
        return " * ".join(key_list)
    def __mul__(self, other):
        if isinstance(other, self.__class__):
            result = defaultdict(float)
            for key in set(self.dims) | set(other.dims):
                result[key] = self.dims[key] + other.dims[key]
            return self.__class__(result)
        else:
            raise TypeError
    def __pow__(self, other):
        if isinstance(other,numbers.Number) and not isinstance(other,Quantity):
            result = { key:value*other for key, value in self.dims.iteritems() }
            return self.__class__(result)
        else:
            return TypeError
    def __div__(self, other):
        return self*other**-1
    def __truediv__(self,other):
        return self.__div__(other)
    def __eq__(self, other):
        quotient = self/other
        return all( isclose(0, quotient.dims[dim]) for dim in quotient.dims )
    def __add__(self, other):
        if self==other:
            return self
        else:
            raise DimensionMismatchError("Can't add two quantities with different dimensions.")
    def __sub__(self, other):
        return self.__add__(other)
    def is_dimensionless(self):
        return self == Dimension({})

class Quantity(numbers.Number):
    """Stores a physical quantity with value and dimensions.
    
    Supported operations:
        Below, 'number' refers to a pure number, i.e., not a quantity.
    
        - addition, subtraction ... both commutative:
            quantity + quantity --> quantity, input dimensions must match
            0 + quantity --> quantity
            
        - multiplication, division:
            quantity*quantity --> quantity
            number*quantity --> quantity
        
        - power:
            quantity ** number --> quantity
            quantity ** quantity --> quantity, exponent quantity must be dimensionless
    
    """
    def __init__(self, value, dims={}):
        if isclose(value, 0):
            self.value = 0
            self.dims = Dimension({})
        else:
            self.value = value
            self.dims = Dimension(dims)
    def __repr__(self):
        return "{value} {dims}".format(value=self.value, dims = self.dims.__repr__())
    def __add__(self, other):
        other = self.__class__._ensure_quantity(other)
        if other == Quantity(0,{}):
            return self
        elif self == Quantity(0,{}):
            return other
        else:
            result_dims = self.dims + other.dims
            result_value = self.value + other.value
            return Quantity(result_value, result_dims)
    def __radd__(self, other):
        return self.__add__(other)
    def __sub__(self, other):
        return self.__add__(-1*other)
    def __rsub__(self, other):
        return -1*self.__sub__(other)
    def __mul__(self, other):
        other = self.__class__._ensure_quantity(other)
        result_dims = self.dims * other.dims
        result_value = self.value * other.value
        return Quantity(result_value, result_dims)
    def __rmul__(self, other):
        return self.__mul__(other)
    def __pow__(self, other):
        if isinstance(other,self.__class__):
            if not other.dims == Dimension({}):
                raise DimensionPowerError
            other = other.value
        result_dims = self.dims ** other
        result_value = (self.value+0j) ** other
        return Quantity(result_value, result_dims)
    def __rpow__(self, other):
        if not self.dims == Dimension({}):
            raise DimensionPowerError
        else:
            result_value = other**self.value
            return Quantity(result_value, Dimension({}))
    def __div__(self, other):
        other = self.__class__._ensure_quantity(other)
        return self*other**-1
    def __rdiv__(self, other):
        return other*self**-1
    def __truediv__(self,other):
        return self.__div__(other)
    def __rtruediv__(self, other):
        return self.__rdiv__(other)
    def __eq__(self, other):
        if not isinstance(other, numbers.Number):
            return False
        other = self.__class__._ensure_quantity(other)
        return self.value == other.value and self.dims == other.dims
    def is_dimensionless(self):
        return self.dims == Dimension({})
    @classmethod
    def _ensure_quantity(cls,other):
        "Tries to convert other to cls"
        if isinstance(other,cls):
            return other
        elif isinstance(other,numbers.Number):
            return Quantity(other,{})
        else:
            raise TypeError

