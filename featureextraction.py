import cv2
from PIL import Image
import numpy as np
import os
import glob
import copy 
import re
import math

numbers = re.compile(r'(\d+)')
def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts

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

def BaseLine(thresh):
    horz_proj = np.sum(thresh, 1)
    ##print("base_line_idx")
    base_line_idx = np.where(horz_proj == np.amax(horz_proj))[0][0]
    return base_line_idx

def inBaseLine(base_line_idx,y,h):
    if(base_line_idx > y and base_line_idx < y+h): return True
    else: return False

#modify #remove repeated code
def dots(thresh): #test
    (h,w) = thresh.shape[:2]
    thresh_tmp = copy.deepcopy(thresh) 
    #img_tmp = copy.deepcopy(img) #test
    connectivity=8 # You need to choose 4 or 8 for connectivity type #question??difference
    labelnum, labelimg, contours, GoCs = cv2.connectedComponentsWithStats(thresh, connectivity, cv2.CV_32S) #num_labels, labels, stats, centroids#labelnum, labelimg, contours, GoCs

    #GoCs:center
    #numberOfConnectedComponent = labelnum-1
    #question labelimg????
    #question#lastargument??
    ##print(" labelnum ", labelnum)
    ##print("contours", contours)
    #cv2.imshow("2", img)
    #cv2.waitKey(0)
    dot_num = 0
    # maxSize = 0
    # maxSizeY = 0
    dotY = h
    upper_dot = -1
    dot_size = 100

    base_line_idx = BaseLine(thresh)
    for label in range(1,labelnum):#first label is for the whole image
        #x,y = GoCs[label]
        #img = cv2.circle(img, (int(x),int(y)), 1, (0,0,255), -1)    #draw center    
        x,y,w,h,size = contours[label]
        # if size > maxSize:
        #     maxSize = size
        #     maxSizeY = y

        if size <= 11 and not(inBaseLine(base_line_idx,y,h)): #maxdotSize till nw = 11
            dot_num += 1
            if(size < dot_size): dot_size = size
            if(y < dotY): dotY = y
            #print("size ", size)
            #modify #check x,y not = 0
            #According to size dot_num #add#modify
            #img_tmp = cv2.rectangle(img_tmp, (x-1,y-1), (x+w,y+h), (255,0,0), 1) #test
            #cv2.imshow("img_tmp", img_tmp)
            #cv2.waitKey(0)
            #Remove dot
            thresh_tmp = cv2.rectangle(thresh_tmp, (x-1,y-1), (x+w,y+h), (0,0,0), -1)
            #cv2.imshow("img_tmp", thresh_tmp)
            #cv2.waitKey(0)

    if(dotY < base_line_idx): upper_dot = 1
    elif(dotY > base_line_idx): upper_dot = 0
    if(dot_num == 0): dot_size = 0
    ##print("upper_dot ", upper_dot)
    #upper_dot: 1:upper, 0: lower, -1: nodots
    return thresh_tmp, dot_num, dot_size, upper_dot

def holes(threshWithoutDots): #test
    #remove dot first#TODO
    (h, w) = threshWithoutDots.shape[:2]

    image,contours,hierarchy = cv2.findContours(threshWithoutDots,cv2.RETR_LIST ,cv2.CHAIN_APPROX_SIMPLE)
    ##print(contours)
    #img = cv2.drawContours(img, contours, -1, (0,255,0), 1) #draw all contours
    #holesNum = len(contours) - 1
    ##print("contoursNum ", len(contours))

    """
    for i in contours:
        if cv2.contourArea(i) > cv2.arcLength(i, True):
            cv2.drawContours(img,[i],0,(255,0,0),1) #img, contour, indx, color, thickness
            cv2.imshow('im',img)
            cv2.waitKey()
    """

    # a = [[[1,6]] ,[[0,-2]], [[-1,6]], [[5,6]]]
    # #print("min",np.amin(a, axis=0)[0][0])  # Minima vertically

    begin = []
    end = []
    trim = []
    flag = False
    hole = True

    maxX =  -1
    miniX = -1

    for cnt in contours:
        # cv2.drawContours(img,[cnt],0,(255,255,0),1)
        # cv2.imshow('contour',img)
        # cv2.waitKey(0)  

        # #print("sara")
        # #print("cnt ", type(cnt)) #Assume cnt = [[[x,y]],.....]
        miniX = np.amin(cnt, axis=0)[0][0]
        maxX = np.amax(cnt, axis=0)[0][0]
        crop = threshWithoutDots[:,miniX+1:maxX] #remove last pixel
        # #print("miniX", miniX)
        # #print("maxX", maxX)
        # #print("crop ", crop)
        transposed = crop.transpose() 
        ##print("transposed ", transposed)
        for j in range(maxX-miniX-1):
            trim.append(np.trim_zeros(transposed[j])) 

        # #print("trim", trim)

        for i in range(len(trim)):
            for  j in range(len(trim[i])):
                if trim[i][j] == 0:
                    flag = True
                    break
                
            if flag == False:
                hole = False
                break
            flag = False

        if hole == True and (maxX-miniX-1) != 0:
            #img = cv2.line(img, (miniX,0), (miniX,h), (255,0,0), 1) #test
            #img = cv2.line(img, (maxX,0), (maxX,h), (255,0,0), 1) #test
            #cv2.imshow('im',img)
            #cv2.waitKey(0)               
            begin.append(miniX-1)
            end.append(maxX+1)
        flag = False
        hole = True
    hole_sz = maxX-miniX
    return len(begin), hole_sz

def aspectRatio(thresh):
    (h, w) = thresh.shape[:2]
    heightArr = np.where(thresh.sum(axis=1)) #axis=1 horizontal #return tuple
    heightArr = list(heightArr[0])
    charHeight = heightArr[len(heightArr)-1] - heightArr[0] + 1

    widthArr = np.where(thresh.sum(axis=0)) #axis=0 vertical
    widthArr = list(widthArr[0])
    charWidth = widthArr[len(widthArr)-1] - widthArr[0] + 1

    aspectRatio = charWidth/charHeight

    #print("height ", charHeight)
    #print("width ", charWidth)

    return aspectRatio
def proj(thresh):
    thresh_tmp = copy.deepcopy(thresh)
    (h, w) = thresh.shape[:2]
    heightArr = np.where(thresh.sum(axis=1)) #axis=1 horizontal #return tuple
    heightArr = list(heightArr[0])
    widthArr = np.where(thresh.sum(axis=0)) #axis=0 vertical
    widthArr = list(widthArr[0])

    #crop the white pixels "char" ONLY
    thresh_tmp = thresh[heightArr[0]:heightArr[len(heightArr)-1]+1, widthArr[0]:widthArr[len(widthArr)-1]+1]
    #cv2.imshow("crop", thresh)
    #cv2.waitKey(0)

    ##########################################################
    #thresh = np.array([[0,0,0,0,0,0,0], [0,0,0,255,0,0,0], [0,255,0,0,0,255,0], [0,0,255,0,0,0,0], [0,0,0,0,0,0,0]])#test
    horzProj = thresh_tmp.sum(axis=1) #axis=1 horizontal
    vertProj = thresh_tmp.sum(axis=0) #axis=0 vertical
    #############################################################################
    #After croping it won't be any zeroes #make_sure#modify
    #get the horz and vertical proj for the white pixels(char) ONLY
    horzProj = np.trim_zeros(horzProj)
    vertProj = np.trim_zeros(vertProj)

    n = 25 - len(horzProj) #thresh #modify
    horzProj = np.pad(horzProj, (n, 0), 'constant') #add zeroes at the begining to make it of const sz #test
    n = 35 - len(vertProj) #thresh #modify
    vertProj = np.pad(vertProj, (n, 0), 'constant')
    #print("horzProj ",horzProj)
    #print("vertProj ", vertProj)
    #print("horzProj ", len(horzProj))
    #print("vertProj ", len(vertProj))
    return horzProj, vertProj


def extractHog(image):
    sizeAfterResize=(32, 32) #Size of images after resize
    image_tmp = cv2.resize(image, sizeAfterResize)

    winSize = (32,32) # Image Size
    cellSize = (4,4) #Size of one cell    
    blockSizeInCells = (2,2)# will be multiplies by No of cells

    blockSize=(blockSizeInCells[1] * cellSize[1], blockSizeInCells[0] * cellSize[0])
    blockStride=(cellSize[1], cellSize[0])
    nbins = 9 #Number of orientation bins
    hog = cv2.HOGDescriptor(winSize, blockSize, blockStride, cellSize, nbins) # 
    h = hog.compute(image_tmp)
    h = h.flatten()
    return h.flatten()


def getSampleFeature(img, thresh):
    threshWithoutDots, dot_num, dot_size, upper_dot = dots(thresh)
    holes_num, hole_sz = holes(threshWithoutDots)
    ratio = aspectRatio(thresh)
    horzProj, vertProj  = proj(thresh)

    sampleFeatures = [dot_num, dot_size, upper_dot, holes_num, hole_sz, ratio]
    #sampleFeatures.extend(horzProj)
    #sampleFeatures.extend(vertProj)
    sampleFeatures.extend(extractHog(img))
    #print(sampleFeatures)
    return sampleFeatures



#test
# txt_dir = "E:/college/fourth_year/4A/pattern/project/codes/images/hole" 
# txt_dir += "/heh"
# txt_data_path = os.path.join(txt_dir,'*')
# txt_files = sorted(glob.glob(txt_data_path), key=numericalSort)

# for txt in txt_files:
#     img = cv2.imread(txt)
#     thresh = binarizeImg(img)
#     threshWithoutDots, dot_num, dot_size, upper_dot = dots(thresh, img)
#     holes_num, hole_sz = holes(threshWithoutDots, img)
#     #print("holes_num ", holes_num)
#     #print("hole_sz ", hole_sz)
