from vector import Vector3, Point3, Color
from ray import Ray


class HitRecord:
    def __init__(self, p:Point3=None, normal:Vector3=None, t:float=None):
        self.p = p
        self.normal = normal
        self.t = t
        self.front_face = None

        # material
        self.material = None 
    
    def set_face_normal(self, r:Ray, outward_normal:Vector3):
        self.front_face = r.direction.dot(outward_normal) < 0
        # if front face is True, the ray is outside the object

        # We always want the normal against the ray
        self.normal =  outward_normal if self.front_face else  outward_normal.negative()

    def __str__(self):
        print('p:', self.p)
        print('normal:', self.normal)
        print('t:', self.t)
        print('front face:', self.front_face)

    def copy(self, tmp_record):
        self.p = tmp_record.p
        self.normal = tmp_record.normal
        self.t = tmp_record.t
        self.front_face = tmp_record.front_face
        self.material = tmp_record.material

class Hittable:
    def __init__(self):
        pass
    
    def hit(self, r:Ray, t_min:float, t_max:float, hit_record:HitRecord):
        raise NotImplementedError()


class HittableList(Hittable):
    def __init__(self):
        self.object_list = []

    def add(self, obj:Hittable):
        self.object_list.append(obj)
    
    def hit(self, r:Ray, t_min:float, t_max:float, hit_record:HitRecord):
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