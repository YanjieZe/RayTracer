import numpy as np
from PIL import Image,ImageOps
from tqdm import tqdm
from vector import Vector3, Point3, Color
from ray import Ray
import argparse
import math
from util import *
from hittable import HittableList, Hittable, HitRecord
from sphere import Sphere
from camera import Camera

def ray_color(r: Ray, world:Hittable):

    hit_record = HitRecord()

    if world.hit(r=r, t_min=0, t_max=infinity, hit_record=hit_record):
        return (hit_record.normal + Color(1,1,1)).multiply(0.5)

    unit_direction = r.direction.unit_vector()

    t = 0.5 * (unit_direction.y + 1) # select color based on y value
    
    return Color(1,1,1).multiply(1.0 - t) + Color(0.5, 0.7, 1.0).multiply(t)



class RayTracer:
    def __init__(self, image_width=256, aspect_ratio=16.0/9.0, samples_per_pixel=10):

        # Image
        self.image_width = int(image_width)
        self.image_height = int(self.image_width/aspect_ratio)
        self.samples_per_pixel = samples_per_pixel

        self.image = np.zeros([self.image_width, self.image_height,3],dtype=np.uint8)
        


        # camera (coordinate)
        self.camera = Camera()

        
        # World
        self.world = HittableList()
        self.world.add(Sphere(cen=Point3(0,0,-1),r=0.5))
        self.world.add(Sphere(cen=Point3(0,-100.5,-1), r=100)) 

        # my test
        # self.world.add(Sphere(cen=Point3(0,0.2,-0.5),r=0.5))
    


    def write_color(self, x:int, y:int, color:Color, samples_per_pixel:int):

        scale = 1.0/samples_per_pixel

        r = color.x
        g = color.y
        b = color.z
        r *= scale
        g *= scale
        b *= scale

        self.image[x][y][0] = int(255.99 * r)
        self.image[x][y][1] = int(255.99 * g)
        self.image[x][y][2] = int(255.99 * b)

        # self.image[x][y][0] = int(255.99 * clamp(r, 0.0, 1))
        # self.image[x][y][1] = int(255.99 * clamp(r, 0.0, 0.999))
        # self.image[x][y][2] = int(255.99 * clamp(r, 0.0, 0.999))



    def render(self):

        for i in tqdm(range(self.image_width), desc='Render Progress'):
            for j in range(self.image_height):

                pixel_color = Color(0., 0., 0.)
                for k in range(self.samples_per_pixel):

                    # by inject random noise, multiple sampling
                    u = float(i+random_float()) / (self.image_width-1)
                    v = float(j+random_float()) / (self.image_height-1)

                    r = self.camera.get_ray(u=u, v=v)
                    pixel_color = pixel_color  + ray_color(r, self.world)

                self.write_color(x=i, y=j, color=pixel_color, samples_per_pixel=self.samples_per_pixel)

                
        
        img = Image.fromarray(self.image.transpose(1,0,2))
        img = ImageOps.flip(img)
        # print(img)
        img.show()
        img.save('1.png')
        

parser = argparse.ArgumentParser(description='Ray Tracer in Python')
parser.add_argument('--sample', type=int, default=10, help='Num of samples per pixel')

if __name__=='__main__':
    args = parser.parse_args()
    print(args)
    ray_tracer = RayTracer(samples_per_pixel=args.sample)
    ray_tracer.render()
