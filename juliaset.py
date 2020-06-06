from PIL import Image, ImageDraw
from math import sqrt
from datetime import datetime
from random import randint
import os

class JuliaSet:
    def __init__(self, ca, cb, w, h, c_mode, date_img):
        self.ca = ca
        self.cb = cb
        self.w = w
        self.h = h
        self.c_mode = c_mode
        self.date_img = date_img
        self.image = Image.new("RGB",(w,h))
        self.draw = ImageDraw.Draw(self.image)
        
        rnd = lambda a,b: randint(a,b)
        self.colorbias = (rnd(20,200),rnd(20,200),rnd(20,200))
        self.glow = (rnd(0,20),rnd(0,20),rnd(0,20))

        self.t = datetime.now()
        self.minutes = self.t.minute if len(str(self.t.minute)) != 1 else "0" + str(self.t.minute)
        self.date_stamp = f"{self.t.month}/{self.t.day}/{self.t.year}"
        self.time_stamp = f"{self.t.hour}:{self.minutes}"

    def genImage(self, iter_per_pixel, zoom):
        for x in range(self.w):
            for y in range(self.h):
                za = self.translate(x,0,self.w,-zoom,zoom)
                zb = self.translate(y,0,self.h,-zoom,zoom)
                i = 0
                while i < iter_per_pixel:
                    tmp = 2 * za * zb
                    za = za * za - zb * zb + self.ca
                    zb = tmp + self.cb
                    if sqrt(za*za + zb*zb) > 4: break
                    i += 1
                self.draw.point((x,y), self.colorize(i, iter_per_pixel) if i != iter_per_pixel else (0,0,0))

    def saveImage(self,path):
        self.genName()
        print(f"{self.date_stamp} | {self.time_stamp} SAVED: {self.file_name}\nMODE: {self.c_mode}")
        if path != "saves" and not os.path.exists(path):
            os.mkdir(path)
        elif not os.path.exists("saves"):
            os.mkdir("saves")
        self.image.save(f"{path}/{self.file_name}","PNG")
    
    def genName(self):
        if self.date_img:
            self.file_name = f"image_{self.t.month}{self.t.day}{self.t.year}_{self.t.hour}{self.minutes}{self.t.second}.png"
        else: self.file_name = "image.png"

    def colorize(self, i, iter_per_pixel):
        if self.c_mode == "rand_color":
            c = int(self.translate(i,0,iter_per_pixel,0,255) * (i/4))
            return (c + self.colorbias[0],c + self.colorbias[1],c + self.colorbias[2])
        elif self.c_mode == "rand_pattern":
            if i % 2 == 0: return self.colorbias
            else: return (0,0,0)
        elif self.c_mode == "rand_glow":
            return (i*self.glow[0],i*self.glow[1],i*self.glow[2])
        else:
            print(f"Unknown color mode: '{self.c_mode}'")
            exit()

    def translate(self, value, leftMin, leftMax, rightMin, rightMax):
        return rightMin + (float(value - leftMin) / float(leftMax - leftMin) * (rightMax - rightMin))