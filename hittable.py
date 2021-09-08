from vector import Vector3, Point3, Color
from ray import Ray
import taichi as ti

@ti.data_oriented
class HitRecord:
    def __init__(self, p:Point3=None, normal:Vector3=None, t:float=None):
        self.p = p
        self.normal = normal
        self.t = t
        self.front_face = None

        # material
        self.material = None 
    
    @ti.pyfunc
    def set_face_normal(self, r, outward_normal):
        self.front_face = r.direction.dot(outward_normal) < 0
        # if front face is True, the ray is outside the object

        # We always want the normal against the ray
        self.normal =  outward_normal if self.front_face else  outward_normal.negative()

    @ti.pyfunc
    def __str__(self):
        print('p:', self.p)
        print('normal:', self.normal)
        print('t:', self.t)
        print('front face:', self.front_face)

    @ti.pyfunc
    def copy(self, tmp_record):
        self.p = tmp_record.p
        self.normal = tmp_record.normal
        self.t = tmp_record.t
        self.front_face = tmp_record.front_face
        self.material = tmp_record.material

@ti.data_oriented
class Hittable:
    def __init__(self):
        pass
    
    @ti.pyfunc
    def hit(self, r, t_min, t_max, hit_record):
        raise NotImplementedError()


@ti.data_oriented
class HittableList(Hittable):
    def __init__(self):
        self.object_list = []

    @ti.pyfunc
    def add(self, obj):
        self.object_list.append(obj)
    
    @ti.pyfunc
    def hit(self, r, t_min, t_max, hit_record):
        """
        Detect whether the ray hits something in the hittable list, and hit what.
        """
        tmp_record = HitRecord()
        hit_anything = False # whether hit
        closet_so_far = t_max

        for obj in self.object_list:
            if obj.hit(r, t_min, closet_so_far, tmp_record):
                # if hit, update record
                hit_anything = True
                closet_so_far = tmp_record.t
                # copy
                hit_record.copy(tmp_record)

                

        return hit_anything