from util import *
import math
import taichi as ti

@ti.data_oriented
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
        # init with taichi field
        self.x = ti.field(dtype=ti.f32, shape=())
        self.y = ti.field(dtype=ti.f32, shape=())
        self.z = ti.field(dtype=ti.f32, shape=())
        
        self.x[None] = x
        self.y[None] = y
        self.z[None] = z
    
    @ti.pyfunc
    def __add__(self, vec):
        return Vector3(self.x[None] + vec.x[None], self.y[None]+ vec.y[None], self.z[None]+vec.z[None])

    @ti.pyfunc
    def add_equal(self, vec):
        self.x[None] = self.x[None] + vec.x[None]
        self.y[None] = self.y[None] + vec.y[None]
        self.z[None] = self.z[None] + vec.z[None]

        return Vector3(self.x[None], self.y[None], self.z[None])

    @ti.pyfunc
    def __sub__(self, vec):
        return Vector3(self.x[None] - vec.x[None], self.y[None] - vec.y[None], self.z[None] - vec.z[None])
    
    @ti.pyfunc
    def subtrace_equal(self, vec):
        self.x[None] = self.x[None] - vec.x[None]
        self.y[None] = self.y[None] - vec.y[None]
        self.z[None] = self.z[None] - vec.z[None]

        return Vector3(self.x[None], self.y[None], self.z[None])

    @ti.pyfunc
    def negative(self):
        return Vector3(-self.x[None], -self.y[None], -self.z[None])

    @ti.pyfunc
    def __str__(self):
        return '(%.3f, %.3f, %.3f)'%(self.x[None], self.y[None], self.z[None])

    @ti.pyfunc
    def __truediv__(self, constant):
        return Vector3(self.x[None]/constant, self.y[None]/constant, self.z[None]/constant)

    @ti.pyfunc
    def divide_equal(self, constant):
        self.x[None] /= constant
        self.y[None] /= constant
        self.z[None] /= constant
        return Vector3(self.x[None], self.y[None], self.z[None])

    @ti.pyfunc
    def length(self):
        return (self.x[None]**2 + self.y[None]**2 + self.z[None]**2)**0.5

    @ti.pyfunc
    def length_square(self):
        return self.x[None]**2 + self.y[None]**2 + self.z[None]**2

    @ti.pyfunc
    def multiply(self, constant):
        return Vector3(self.x[None] * constant, self.y[None]*constant, self.z[None]*constant)
    
    @ti.pyfunc
    def multiply_equal(self, constant):
        self.x[None] *= constant
        self.y[None] *= constant
        self.z[None] *= constant
        return Vector3(self.x[None], self.y[None], self.z[None])
    
    @ti.pyfunc
    def dot(self,vec):
        return self.x[None]*vec.x[None] + self.y[None]*vec.y[None] + self.z[None]*vec.z[None]

    @ti.pyfunc
    def dot_equal(self, vec):
        self.x[None] *= vec.x[None]
        self.y[None] *= vec.y[None]
        self.z[None] *= vec.z[None]
        return Vector3(self.x[None], self.y[None], self.z[None])
    
    @ti.pyfunc
    def copy(self):
        return Vector3(self.x[None], self.y[None], self.z[None])
    
    @ti.pyfunc
    def unit_vector(self):
        return Vector3(self.x[None]/self.length(), self.y[None]/self.length(), self.z[None]/self.length())

    @ti.pyfunc
    def cross(self, vec):
        return Vector3(self.y[None]*vec.z[None] - self.z[None]*vec.y[None], self.z[None]*vec.x[None] - self.x[None]*vec.z[None], self.x[None]*vec.y[None]-self.y[None]*vec.x[None])

    @ti.pyfunc
    def mul(self, vec):
        return Vector3(self.x[None]*vec.x[None], self.y[None]*vec.y[None], self.z[None]*vec.z[None])


    @staticmethod
    @ti.pyfunc
    def random(min=None, max=None):
        if min is None:
            return Vector3(random_float(), random_float(), random_float())
        else:
            return Vector3(random_float(min, max), random_float(min, max), random_float(min, max))

    @ti.pyfunc
    def near_zero(self):
        s = 1e-8
        return abs(self.x[None])<s and abs(self.y[None])<s and abs(self.z[None])<s

    @ti.pyfunc
    def copy(self, vec):
        self.x[None] = vec.x[None]
        self.y[None] = vec.y[None]
        self.z[None] = vec.z[None]
        
@ti.pyfunc
def random_in_unit_sphere():
    """
    Return a random vector in unit sphere
    """
    while(True):
        p = Vector3.random(-1, 1)
        if p.length_square() >= 1:
            continue
        return p

@ti.pyfunc
def random_unit_vector():
    """
    Return a random unit vector
    """
    return random_in_unit_sphere().unit_vector()

@ti.pyfunc
def random_in_hemisphere(normal):
    in_unit_sphere = random_in_unit_sphere()
    if (in_unit_sphere.dot(normal)>0.0):
        return in_unit_sphere
    else:
        return in_unit_sphere.negative()
@ti.pyfunc
def reflect(v, n):
    return v - n.multiply(2*v.dot(n))

@ti.pyfunc
def refract(uv, n, etai_over_etat):
    """
    refraction
    """ 
    cos_theta = min(uv.negative().dot(n), 1.0)
    r_out_perp = (uv + n.multiply(cos_theta)).multiply(etai_over_etat)
    r_out_parallel = n.multiply(-math.sqrt(abs(1.0 - r_out_perp.length_square())))
    return r_out_parallel + r_out_perp

@ti.data_oriented
class Color(Vector3):
    def __init__(self, r=0., g=0., b=0.):
        super(Color, self).__init__(r,g,b)

@ti.data_oriented
class Point3(Vector3):
    def __init__(self, x=0., y=0., z=0.):
        super(Point3, self).__init__(x,y,z)

@ti.pyfunc
def random_color(min_val=None, max_val=None):
    if min_val is not None:
        return Color(random_float(min_val, max_val), random_float(min_val, max_val), random_float(min_val, max_val))
    return Color(random_float(), random_float(), random_float())

# @ti.kernel
def main():
    vec1 = Point3(0,1,2)
    vec2 = Point3(1,2,3)
    vec = vec1 + vec2
    print(vec.multiply(3.))
    print(vec.unit_vector())

if __name__=='__main__':
    ti.init()
    main()
    




