from vector import Point3, Vector3

class Ray:
    def __init__(self, origin:Point3=None, direction:Vector3=None):
        self.origin = origin
        self.direction = direction

    def at(self, t:float):
        return self.origin +  self.direction.multiply(t)
    

if __name__=='__main__':
    org = Point3(1,2,3)
    direc = Vector3(1,2,3)
    ray1 = Ray(org, direc)
    print(ray1.at(1.5))
