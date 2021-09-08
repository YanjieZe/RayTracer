from hittable import HitRecord
from ray import Ray
from vector import Vector3, Color, Point3 , random_unit_vector, \
    reflect, random_in_unit_sphere, refract, random_float
import math
import taichi as ti

@ti.data_oriented
class Material:
    def __init__(self):
        pass
    
    @ti.pyfunc
    def scatter(self, r_in, hit_record, attenuation, scattered):
        raise NotImplementedError()


@ti.data_oriented
class Lambertian(Material):
    def __init__(self, albedo):
        self.albedo = albedo
    
    @ti.pyfunc
    def scatter(self, r_in, hit_record, attenuation, scattered):

        scatter_direction = hit_record.normal + random_unit_vector()

        if scatter_direction.near_zero():
            scatter_direction = hit_record.normal

        scattered_new = Ray(hit_record.p, scatter_direction)
        scattered.direction = scattered_new.direction
        scattered.origin = scattered_new.origin

        attenuation.copy(self.albedo)

        return True

@ti.data_oriented
class Metal(Material):
    def __init__(self, albedo:Color , fuzz:float):
        self.albedo = albedo
        self.fuzz = fuzz if fuzz<1 else 1
    
    @ti.pyfunc
    def scatter(self, r_in, hit_record, attenuation, scattered):
        reflected = reflect(r_in.direction.unit_vector(), hit_record.normal) # get the reflected vector
        
        scattered_new = Ray(hit_record.p, reflected + random_in_unit_sphere().multiply(self.fuzz))
        
        scattered.direction = scattered_new.direction
        scattered.origin = scattered_new.origin

        attenuation.copy(self.albedo)
        
        return (scattered.direction.dot(hit_record.normal)>0)

@ti.data_oriented
class Dielectric(Material):
    def __init__(self, ir:float):
        self.ir = ir # index of refraction
    
    @ti.pyfunc
    def scatter(self, r_in, hit_record, attenuation, scattered):

        attenuation.copy(Color(1,1,1))

        refraction_ratio =  1.0/self.ir if hit_record.front_face else self.ir
        unit_direction = r_in.direction.unit_vector()

        cos_theta = min(unit_direction.negative().dot(hit_record.normal), 1.0)
        sin_theta = math.sqrt(1.0 - cos_theta*cos_theta)

        cannot_refract = refraction_ratio * sin_theta > 1.0
        # judge whether can refract
        if cannot_refract or self.reflectance(cos_theta, refraction_ratio)>random_float():
            direction = reflect(unit_direction, hit_record.normal)
        else:
            direction = refract(unit_direction, hit_record.normal, refraction_ratio)

        scattered.copy(Ray(hit_record.p, direction))
        return True
    
    @ti.pyfunc
    def reflectance(self, cosine, ref_idx):
        # Schlick's approximation
        r0 = (1-ref_idx) / (1+ref_idx)
        r0 = r0 * r0
        return r0 + (1-r0)*math.pow((1-cosine), 5)
