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

def deroad(img, arr):
    for i in arr:
        img[i[0]][i[1]] = 0
    return img

def gray_rgb(img):
    img_gray_g = []
    for i in range(img.shape[0]):
        line = []
        for j in range(img.shape[1]):
            line.append((img[i][j],img[i][j],img[i][j]))
        img_gray_g.append(line)
    return img_gray_g

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

def OSTU_threshold(image, px):
    #resize image
    width = int(math.ceil(float(image.shape[0])/px) * px)
    length = int(math.ceil(float(image.shape[1])/px) * px)
    img_resize = cv2.resize(image,(length, width))
    print img_resize.shape
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

def get_derode(arr):
    road = []
    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            if arr[i][j] >= 247:
                arr[i][j] = 0
                road.append((i, j))
    road = np.array(road)
    np.savetxt("road.txt", road, fmt = "%d")
    np.savetxt("arr1.txt", arr, fmt = "%d")
    return np.array(arr)


def green_digree(arr):
    r = arr[:,:,0]
    g = arr[:,:,1]
    b = arr[:,:,2]
    r = np.multiply(r, 0.3)
    g = np.multiply(g, 0.5)
    b = np.multiply(b, 0.2)
    res = np.add(r, g)
    res = np.add(res, b)
    res = np.floor_divide(res, 3)
    return np.array(res)