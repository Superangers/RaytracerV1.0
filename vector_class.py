from math import *

class Vector():
    def __init__(self, x, y, z):
        self.x, self.y, self.z = x, y, z  #float(x), float(y), float(z)

    # basic operations ===========================================================
    def __add__(self, other):
        if type(other)==Vector:
            return Vector(self.x + other.x,
                self.y + other.y,
                self.z + other.z)
        elif type(other)==float or type(other)==int:
            return self + Vector(other, other, other)

    def __sub__(self, other):
        if type(other)==Vector:
            return Vector(self.x - other.x,
                self.y - other.y,
                self.z - other.z)
        elif type(other)==float or type(other)==int:
            return self - Vector(other, other, other)

    def __mul__(self, other):
        if type(other)==Vector:
            return Vector(self.x * other.x,
                self.y * other.y,
                self.z * other.z)
        elif type(other)==float or type(other)==int:
            return self * Vector(other, other, other)
        #else: raise TypeError("Vector")

    def __truediv__(self, other):
        if type(other)==Vector:
            return Vector(self.x / other.x,
                self.y / other.y,
                self.z / other.z)
        elif type(other)==float or type(other)==int:
            return self / Vector(other, other, other)
    
    def __pow__(self, other):
        if type(other)==Vector:
            return Vector((self.x ** other.x).real ,
                (self.y ** other.y).real ,
                (self.z ** other.z).real)
        elif type(other)==float or type(other)==int:
            return self ** Vector(other, other, other)
        else: raise TypeError("Vector POWER error")
    
    def __neg__(self):
        return Vector(-self.x,
            -self.y,
            -self.z)

    def sqrt(self):
        return Vector(sqrt(abs(self.x)), sqrt(abs(self.y)), sqrt(abs(self.z)))

    def exp(self):
        return Vector(exp(self.x), exp(self.y), exp(self.z))
                        

    # others=========================================================================

    def __str__(self):
        return ", ".join((str(self.x), str(self.y), str(self.z)))

    def clip(self, min, max):
        if self.x < min or self.x > max:
            self.x = min if self.x < min else max
        if self.y < min or self.y > max:
            self.y = min if self.y < min else max
        if self.z < min or self.z > max:
            self.z = min if self.z < min else max
        return Vector(float(self.x), float(self.y), float(self.z))

    #vector operations===============================================================

    def length(self):
        return sqrt(self.x**2 + self.y**2 + self.z**2)

    def normalize(self):
        return self / self.length()

    def dotProduct(self, other):
        temp = self * other
        return float(temp.x + temp.y + temp.z)

print(Vector(-0.02263815353620452, -0.02263815353620452, -0.02263815353620452) ** 17.5)
