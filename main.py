import numpy as np
from PIL import Image
from tqdm import tqdm

class RayTracer:
    def __init__(self, image_width=256, image_height=256):
        self.image_width = 256
        self.image_height = 256
        # three channel: R, G, B
        self.image = np.zeros([self.image_width, self.image_height,3],dtype=np.uint8)
    
    def render(self):

        for i in tqdm(range(self.image_height), desc='Render Progress'):
            for j in range(self.image_width):

                r = i/(self.image_height -1)
                g = j/(self.image_width - 1)
                b = 0.25

                self.image[i][j][0] = int(255.99 * r)
                self.image[i][j][1] = int(255.99 * g)
                self.image[i][j][2] = int(255.99 * b)

        img = Image.fromarray(self.image)
        img.show()
        img.save('1.png')
        


if __name__=='__main__':
    ray_tracer = RayTracer()
    ray_tracer.render()
