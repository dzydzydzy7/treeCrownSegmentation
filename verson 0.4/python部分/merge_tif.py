import numpy as np
from scipy import misc
from PIL import Image
from matplotlib import pyplot as plt
from matplotlib.image import imsave
import common as co
import math
import cv2

dic = "data/dsm/"

dsm_100 = cv2.imread(dic + "dsm_grey_sw100.png")
dsm_200 = cv2.imread(dic + "dsm_grey_sw200.png")

dsm_100200 = (dsm_100 + dsm_200)/2
co.show_image(dsm_100200)
imsave(dic + "dsm_grey_sw1_2.png", dsm_100200)