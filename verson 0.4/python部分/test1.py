import os
import sys
import skimage
import math
from PIL import Image
import numpy as np
from skimage.morphology import watershed
from skimage.feature import peak_local_max
from skimage import morphology
from skimage.segmentation import random_walker
import matplotlib.pyplot as plt
from scipy import ndimage
from skimage import io
from matplotlib.image import imsave
import cv2
import cv2.cv2 as cv
from skimage.filters import thresholding,_rank_order
import time
from skimage.morphology import rectangle

def show_image(arr):
    plt.imshow(arr)
    plt.show()


def OSTU_threshold(image, px):
    #resize image
    width = int(math.ceil(float(image.shape[0])/px) * px)
    length = int(math.ceil(float(image.shape[1])/px) * px)
    img_resize = cv2.resize(image,(length, width))
    print img_resize.shape
    imsave("data/img_resize.png",img_resize)
    #divide windows
    wds = []
    for i in range(img_resize.shape[0]/px):
        for j in range(img_resize.shape[1]/px):
            wds.append(img_resize[i * px:i * px + px, j * px:j * px + px])
    print np.array(wds).shape

    #OTSU threshold
    ths = []
    rects = []
    for one_wd in wds:
        threshold, rectangle = cv2.threshold(one_wd, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU) #only black
        ths.append(threshold)
        rects.append(rectangle.tolist())
    print type(rects)
    print np.array(rects).shape

    #merge windows
    final_rect = []
    for i in range(img_resize.shape[0]/px):
        lines = []
        for k in range(px):
            line = []
            for j in range(img_resize.shape[1]/px):
                line.extend(rects[i * img_resize.shape[1]/px + j][k])
            lines.append(line)
        final_rect.extend(lines)
    print type(final_rect)
    print np.array(final_rect).shape
    return final_rect

image = cv2.imread("data/DJI_0330.JPG")
image_color = image     #is this sentence useful?
print image_color.shape #600 600 3 three dimension

#define region of interset
roi_x1 = image.shape[0] #length of the picture
roi_y1 = image.shape[1] #width of the picture
roi_x2 = 0
roi_y2 = 0

image = image[roi_x2:roi_x1, roi_y2:roi_y1] #get the region of interset

print image.ndim

if image.ndim == 3:
    print "Extract night-time ozone profile channel"
    #image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)    
    image = image[:,:,2]#take only the one dimension (green good, blue good, red shit)
    print image.shape
else:
    print "not one dimension image"

print "OTSU Threshold with sliding window" #OTSU threshold means da_jin_fa_zhi_fa

final_rect = OSTU_threshold(image, 200)

len_x = np.array(final_rect).shape[0]
len_y = np.array(final_rect).shape[1]
print(np.array(final_rect).shape)

#convert not zero to 1
for i in range(len_x):
    for j in range(len_y):
        if final_rect[i][j] != 0:
            final_rect[i][j] = 0
        else:
            final_rect[i][j] = 1

#show image
show_image(final_rect)

#Exact euclidean distance transform.
distance = ndimage.distance_transform_edt(final_rect)
print distance.shape
#np.savetxt("output_label.txt", distance, fmt = "%.3f")

#Exact local maxima(tree's peak)
binary_rect = np.array(final_rect)
local_maxi = peak_local_max(distance, indices=False, footprint=np.ones((55,55)),threshold_abs = 10, labels = binary_rect)
print type(local_maxi)
print local_maxi.shape
show_image(local_maxi)

#zengqiang peak? ba peak ju zai yi qi?
markers = morphology.label(local_maxi)
print type(markers)
print markers.shape
show_image(markers)

#watershed
start_ws = time.clock() #time when start watershed
labels_ws = watershed(-distance, markers, mask=binary_rect)
end_ws = time.clock()
time_ws = end_ws - start_ws
print type(labels_ws)
print labels_ws.shape
show_image(labels_ws)

print "Find detected trees in watershed"
slices = ndimage.find_objects(labels_ws)
print type(slices)
print np.array(slices).shape

circle_image_ws = np.zeros(shape=(roi_x1-roi_x2,roi_y1-roi_y2,3),dtype=np.uint8)
circle_image_ws[:]=254
print circle_image_ws.shape

image_sep = np.zeros(shape=(roi_x1-roi_x2,roi_y1-roi_y2,1),dtype=np.uint8)
for i in range(np.array(slices).shape[0]):
    x,y = [(side.start+side.stop)/2. for side in slices[i]]
    cv2.circle(circle_image_ws,(int(y),int(x)),25,(0,0,0),4)
    x = int(x)
    y = int(y)
    image_sep[x,y] = 255

imsave("data/circle_image_ws.png",circle_image_ws)

list_sep_ws = np.where(image_sep==255)
tree_num = np.array(slices).shape[0]
print "Number of detected trees in watershed: ", tree_num

img1 = Image.open( "data/DJI_0330.JPG")
img1 = img1.convert('RGBA')
 
img2 = Image.open( "data/circle_image_ws.png")
img2 = img2.convert('RGBA')
    
img = Image.blend(img1, img2, 0.3)
img.show()
img.save("data/res.png")
