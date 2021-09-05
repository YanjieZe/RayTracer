import numpy as np
from PIL import Image,ImageOps
from tqdm import tqdm
from vector import Vector3, Point3, Color
from ray import Ray
import argparse
import math
from util import pi, infinity, degrees_to_radians
from hittable import HittableList, Hittable, HitRecord
from sphere import Sphere

def ray_color(r: Ray, world:Hittable):

    hit_record = HitRecord()

    if world.hit(r=r, t_min=0, t_max=infinity, hit_record=hit_record):
        return (hit_record.normal + Color(1,1,1)).multiply(0.5)

    unit_direction = r.direction.unit_vector()

    t = 0.5 * (unit_direction.y + 1) # select color based on y value
    
    return Color(1,1,1).multiply(1.0 - t) + Color(0.5, 0.7, 1.0).multiply(t)



class RayTracer:
    def __init__(self, image_width=256, aspect_ratio=16.0/9.0):

        # Image
        self.image_width = int(image_width)
        self.image_height = int(self.image_width/aspect_ratio)


        # three channel: R, G, B
        self.image = np.zeros([self.image_width, self.image_height,3],dtype=np.uint8)
        

        # camera (coordinate)
        self.viewport_height = 2.0
        self.viewport_width = aspect_ratio * self.viewport_height
        self.focal_length = 1.0 # the distance between the hole and the plane's center

        self.origin = Point3(0,0,0)
        self.horizontal = Vector3(self.viewport_width, 0, 0) # vector of hozirontal line
        self.vertical = Vector3(0, self.viewport_height, 0) # vector of vertical line
        self.lower_left_corner = self.origin - self.horizontal/2 - self.vertical/2 - Vector3(0,0,self.focal_length)
        # print('Lower left corner:', self.lower_left_corner)

        
        # World
        self.world = HittableList()
        self.world.add(Sphere(cen=Point3(0,0,-1),r=0.5))
        self.world.add(Sphere(cen=Point3(0,-100.5,-1), r=100)) 

        # my test
        # self.world.add(Sphere(cen=Point3(0,0.2,-0.5),r=0.5))
    
    def write_color(self, x:int, y:int, color:Color):
        self.image[x][y][0] = int(255.99 * color.x)
        self.image[x][y][1] = int(255.99 * color.y)
        self.image[x][y][2] = int(255.99 * color.z)

    def render(self):
        print('Img Shape:', self.image.shape)
        for i in tqdm(range(self.image_width), desc='Render Progress'):
            for j in range(self.image_height):

                u = float(i)/(self.image_width-1)
                v = float(j)/(self.image_height-1)
                r = Ray(self.origin, self.lower_left_corner + self.horizontal.multiply(u) + self.vertical.multiply(v)-self.origin)
                pixel_color = ray_color(r, self.world)
                
                self.write_color(x=i, y=j, color=pixel_color)

                
        
        img = Image.fromarray(self.image.transpose(1,0,2))
        img = ImageOps.flip(img)
        # print(img)
        img.show()
        img.save('1.png')
        
    

if __name__=='__main__':
    ray_tracer = RayTracer()
    ray_tracer.render()
