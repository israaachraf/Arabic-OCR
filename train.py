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
import re
import glob


numbers = re.compile(r'(\d+)')
def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts

model_path = "E:/college/fourth_year/4A/pattern/project/codes/dataset2/model/modelc10000g0001.sav" #path of the trained model #modify 
t_size = 0.05 #test_Size
r_state = 42 #Random Seed
#imagePaths = list(paths.list_images(path))

folders_dir = 'E:/college/fourth_year/4A/pattern/project/codes/dataset2/output' # Enter Directory of all texts 
folders_data_path = os.path.join(folders_dir,'*')
folders = sorted(glob.glob(folders_data_path), key=numericalSort)
print("folders", len(folders))

# initialize matrices and labels list
features = []
labels = []

# h = [] #test
# w = [] #test
for folder in folders:
    #print("folder ", folder)
    imgs_data_path = os.path.join(folder,'*')
    imagePaths = sorted(glob.glob(imgs_data_path), key=numericalSort)

    for (i, imagePath) in enumerate(imagePaths):
        
        image = cv2.imread(imagePath)
        label = imagePath.split(os.path.sep)[-1].split(".")[0]
        #print("label ", label)
        thresh = binarizeImg(image)
        # x1,h1,w1 = aspectRatio(thresh)
        # h.append(h1)
        # w.append(w1)
        features.append(getSampleFeature(image, thresh))
        labels.append(label)
        # show an update every 1,000 images #test
        if i > 0 and i % 1000 == 0:
            print("[INFO] processed {}/{}".format(i, len(imagePaths)))


# h = np.array(h)#test
# w = np.array(w)#test

# print("max h", np.amax(h)) #test
# print("max w", np.amax(w)) #test

features = np.array(features)
labels = np.array(labels)
# partition the data into training and testing splits
(trainFeatures, testFeatures, trainLabels, testLabels) = train_test_split(
    features, labels, test_size=t_size, random_state=r_state)

print("trainlabels ", labels)
#--------------------------------------------------------------
#NuSVC 
#gamma = 0.025
#change hog parameters
#svc_model = svm.SVC(C=1000, kernel='rbf', degree=3, gamma= 0.001) #no str "scale" for gamma #77.27% #98.09%
#svc_model = svm.SVC(C=1.0, kernel='rbf', degree=3, gamma= 0.001) #55.27%
#svc_model = svm.SVC(C=1000, kernel='rbf', degree=3, gamma= 0.025) #97.67%
svc_model = svm.SVC(C=1000, kernel='rbf', degree=3, gamma= 0.0001) #98.31%
#svc_model = svm.SVC(C=10000, kernel='rbf', degree=3, gamma= 0.0001) #97.88%
#--------------------------------------------------------------
print("[SVM] Training")
# print("type",len(trainFeatures))
# print("type",len(trainLabels))
svc_model.fit(trainFeatures, trainLabels)
print("[SVM] write model")
joblib.dump(svc_model, model_path)

for (i,testFeature) in enumerate(testFeatures):
    img_label = svc_model.predict(testFeature)
    if(img_label !=  testLabels[i]):
        print("out_label ", img_label, "actual ", testLabels[i])

acc = svc_model.score(testFeatures, testLabels)
print("[SVM] Accuracy: {:.2f}%".format(acc * 100))


#svc_model.predict([[2., 2.]])


# lin_model = svm.LinearSVC()
# print("[SVM] Training")
# lin_model.fit(trainFeatures, trainLabels)
# print('get Score')
# acc = lin_model.score(testFeatures, testLabels)
# print("[SVM] Accuracy: {:.2f}%".format(acc * 100))


#--------------------------------------------------------------------------------------------------------------------------------------------#
# Test on chosen images:
# -----------------------
# image1Path = 'test2.jpg'
# image2Path = 'test5.jpg'

# # TODO: read each path of image1Path and image2Path
# # 1) Read the image using cv2.imread
# # 2) getSampleFeature
# img1=cv2.imread(image1Path)
# image1Features=getSampleFeature(img1)
# img2=cv2.imread(image2Path)
# image2Features=getSampleFeature(img2)
# # TODO: Add the features of the 2 images to an array called testImages
# testImages = [image1Features, image2Features]
# print(image2Features.shape, image1Features.shape)

# # Memory Info
# print("[MEM INFO] pixels matrix: {:.2f}MB".format(
#     features.nbytes / (1024 * 1000.0)))

# The following line get the probability for each test image to 
# be in the learnt classes. It isn't applicable to SVM 
# but can be used in the following requirements

#print(lin_model.predict_proba(testImages))
