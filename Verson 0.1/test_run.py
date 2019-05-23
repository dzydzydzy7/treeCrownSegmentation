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
import common as co

dic = "data/tree/"
pic = "img_close.png"

'''
img_contrasted = cv.imread(dic + "DJI_0330.JPG")
print img_contrasted.shape
#img_contrasted = co.green_digree(img_contrasted)
#img_contrasted = img_contrasted[:,:,0]
img_contrasted = np.array(cv2.cvtColor(img_contrasted, cv2.COLOR_BGR2GRAY))
img_contrasted = co.get_derode(img_contrasted)
print img_contrasted.shape
img_close = morphology.closing(img_contrasted, morphology.disk(20)) #close
co.show_image(img_close)
'''

img_close = cv.imread(dic + pic)
img_close = img_close[:,:,0]

#define region of interset
roi_x1 = img_close.shape[0] #length of the picture
roi_y1 = img_close.shape[1] #width of the picture
roi_x2 = 0
roi_y2 = 0

print "OTSU Threshold with sliding window" #OTSU threshold means da_jin_fa_zhi_fa
final_rect = co.OSTU_threshold(img_close, 200) #change to 200 is also good

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
co.show_image(final_rect)

#Exact euclidean distance transform.
distance = ndimage.distance_transform_edt(final_rect)
print distance.shape
#np.savetxt("output_label.txt", distance, fmt = "%.3f")

#Exact local maxima(tree's peak)
binary_rect = np.array(final_rect)                                      #85 85(200)
local_maxi = peak_local_max(distance, indices=False, footprint=np.ones((85,85)),threshold_abs = 1, labels = binary_rect)
print type(local_maxi)
print local_maxi.shape
co.show_image(local_maxi)

#zengqiang peak? ba peak ju zai yi qi?
markers = morphology.label(local_maxi)
print type(markers)
print markers.shape
co.show_image(markers)

roi_x1 = markers.shape[0]
roi_y1 = markers.shape[1]

#watershed
start_ws = time.clock() #time when start watershed
labels_ws = watershed(-distance, markers, mask=binary_rect)
end_ws = time.clock()
time_ws = end_ws - start_ws
print type(labels_ws)
print labels_ws.shape
co.show_image(labels_ws)

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
    cv2.circle(circle_image_ws,(int(y),int(x)),25,(0,0,255),3)
    x = int(x)
    y = int(y)
    image_sep[x,y] = 255

imsave(dic + "circle_image_ws_t.png",circle_image_ws)

list_sep_ws = np.where(image_sep==255)
tree_num = np.array(slices).shape[0]
print "Number of detected trees in watershed: ", tree_num

img1 = Image.open( dic + "resized.png")
img1 = img1.convert('RGBA')
 
img2 = Image.open( dic + "circle_image_ws_t.png")
img2 = img2.convert('RGBA')
    
img = Image.blend(img1, img2, 0.3)
img.show()
img.save(dic + "res_t1.png")
