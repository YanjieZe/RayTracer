from hittable import HitRecord, Hittable
from vector import Vector3, Point3, Color
from ray import Ray
import math
from material import Material
import taichi as ti

@ti.data_oriented
class Sphere(Hittable):
    def __init__(self, cen:Point3, r:float, m:Material):
        self.center = cen
        self.radius = r
        self.material = m

    @ti.pyfunc
    def hit(self, r, t_min, t_max, hit_record):
        """
        (A+tB-C)*(A+tB-C)=r^2

        => delta = ...
        """
        
        A = r.direction.dot(r.direction)
        B = (r.origin - self.center).dot(r.direction)*2
        C = (r.origin - self.center).dot(r.origin - self.center) - self.radius*self.radius
        delta = B*B - 4*A*C
       

        if delta <0: # not hit
            return False 

        root = (-B - math.sqrt(delta))/(2*A)
        # find a point that is in the range
        if root>t_max or root<t_min:
            root = (-B + math.sqrt(delta))/(2*A)
            if root>t_max or root<t_min:
                return False

        hit_record.t = root
        hit_record.p = r.at(root)
        
        outward_normal = (hit_record.p - self.center)/self.radius
        hit_record.set_face_normal(r, outward_normal)
        hit_record.material = self.material # record material


        return True