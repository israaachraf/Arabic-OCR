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
from featureextraction import getSampleFeature
from preprocessing import binarizeImg
from generateoutput import labelToChar
import re


numbers = re.compile(r'(\d+)')
def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts

def predict(words_path):
    model_path = "E:/college/fourth_year/4A/pattern/project/codes/dataset2/model/modelc1000.sav" #path of the trained model #modify
    loaded_model = joblib.load(model_path)
    output_path = "out.txt" #modify
    out = open(output_path, "w", encoding="utf-8")

    words_data_path = os.path.join(words_path,'*') #israa remove all imgs in that folder #modify
    words_files = sorted(glob.glob(word_data_path), key=numericalSort)
    words_cnt = len(char_files)

    for wordnum in range(1, wordnum):
        chars_dir = words_path+ "/" + str(wordnum) + "/chars" 
        chars_data_path = os.path.join(word_dir,'*g')
        char_files = sorted(glob.glob(word_data_path), key=numericalSort)
        for img_path in char_files:
            img = cv2.imread(img_path)
            #prediction
            thresh = binarizeImg(img)
            img_label = loaded_model.predict(getSampleFeature(img, thresh))
            #print(img_label)
            char = labelToChar
            out.write(char)
        out.write(" ")


    out.close()