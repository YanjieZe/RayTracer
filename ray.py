from vector import Point3, Vector3
import taichi as ti

@ti.data_oriented
class Ray:
    def __init__(self, origin:Point3=None, direction:Vector3=None):
        self.origin = origin
        self.direction = direction

    @ti.pyfunc
    def at(self, t):
        return self.origin +  self.direction.multiply(t)
    
    @ti.pyfunc
    def copy(self, r):
        self.origin = r.origin
        self.direction = r.direction
        
if __name__=='__main__':
    ti.init()
    org = Point3(1,2,3)
    direc = Vector3(1,2,3)
    ray1 = Ray(org, direc)
    print(ray1.at(1.5))
