
class Vector3:
    """
    Vector with 3 Dimensions, support basic arithmetic. 
    """
    def __init__(self, x=0., y=0., z=0.):
        x:float
        y:float
        z:float
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
    
    def add(self, vec):
        return Vector3(self.x + vec.x, self.y + vec.y, self.z+vec.z)

    def add_equal(self, vec):
        self.x = self.x + vec.x
        self.y = self.y + vec.y
        self.z = self.z + vec.z

        return Vector3(self.x, self.y, self.z)

    def subtract(self, vec):
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

    def divide(self, constant):
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




