from sklearn.neighbors import KNeighborsClassifier
from sklearn.cross_validation import train_test_split
from imutils import paths
import numpy as np
from sklearn import svm
from sklearn.externals import joblib
import argparse
import imutils
import cv2
import os
from preprocessing import binarizeImg, skewCorrection
from predict import predict



#take paths from cmd #modify
img_path = "" #modify
test_cases_num = ""

for i in range(1,test_cases_num+1):
    img_path_tmp = img_path + "test_" + str(i) + ".png"
    img = cv2.imread(img_path)
    deskewedimg = skewCorrection(img)
    #----code Israa:  #modify
    predict(words_path) #arguments #modify