"""
Tree Crown Segmentation with Watershed

python 2.7.16
backports.functools-lru-cache 1.5
cloudpickle                   1.1.1
cycler                        0.10.0
dask                          1.2.2
decorator                     4.4.0
kiwisolver                    1.1.0
matplotlib                    2.2.4
networkx                      2.2
numpy                         1.15.0
opencv-python                 4.1.0.25
Pillow                        6.0.0
pip                           18.1
pyparsing                     2.4.0
python-dateutil               2.8.0
pytz                          2019.1
PyWavelets                    1.0.3
scikit-image                  0.14.0
scipy                         1.2.1
setuptools                    40.6.2
six                           1.12.0
toolz                         0.9.0
"""
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

#start from here
#loading images
image = io.imread("img.jpg")
image_color = image     #is this sentence useful?
print image_color.shape #600 600 3 three dimension

ground_truth = cv2.imread("ground_truth.png")
ground_truth = cv2.cvtColor(ground_truth, cv2.COLOR_BGR2GRAY)
print ground_truth.shape    #600 600 double dimesion

#define region of interset
roi_x1 = image.shape[0] #length of the picture
roi_y1 = image.shape[1] #width of the picture
roi_x2 = 0
roi_y2 = 0

image = image[roi_x2:roi_x1, roi_y2:roi_y1] #get the region of interset
ground_truth = ground_truth[roi_x2:roi_x1, roi_y2:roi_y1]#x from 0 to 600 y from 0 to 600

print image.ndim
if image.ndim == 3:
    print "Extract night-time ozone profile channel"
    image = image[:,:,0]    #take only the first dimension(Red)
    print image.shape
else:
    print "not one dimension image"

print "OTSU Threshold with sliding window" #OTSU threshold means da_jin_fa_zhi_fa

#divide windows
wds = []
for i in range(6):
    for j in range(6):
        wds.append(image[i * 100:i * 100 + 100, j * 100:j * 100 + 100])#total 36 windows
print np.array(wds).shape

#OTSU threshold
ths = []
rects = []
for one_wd in wds:
    threshold, rectangle = cv2.threshold(one_wd, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU) #only black
    ths.append(threshold)
    rects.append(rectangle.tolist())

#merge windows
len = len(rects[0][0])
print len
final_rect = []
for i in range(6):
    lines = []
    for k in range(len):
        line = []
        for j in range(6):
            line.extend(rects[i * 6 + j][k])
        lines.append(line)
    final_rect.extend(lines)

len_x = np.array(final_rect).shape[0]
len_y = np.array(final_rect).shape[1]
print(np.array(final_rect).shape)

#convert not zero to 1
for i in range(len_x):
    for j in range(len_y):
        if final_rect[i][j] != 0:
            final_rect[i][j] = 1
        else:
            final_rect[i][j] = 0

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
    cv2.circle(circle_image_ws,(int(y),int(x)),5,(0,0,255),3)
    x = int(x)
    y = int(y)
    image_sep[x,y] = 255

imsave("circle_image_ws.png",circle_image_ws)

list_sep_ws = np.where(image_sep==255)
tree_num = np.array(slices).shape[0]
print "Number of detected trees in watershed: ", tree_num

img1 = Image.open( "img.jpg")
img1 = img1.convert('RGBA')
 
img2 = Image.open( "circle_image_ws.png")
img2 = img2.convert('RGBA')
    
img = Image.blend(img1, img2, 0.3)
img.show()
img.save("res.png")
