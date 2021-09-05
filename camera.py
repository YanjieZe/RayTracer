from util import *
from vector import Point3, Vector3, Color
from ray import Ray


class Camera:
    def __init__(self):

        self.aspect_ratio = 16.0/9.0
        self.viewport_height = 2.0
        self.viewport_width = self.aspect_ratio * self.viewport_height
        self.focal_length = 1.0

        self.origin = Point3(0,0,0)
        self.horizontal = Vector3(self.viewport_width, 0., 0.)
        self.vertical = Vector3(0., self.viewport_height, 0.)
        self.lower_left_corner = self.origin - self.horizontal/2 - self.vertical/2 - Vector3(0,0,self.focal_length)

    def get_ray(self, u:float, v:float):
        """
        Given the pixel coordinate in image, return the ray from the camera to the pixel
        """
        return Ray(self.origin, self.lower_left_corner + self.horizontal.multiply(u) + self.vertical.multiply(v)-self.origin)
