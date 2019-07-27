import cv2
import cv2.cv2 as cv
import common as co
from matplotlib.image import imsave

dic = "data/clip1/"
pic = "rgb_clip1.tif"
length = 1400   #1400 1100
width = 1000     #1000 800

img = cv.imread(dic + pic)
img0 = img[:,:,0]
img1 = img[:,:,1]
img2 = img[:,:,2]

print type(img0)

img_clip0 = img0[200:360, 213:373]
img_clip1 = img1[200:360, 213:373]
img_clip2 = img2[200:360, 213:373]

merged = cv2.merge([img_clip2,img_clip1,img_clip0])
co.imsave(dic + "topss.png", merged)

'''
B = cv2.resize(img0,(length, width))
G = cv2.resize(img1,(length, width))
R = cv2.resize(img2,(length, width))

merged = cv2.merge([R,G,B])
cv2.imshow("Merged",merged)
co.imsave(dic + "resized.png", merged)
'''