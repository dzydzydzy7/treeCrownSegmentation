import os
import math
import numpy as np
import cv2
import cv2.cv2 as cv
from scipy import misc
from matplotlib.image import imsave
from PIL import Image

dic = "data/clip1/" # 1 2

width = 1322    # 1322 1087
height = 993    # 993 774
#l = 5651
#w = 2594

'''
dsm = misc.imread(dic + "dsm_clip2.tif")
print dsm.shape
dsm = dsm - np.min(dsm)
print np.min(dsm)
print np.max(dsm)
np.savetxt(dic + "dsm.txt", dsm, fmt = "%6.3f")
'''

#ttop = np.loadtxt("E:/console/watershed/watershed/treeTop.txt")
ttop = np.loadtxt("E:/console/merge/merge/out_merge.txt")
mtop = np.loadtxt("E:/console/TreeTopMatch/TreeTopMatch/mtop.txt")
print ttop.shape
print mtop.shape

circle_image = np.zeros(shape=(height,width,3),dtype=np.uint8)
circle_image[:] = 255
for i in range(np.array(ttop).shape[0]):
    cv2.circle(circle_image,(int(ttop[i][1]),int(ttop[i][0])),6,(0,0,255),6)

#for i in range(np.array(mtop).shape[0]):
#    cv2.circle(circle_image,(int(mtop[i][0]),int(mtop[i][1])),3,(0,0,255),3)

imsave(dic + "circle_image.png",circle_image)

img = cv.imread(dic + "circle_image.png")
img0 = img[:,:,0]
img1 = img[:,:,1]
img2 = img[:,:,2]

#B = cv2.resize(img0,(l, w))
#G = cv2.resize(img1,(l, w))
#R = cv2.resize(img2,(l, w))

#merged = cv2.merge([R,G,B])
merged = cv2.merge([img0, img1, img2])
imsave(dic + "circle_image.png", merged)

imsave(dic + "circle_image.png", merged)

img1 = Image.open( dic + "rgb_clip1.tif") # 1 2
img1 = img1.convert('RGBA')
 
img2 = Image.open( dic + "circle_image.png")
img2 = img2.convert('RGBA')
    
img = Image.blend(img1, img2, 0.3)
img.show()
img.save(dic + "res_t2.png")


'''
def get_round(matr, radius, x, y, value):
    xmin = 0 if x - radius < 0 else x - radius
    xmax = matr.shape[1] if x + radius > matr.shape[1] else x + radius
    ymin = 0 if y - radius < 0 else y - radius
    ymax = matr.shape[0] if y - radius > matr.shape[0] else y + radius
    
    circle = []
    for i in range(ymin, ymax):
        for j in range(xmin, xmax):
            xx = math.fabs(x - j)
            yy = math.fabs(y - i)
            if (xx * xx + yy * yy) >= radius * radius and xx + yy != 0:
                circle.append(matr[i][j])
    circle = np.array(circle)
    if np.max(circle) < value:
        return True
    else:
       return False

ttop = []
count = 0
for i in range(dsm.shape[0]):
    for j in range(dsm.shape[1]):
        if(get_round(dsm, 25, j, i, dsm[i][j])):
            ttop.append([i, j])
            count += 1
            print count

print np.array(ttop).shape
print count
'''