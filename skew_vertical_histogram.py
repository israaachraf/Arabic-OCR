#+- 5 angle skew
import sys
import os
import glob
import cv2
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image as im
from scipy.ndimage import interpolation as inter
import re
#input_file = sys.argv[1]


numbers = re.compile(r'(\d+)')
def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts

def find_score(arr, angle):
    data = inter.rotate(arr, angle, reshape=False, order=0)
    hist = np.sum(data, axis=1)
    score = np.sum((hist[1:] - hist[:-1]) ** 2)
    return hist, score

img_dir = "E:/college/fourth_year/4A/pattern/project/codes/images/scanned/" # Enter Directory of all images 
data_path = os.path.join(img_dir,'*g')
files = sorted(glob.glob(data_path), key=numericalSort)
#files = ["E:/college/fourth_year/4A/pattern/project/codes/images/scanned/capr622.png"]
i=0
for f1 in files:
    img = im.open(f1)
    i += 1
    if(i < 1737): continue
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
    #print(type(data))
    #img = inter.rotate(img, best_angle, reshape=False, order=0)
    #img = im.fromarray((255 * data).astype("uint8")).convert("RGB")
    savePath = f1
    tmp = savePath.split("/")
    print(str(i), " : ", str(best_angle))
    savePath =  "E:/college/fourth_year/4A/pattern/project/codes/images/finalskew/"+  tmp[len(tmp)-1].split(".")[0] +".png"
    #print(savePath)
    cv2.imwrite(savePath,data)
    #img.save(savePath)
    #cv2.imshow("corrected", data)
    #cv2.waitKey(0)

    
    """
    # rotate the image to deskew it
    (h, w) = bin_img.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, best_angle, 1.0)
    print(type(img))
    rotated = cv2.warpAffine(img, M, (w, h),
    flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    savePath =  "E:/college/fourth_year/4A/pattern/project/codes/images/test_skew_vert_hist/"+  tmp[len(tmp)-1].split(".")[0] + "angle_" + str(best_angle) +".png"
    cv2.imwrite(savePath,rotated)
    """