from util import *


class Vector3:
    """
    Info: Vector with 3 Dimensions, support basic arithmetic. 

    Usage: 
    
    Init: (x,y,z)
    Func: +, add_equal, -, subtract_equal, negative,
      /, divide_equal, length, length_square, multiply, multiply_equal,
      dot, dot_equal, copy, unit_vector, cross

    Subclass: Point3, Color

    """
    def __init__(self, x=0., y=0., z=0.):
        x:float
        y:float
        z:float
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
    
    def __add__(self, vec):
        return Vector3(self.x + vec.x, self.y + vec.y, self.z+vec.z)

    def add_equal(self, vec):
        self.x = self.x + vec.x
        self.y = self.y + vec.y
        self.z = self.z + vec.z

        return Vector3(self.x, self.y, self.z)

    def __sub__(self, vec):
        return Vector3(self.x - vec.x, self.y - vec.y, self.z - vec.z)
    
    def subtrace_equal(self, vec):
        self.x = self.x - vec.x
        self.y = self.y - vec.y
        self.z = self.z - vec.z

        return Vector3(self.x, self.y, self.z)

    def negative(self):
        return Vector3(-self.x, -self.y, -self.z)

    def __str__(self):
        return '(%.3f, %.3f, %.3f)'%(self.x, self.y, self.z)

    def __truediv__(self, constant):
        return Vector3(self.x/constant, self.y/constant, self.z/constant)

    def divide_equal(self, constant):
        self.x /= constant
        self.y /= constant
        self.z /= constant
        return Vector3(self.x, self.y, self.z)

    def length(self):
        return (self.x**2 + self.y**2 + self.z**2)**0.5

    def length_square(self):
        return self.x**2 + self.y**2 + self.z**2

    def multiply(self, constant):
        return Vector3(self.x*constant, self.y*constant, self.z*constant)
    
    def multiply_equal(self, constant):
        self.x *= constant
        self.y *= constant
        self.z *= constant
        return Vector3(self.x, self.y, self.z)
        
    def dot(self,vec):
        return self.x*vec.x + self.y*vec.y + self.z*vec.z

    def dot_equal(self, vec):
        self.x *= vec.x
        self.y *= vec.y
        self.z *= vec.z
        return Vector3(self.x, self.y, self.z)
    
    def copy(self):
        return Vector3(self.x, self.y, self.z)
    
    def unit_vector(self):
        return Vector3(self.x/self.length(), self.y/self.length(), self.z/self.length())


    def cross(self, vec):
        return Vector3(self.y*vec.z - self.z*vec.y, self.z*vec.x - self.x*vec.z, self.x*vec.y-self.y*vec.x)


    @staticmethod
    def random(min=None, max=None):
        if min is None:
            return Vector3(random_float(), random_float(), random_float())
        else:
            return Vector3(random_float(min, max), random_float(min, max), random_float(min, max))


def random_in_unit_sphere():
    """
    Return a random vector in unit sphere
    """
    while(True):
        p = Vector3.random(-1, 1)
        if p.length_square() >= 1:
            continue
        return p

def random_unit_vector():
    """
    Return a random unit vector
    """
    return random_in_unit_sphere().unit_vector()


def random_in_hemisphere(normal:Vector3):
    in_unit_sphere = random_in_unit_sphere()
    if (in_unit_sphere.dot(normal)>0.0):
        return in_unit_sphere
    else:
        return in_unit_sphere.negative()


class Color(Vector3):
    def __init__(self, r=0., g=0., b=0.):
        super(Color, self).__init__(r,g,b)


class Point3(Vector3):
    def __init__(self, x=0., y=0., z=0.):
        super(Point3, self).__init__(x,y,z)


if __name__=='__main__':
    vec1 = Point3(0,1,2)
    vec2 = Point3(1,2,3)
    vec = vec1.add_equal(vec2)
    vec.divide_equal(5)
    print(vec.unit_vector())




