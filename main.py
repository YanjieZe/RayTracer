import numpy as np
from PIL import Image,ImageOps
from tqdm import tqdm
from vector import Vector3, Point3, Color, random_in_hemisphere
from ray import Ray
import argparse
import math
from util import *
from hittable import HittableList, Hittable, HitRecord
from sphere import Sphere
from camera import Camera
from material import *

def ray_color(r: Ray, world:Hittable, depth:int):

    hit_record = HitRecord()
    if depth<=0:
        return Color(0, 0, 0)
   
    if world.hit(r=r, t_min=0.001, t_max=infinity, hit_record=hit_record):
        scattered = Ray()
        attenutation = Color()
        
        if hit_record.material.scatter(r, hit_record, attenutation, scattered):
            # use the scattered
            return attenutation.mul(ray_color(scattered, world, depth-1)) 
        return  Color(0,0,0)

    unit_direction = r.direction.unit_vector()

    t = 0.5 * (unit_direction.y + 1) # select color based on y value
    
    return Color(1,1,1).multiply(1.0 - t) + Color(0.5, 0.7, 1.0).multiply(t)



class RayTracer:
    def __init__(self, image_width=256, aspect_ratio=16.0/9.0, 
                samples_per_pixel=10,
                max_depth=50):

        # Image
        self.image_width = int(image_width)
        self.image_height = int(self.image_width/aspect_ratio)
        self.samples_per_pixel = samples_per_pixel

        self.image = np.zeros([self.image_width, self.image_height,3],dtype=np.uint8)
        
        self.max_depth = max_depth


        # camera (coordinate)
        self.camera = Camera()

        
        # World
        self.world = HittableList()

        material_ground = Lambertian(Color(0.8, 0.8, 0.0))
        material_center = Lambertian(Color(0.1,0.2,0.5))
        material_left = Dielectric(ir=1.5)
        material_right = Metal(Color(0.8, 0.6, 0.2), fuzz=0.0)

        self.world.add(Sphere(cen=Point3(0,0,-1),r=0.5,m=material_center))
        self.world.add(Sphere(cen=Point3(0,-100.5,-1), r=100,m=material_ground)) 
        self.world.add(Sphere(cen=Point3(-1,0,-1), r=0.5,m=material_left)) 
        self.world.add(Sphere(cen=Point3(-1.0, 0.0, -1.0), r=-0.4, m=material_left))
        self.world.add(Sphere(cen=Point3(1, 0,-1), r=0.5,m=material_right)) 

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

        r = math.sqrt(r)
        g = math.sqrt(g)
        b = math.sqrt(b)

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
                    pixel_color = pixel_color  + ray_color(r, self.world, self.max_depth)

                self.write_color(x=i, y=j, color=pixel_color, samples_per_pixel=self.samples_per_pixel)

                
        
        img = Image.fromarray(self.image.transpose(1,0,2))
        img = ImageOps.flip(img)
        img.show()
        img.save('1.png')
        

parser = argparse.ArgumentParser(description='Ray Tracer in Python')
parser.add_argument('--img_width', type=int, default=256, help='Width of img')
parser.add_argument('--sample', type=int, default=10, help='Num of samples per pixel')
parser.add_argument('--recursion', type=int, default=50, help='Num of maximum recursion depth')


if __name__=='__main__':
    args = parser.parse_args()
    print(args)
    ray_tracer = RayTracer(image_width=args.img_width,
                            samples_per_pixel=args.sample,
                            max_depth=args.recursion)
    ray_tracer.render()
