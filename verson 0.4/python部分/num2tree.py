import os
import math
import random
import numpy as np
import cv2
import cv2.cv2 as cv
from scipy import misc
from matplotlib.image import imsave
from PIL import Image

dic = "data/clip2/" # 1 2
width = 1087    # 1322 1087
height = 774    # 993 774

#trees = np.loadtxt("E:/RStudio/workplace/res_seeds_ws2.txt")
#trees = np.loadtxt("E:/RStudio/workplace/res_seeds.txt")
trees = np.loadtxt("E:/console/shiyan1/shiyan1/out.txt")
print trees.shape

shape_image = np.zeros(shape=(height,width,3),dtype=np.uint8)
shape_image[:] = 255
for i in range(np.array(shape_image).shape[0]):
    for j in range(np.array(shape_image).shape[1]):
            if trees[i][j]%11 == 0 and trees[i][j] != 0:
                shape_image[i][j][0] = 255
                shape_image[i][j][1] = 0
                shape_image[i][j][2] = 0
            elif trees[i][j]%11 == 1:
                shape_image[i][j][0] = 0
                shape_image[i][j][1] = 255
                shape_image[i][j][2] = 0
            elif trees[i][j]%11 == 2:
                shape_image[i][j][0] = 0
                shape_image[i][j][1] = 0
                shape_image[i][j][2] = 255
            elif trees[i][j]%11 == 3:
                shape_image[i][j][0] = 255
                shape_image[i][j][1] = 0
                shape_image[i][j][2] = 255
            elif trees[i][j]%11 == 4:
                shape_image[i][j][0] = 0
                shape_image[i][j][1] = 255
                shape_image[i][j][2] = 255
            elif trees[i][j]%11 == 5:
                shape_image[i][j][0] = 127
                shape_image[i][j][1] = 255
                shape_image[i][j][2] = 0
            elif trees[i][j]%11 == 6:
                shape_image[i][j][0] = 255
                shape_image[i][j][1] = 106
                shape_image[i][j][2] = 106
            elif trees[i][j]%11 == 7:
                shape_image[i][j][0] = 238
                shape_image[i][j][1] = 238
                shape_image[i][j][2] = 0
            elif trees[i][j]%11 == 8:
                shape_image[i][j][0] = 0
                shape_image[i][j][1] = 0
                shape_image[i][j][2] = 139
            elif trees[i][j]%11 == 9:
                shape_image[i][j][0] = 255
                shape_image[i][j][1] = 140
                shape_image[i][j][2] = 0
            elif trees[i][j]%11 == 10:
                shape_image[i][j][0] = 0
                shape_image[i][j][1] = 102
                shape_image[i][j][2] = 205

imsave(dic + "shape_image.png",shape_image)

img = cv.imread(dic + "shape_image.png")
img0 = img[:,:,0]
img1 = img[:,:,1]
img2 = img[:,:,2]

#B = cv2.resize(img0,(5651, 2594))
#G = cv2.resize(img1,(5651, 2594))
#R = cv2.resize(img2,(5651, 2594))

#merged = cv2.merge([R,G,B])
merged = cv2.merge([img0,img1,img2])

imsave(dic + "shape_image.png",merged)

img1 = Image.open( dic + "rgb_clip2.tif") # 1
img1 = img1.convert('RGBA')
 
img2 = Image.open( dic + "shape_image.png")
img2 = img2.convert('RGBA')
    
img = Image.blend(img1, img2, 0.3)
img.show()
img.save(dic + "res_seg_dal.png")

