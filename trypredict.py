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


img_path = "E:/college/fourth_year/4A/pattern/project/codes/dataset2/extra/alf/alf.1918.png" #modify #try from extra
img = cv2.imread(img_path)

model_path = "E:/college/fourth_year/4A/pattern/project/codes/dataset2/model/modelc1000.sav" #path of the trained model #modify
loaded_model = joblib.load(model_path)

output_path = "out.txt" #modify

out = open(output_path, "w", encoding="utf-8")

#prediction
thresh = binarizeImg(img)
img_label = loaded_model.predict(getSampleFeature(img, thresh))
print(img_label)
char = labelToChar
out.write(char)

out.close()