from hittable import HitRecord
from ray import Ray
from vector import Vector3, Color, Point3 , random_unit_vector, reflect, random_in_unit_sphere


class Material:
    def __init__(self):
        pass

    def scatter(self, r_in:Ray, hit_record:HitRecord, attenuation:Color, scattered:Ray):
        raise NotImplementedError()


class Lambertian(Material):
    def __init__(self, albedo:Color):
        self.albedo = albedo
    
    def scatter(self, r_in:Ray, hit_record:HitRecord, attenuation:Color, scattered:Ray):

        scatter_direction = hit_record.normal + random_unit_vector()

        if scatter_direction.near_zero():
            scatter_direction = hit_record.normal

        scattered_new = Ray(hit_record.p, scatter_direction)
        scattered.direction = scattered_new.direction
        scattered.origin = scattered_new.origin

        attenuation.copy(self.albedo)

        return True

class Metal(Material):
    def __init__(self, albedo:Color , fuzz:float):
        self.albedo = albedo
        self.fuzz = fuzz if fuzz<1 else 1
    
    def scatter(self, r_in:Ray, hit_record:HitRecord, attenuation:Color, scattered:Ray):
        reflected = reflect(r_in.direction.unit_vector(), hit_record.normal) # get the reflected vector
        
        scattered_new = Ray(hit_record.p, reflected + random_in_unit_sphere().multiply(self.fuzz))
        
        scattered.direction = scattered_new.direction
        scattered.origin = scattered_new.origin

        attenuation.copy(self.albedo)
        
        return (scattered.direction.dot(hit_record.normal)>0)

