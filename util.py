import random


# some constants
infinity = float("inf")
pi = 3.1415926535897932385

def degrees_to_radians(degrees:float):
    return degrees * pi / 180.0


def random_float(min_val:float=None, max_val:float=None):
    if min_val is None:
        return random.random() # range from [0, 1)
    else:
        return min_val + (max_val - min_val) * random.random()

def clamp(x:float, min:float, max:float):
    if (x<min): 
        return min
    if (x>max): 
        return max
    return x

if __name__=='__main__':
    print(random_float(10,100))
