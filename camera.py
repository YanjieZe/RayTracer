from util import *
from vector import Point3, Vector3, Color, degrees_to_radians, random_in_unit_sphere
from ray import Ray
import math


class Camera:
    def __init__(self, lookfrom:Point3, lookat:Point3, vup:Vector3, vfov:float,\
             aspect_ratio:float, aperture:float, focus_dist:float):
        self.theta = degrees_to_radians(vfov)
        self.h = math.tan(self.theta/2)

        self.aspect_ratio = aspect_ratio
        self.viewport_height = 2.0 * self.h
        self.viewport_width = self.aspect_ratio * self.viewport_height
        self.focal_length = 1.0

        w = (lookfrom - lookat).unit_vector()
        u = vup.cross(w).unit_vector()
        v = w.cross(u)

        self.w = w
        self.u = u
        self.v = v


        self.origin = lookfrom
        self.horizontal = self.u.multiply(self.viewport_width*focus_dist)

        self.vertical = self.v.multiply(self.viewport_height*focus_dist)

        self.lower_left_corner = self.origin - self.horizontal/2 - self.vertical/2 - w.multiply(focus_dist)

        self.lens_radius = aperture/2


    def get_ray(self, u:float, v:float):
        """
        Given the pixel coordinate in image, return the ray from the camera to the pixel
        """
        rd = random_in_unit_sphere().multiply(self.lens_radius)
        offset = self.u.multiply(rd.x) + self.v.multiply(rd.y)

        return Ray(self.origin+offset, \
            self.lower_left_corner + self.horizontal.multiply(u) + self.vertical.multiply(v)-self.origin-offset)
