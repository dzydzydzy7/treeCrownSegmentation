import numpy as np
import cv2 as cv
import cv2
import math
from PIL import Image
from PIL import ImageEnhance
import sys
from matplotlib import pyplot as plt
from matplotlib.image import imsave
from skimage import data,filters,segmentation,measure,morphology,color
import common as co

px = 100

dic = "data/tree/"
pic = "resized.png"

#dui bi du zeng qiang
img = Image.open(dic + pic)
enh_con = ImageEnhance.Contrast(img)
contrast = 2.0  
img_contrasted = enh_con.enhance(contrast)  
img_contrasted.show()
imsave(dic + "img_contrasted.png", img_contrasted)

img_contrasted = cv.imread(dic + "img_contrasted.png")
#img_contrasted = cv.imread(dic + pic)
#road = np.loadtxt('road.txt',dtype=np.int)
#img_contrasted = co.deroad(img_contrasted, road)
#co.show_image(img_contrasted)

#resize
image = cv2.cvtColor(img_contrasted, cv2.COLOR_BGR2GRAY)
width = int(math.ceil(float(image.shape[0])/px) * px)
length = int(math.ceil(float(image.shape[1])/px) * px)
image = cv2.resize(image,(length, width))
image_g = co.gray_rgb(image)
imsave(dic + "img_grey.png", image_g)

#laplacian
image_g = cv.imread(dic + "img_grey.png")
gray_lap = np.abs(cv2.Laplacian(image_g, cv2.CV_16S, ksize = 5))
gray_lap = co.shrink(gray_lap, 255, 5)
#co.show_image(gray_lap)
imsave(dic + "LoG3.png", gray_lap)

after_lap = image_g + gray_lap
print after_lap.shape
#co.show_image(after_lap)
imsave(dic + "after_lap.png", after_lap)

#sobel
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
output = co.shrink(output, 255, 6)
#co.show_image(output)
output = after_lap - output

#qu zao dian
co.show_image(output)
output = cv2.medianBlur(output, 5)
#co.show_image(output)
imsave(dic + "sobel.png", output)

#kai yun suan
image = morphology.opening(output[:,:,0], morphology.disk(12))
image_g = co.gray_rgb(image)
imsave(dic + "open_grey.png", image_g)

#laplacian
image_g = cv.imread(dic + "open_grey.png")
gray_lap = np.abs(cv2.Laplacian(image_g, cv2.CV_16S, ksize = 3))
gray_lap = co.shrink(gray_lap, 255, 5)
#co.show_image(gray_lap)
after_lap = image_g + gray_lap
print after_lap.shape

#qu zao dian
after_lap = cv2.medianBlur(after_lap, 5)
co.show_image(after_lap)
imsave(dic + "after_lap2.png", after_lap)

#bi yun suan
print image.shape
img_close = morphology.closing(after_lap[:,:,0], morphology.disk(10)) #close
co.show_image(img_close)
img_close_g = co.gray_rgb(img_close)
imsave(dic + "img_close.png", img_close_g)

#hui du zhi fang tu jun heng
img_close = cv.imread(dic + "img_close.png")
img_close = cv2.equalizeHist(img_close[:,:,0])
img_close = cv2.equalizeHist(img_close)
co.show_image(img_close)
img_close_g = co.gray_rgb(img_close)
print np.array(img_close_g).shape
imsave(dic + "img_close.png", img_close_g)

#53332