import cv2
from PIL import Image
import numpy as np
import os
import glob
import re

#Add othrlabels #modify
Dict = {'alf':'ا',
        'beh':'ب',
        "teh":'ت',
        "theh":"ث",
        "gem":"ج",
        "hah":"ح",
        "khah":"خ",
        "dal":"د",
        "zal":"ذ",
        "reh":"ر",
        "zen":"ز" ,
        "sen":"س",
        "shen":"ش",
        "sad":"ص",
        "dad":"ض",
        "tah":"ط",
        "zah":"ظ",
        "aen":"ع",
        "ghen":"غ",
        "feh":"ف",
        "Qaf":"ق",
        "kaf":"ك",
        "lam":"ل",
        "mem":"م",
        "non":"ن",
        "heh":"ه",
        "waw":"و",
        "yeh":"ي",
        "lamalf":"لا",
        "tehmarbota":"ة"}



def labelToChar(label):
    return Dict[label]
