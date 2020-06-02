import cv2
from PIL import Image as im
import numpy as np
import os
import glob
import copy 
import re
import sys
from scipy.ndimage import interpolation as inter
def binarizeImg(img):
    # convert the image to grayscale and flip the foreground
    # and background to ensure foreground is now "white" and
    # the background is "black"
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)
    
    # threshold the image, setting all foreground pixels to
    # 255 and all background pixels to 0
    thresh = cv2.threshold(gray, 0, 255,
    	cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    return thresh

#+- 1.5 angle skew
def skewCorrection(img):
    def find_score(arr, angle):
        data = inter.rotate(arr, angle, reshape=False, order=0)
        hist = np.sum(data, axis=1)
        score = np.sum((hist[1:] - hist[:-1]) ** 2)
        return hist, score

        img = im.open(f1)
        i += 1

        # convert to binary
        wd, ht = img.size
        #pix = np.array(img.convert('1').getdata(), np.uint8)
        bin_img = 1 - (np.array(img).reshape((ht, wd)) / 255)
        #plt.imshow(bin_img, cmap='gray')
        #plt.savefig('binary.png')

        delta = 0.05
        limit = 1.5
        angles = np.arange(-limit, limit+delta, delta)
        scores = []
        for angle in angles:
            hist, score = find_score(bin_img, angle)
            scores.append(score)

        best_score = max(scores)
        best_angle = angles[scores.index(best_score)]
        #print('Best angle: {}', best_angle)
        
        # correct skew
        data = inter.rotate(bin_img, best_angle, reshape=False, order=0)
        data = 255*data
        data = 255-data

        return data

        #print(type(data))
        #img = inter.rotate(img, best_angle, reshape=False, order=0)
        #img = im.fromarray((255 * data).astype("uint8")).convert("RGB")
        #savePath = f1
        #tmp = savePath.split("/")
        #print(str(i), " : ", str(best_angle))
        #savePath =  "E:/college/fourth_year/4A/pattern/project/codes/images/finalskew/"+  tmp[len(tmp)-1].split(".")[0] +".png"
        #print(savePath)
        #cv2.imwrite(savePath,data)
        #img.save(savePath)
        #cv2.imshow("corrected", data)
        #cv2.waitKey(0)
