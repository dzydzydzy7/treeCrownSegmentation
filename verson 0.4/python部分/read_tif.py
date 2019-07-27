import numpy as np
from scipy import misc
from PIL import Image
from matplotlib import pyplot as plt
from matplotlib.image import imsave
import common as co
import math
import cv2

dic = "data/clip1/"
pic = "dsm_clip1.tif"


dsm = misc.imread(dic + pic) #tif
print dsm.shape

a = 3929/2268.0
b = 978/564.0
print a,b

#dsm = cv2.imread(dic + pic)
#dsm = dsm[:,:,0].astype(np.float32)

print type(dsm[0][0])
print dsm.shape
co.show_image(dsm)

'''
maxn = np.max(dsm)
dsm[dsm == np.min(dsm)] = maxn + 1
co.show_image(dsm)
'''

def slide_window_grey(image, px):
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
        rectangle = (one_wd-np.min(one_wd))/(np.max(one_wd)-np.min(one_wd))
        rectangle = rectangle * 255
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

    final_rect = np.array(final_rect).astype(np.uint8)
    print type(final_rect)
    print np.array(final_rect).shape
    return final_rect

#dsm_uint8 = slide_window_grey(dsm, 800)


dsm_norm = (dsm-np.min(dsm))/(np.max(dsm)-np.min(dsm))
co.show_image(dsm_norm)
dsm_uint8 = (dsm_norm * 255).astype(np.uint8)
#dsm_uint8[dsm_uint8 == 255] = 0

co.show_image(dsm_uint8)
dsm_grey = co.gray_rgb(dsm_uint8)
co.imsave(dic + "rgb_clip1.png", dsm_grey)