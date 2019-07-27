import numpy as np
import cv2 as cv
import cv2
from PIL import Image
import sys
from matplotlib import pyplot as plt
from matplotlib.image import imsave
from skimage import data,filters,segmentation,measure,morphology,color
from PIL import ImageEnhance

def show_image(arr):
    plt.imshow(arr)
    plt.show()

image = cv.imread("data/trees/img_grey.png")

def shrink(arr, maxn, white_digree):
    maxx = np.max(arr)
    minn = np.min(arr)
    sub = (maxx - minn)/white_digree
    print maxn
    print maxx
    print minn
    print sub
    arr_a = (arr - minn) / sub
    arr_r = arr_a * maxn
    return arr_r

gray_lap = np.abs(cv2.Laplacian(image, cv2.CV_16S, ksize = 3))
gray_lap = shrink(gray_lap, 255, 3)
show_image(gray_lap)
imsave("data/trees/LoG3.png", gray_lap)

after_lap = image + gray_lap
print after_lap.shape
show_image(after_lap)
imsave("data/trees/after_lap.png", after_lap)


'''
LoG3 = np.array([[0,-1,0],
                 [-1,4,-1],
                 [0,-1,0]])

LoG5 = np.array([[-2, -4, -4, -4, -2],
                [-4, 0, 8, 0, -4],
                [-4, 8, 24, 8, -4],
                [-4, 0, 8, 0, -4],
                [-2, -4, -4, -4, -2]])

output_LoG5 = np.abs(cv2.filter2D(image,-1,LoG5))
show_image(output_LoG5)
imsave("data/trees/LoG5.png", output_LoG5)

output_LoG3 = np.abs(cv2.filter2D(image,-1,LoG3))
show_image(output_LoG3)
imsave("data/trees/LoG3.png", output_LoG3)
'''


'''
img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
thresh =filters.threshold_otsu(img_gray)
bw =morphology.closing(img_gray > thresh)
print bw.shape
show_image(bw)
'''


sobel_x = np.array([[-1, -2, -1],
                   [0, 0, 0],
                   [1, 2, 1]])
sobel_y = np.array([[-1, 0, 1],
                   [-2, 0, 2],
                   [-1, 0, 1]])
output_1 = cv2.filter2D(after_lap,-1,sobel_x)
output_2 = cv2.filter2D(after_lap,-1,sobel_y)

output_1 = np.abs(output_1)
output_2 = np.abs(output_2)

output = output_1 + output_2
output = shrink(output, 255, 3)
show_image(output)
output = after_lap - output

show_image(output)
imsave("data/trees/sobel.png", output)


'''
kernel_sharpen_1 = np.array([
	        [-1,-1,-1],
	        [-1,9,-1],
	        [-1,-1,-1]])
kernel_sharpen_2 = np.array([
	    [1,1,1],
	    [1,-7,1],
	    [1,1,1]])
'''	
# 522
# 333