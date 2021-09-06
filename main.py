import numpy as np
from PIL import Image,ImageOps
from tqdm import tqdm
from vector import *
from ray import Ray
import argparse
import math
from util import *
from hittable import HittableList, Hittable, HitRecord
from sphere import Sphere
from camera import Camera
from material import *
from threading import Thread

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


def random_scene():
    world = HittableList()
    ground_material = Lambertian(Color(0.5, 0.5, 0.5))
    world.add(Sphere(Point3(0,-1000,0), 1000, ground_material))

    for a in range(-11, 11):
        for b in range(-11, 11):
            choose_mat = random_float()
            center = Point3(a+0.9*random_float(), 0.2, b+0.9*random_float())

            if (center - Point3(4, 0.2, 0)).length() > 0.9:
                if choose_mat < 0.8:
                    # diffuse
                    albedo = random_color().mul(random_color())
                    sphere_material = Lambertian(albedo)
                    world.add(Sphere(center, 0.2, sphere_material))
                elif choose_mat < 0.95:
                    # metal
                    albedo = random_color(0.5, 0.1)
                    fuzz = random_float(0, 0.5)
                    sphere_material = Metal(albedo, fuzz)
                    world.add(Sphere(center, 0.2, sphere_material))
                else:
                    # glass
                    sphere_material = Dielectric(1.5)
                    world.add(Sphere(center, 0.2, sphere_material))

    material1= Dielectric(1.5)
    world.add(Sphere(Point3(0,1,0), 1.0, material1))

    material2= Lambertian(Color(0.4, 0.2, 0.1))
    world.add(Sphere(Point3(-4, 1, 0), 1.0, material2))

    material3 = Metal(Color(0.7,0.6,0.5), 0.0)
    world.add(Sphere(Point3(4,1,0), 1.0, material3))
    print('World Created.')
    return world


class RayTracer:
    def __init__(self, image_width=1200, aspect_ratio=3.0/2.0, 
                samples_per_pixel=500,
                max_depth=50,
                num_thread=4):

        # Image
        self.image_width = int(image_width)
        self.image_height = int(self.image_width/aspect_ratio)
        self.samples_per_pixel = samples_per_pixel

        self.image = np.zeros([self.image_width, self.image_height,3],dtype=np.uint8)
        
        self.max_depth = max_depth

        self.num_thread = num_thread
        
        # World
        self.world = random_scene()


        # camera 
        lookfrom = Point3(13, 2, 3)
        lookat = Point3(0,0,0)
        vup = Vector3(0, 1, 0)
        dist_to_focus = 10.0
        aperture = 0.1
        self.camera = Camera(lookfrom=lookfrom, lookat=lookat, vup=Vector3(0,1,0), vfov=20,\
             aspect_ratio=aspect_ratio, aperture=aperture, focus_dist=dist_to_focus)
    


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


    def render_for_one_thread(self, i, j):
        pixel_color = Color(0., 0., 0.)
        for k in range(self.samples_per_pixel):

            # by inject random noise, multiple sampling
            u = float(i+random_float()) / (self.image_width-1)
            v = float(j+random_float()) / (self.image_height-1)

            r = self.camera.get_ray(u=u, v=v)
            pixel_color = pixel_color  + ray_color(r, self.world, self.max_depth)

        self.write_color(x=i, y=j, color=pixel_color, samples_per_pixel=self.samples_per_pixel)

    def render(self):

        for i in tqdm(range(self.image_width), desc='Render Progress'):
            int_image_height = (int(self.image_height/self.num_thread))*self.num_thread
            for j in range(0, int_image_height, self.num_thread):
                thread_list = []
                for t in range(self.num_thread):
                    thread_list.append(Thread(target=self.render_for_one_thread, args=(i,j+t)))

                for t in range(self.num_thread):
                    thread_list[t].start()

                for t in range(self.num_thread):
                    thread_list[t].join()

            # remaining
            for j in range(int_image_height, self.image_height):
                self.render_for_one_thread(i, j)

                
        
        img = Image.fromarray(self.image.transpose(1,0,2))
        img = ImageOps.flip(img)
        img.show()
        img.save('1.png')
        

parser = argparse.ArgumentParser(description='Ray Tracer in Python')
parser.add_argument('--img_width', type=int, default=256, help='Width of img')
parser.add_argument('--sample', type=int, default=1, help='Num of samples per pixel')
parser.add_argument('--recursion', type=int, default=5, help='Num of maximum recursion depth')
parser.add_argument('--thread', default=16, type=int, help='Num of threads')

if __name__=='__main__':
    args = parser.parse_args()
    print(args)
    ray_tracer = RayTracer(image_width=args.img_width,
                            samples_per_pixel=args.sample,
                            max_depth=args.recursion,
                            num_thread=args.thread)
    ray_tracer.render()
