# f = open('./images/text/capr1.txt', 'r').read()
# splitf = f.split('\n')

# for eachline in splitf:
#      x = eachline.encode('utf-8')
#      print(x.decode('unicode-escape'))

import cv2
from PIL import Image
import numpy as np
import os
import glob
import re

#check correct reading, lam2lf #modify
#other combination, middle,...


numbers = re.compile(r'(\d+)')
def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts


Dict = {'ا': 'alf',
        'ب': 'beh',
        'ت': "teh",
        "ث": "theh",
        "ج": "gem",
        "ح": "hah",
        "خ": "khah",
        "د": "dal",
        "ذ": "zal",
        "ر": "reh",
        "ز": "zen",
        "س": "sen",
        "ش": "shen",
        "ص": "sad",
        "ض": "dad",
        "ط": "tah",
        "ظ": "zah",
        "ع": "aen",
        "غ": "ghen",
        "ف": "feh",
        "ق": "Qaf",
        "ك": "kaf",
        "ل": "lam",
        "م": "mem",
        "ن": "non",
        "ه": "heh",
        "و": "waw",
        "ي": "yeh",
        "لا": "lamalf",
        "ة": "tehmarbota"} 

##print("dic", Dict['ك'])

txt_dir = "E:/college/fourth_year/4A/pattern/project/codes/dataset2/text" # Enter Directory of all texts 
txt_data_path = os.path.join(txt_dir,'*')
txt_files = sorted(glob.glob(txt_data_path), key=numericalSort)
#print("txt_files", txt_data_path)

main_imgs_dir = "E:/college/fourth_year/4A/pattern/project/codes/dataset2/segmentation" # Enter Directory of all imgs
main_char_path = "E:/college/fourth_year/4A/pattern/project/codes/dataset2/output"
# img_data_path = os.path.join(img_dir,'*g')
# img_files = glob.glob(img_data_path)

txtnum = 1
for txt in txt_files:
  print("txtnum ", txtnum)
  #if(txtnum > 1): break
  #print("read text")
  f = open(txt, encoding="utf-8")

  #open folder of word img, get char_cnt
  img_dir = main_imgs_dir + "/" + str(txtnum) + "/words"
  char_cnt = 0
  
  myfile = open("file.txt", "w", encoding="utf-8") #test
  lines = f.readlines()
  for line in lines:
      #myfile.write(line) #test
      wordnum = 1
      for word in line.split():
        #print(wordnum)
        word_dir = img_dir+ "/" + str(wordnum) + "/chars" #remove charsfolder modify
        ##print("word_dir ",word_dir)
        word_data_path = os.path.join(word_dir,'*g')
        char_files = sorted(glob.glob(word_data_path), key=numericalSort)
        char_cnt = len(char_files)

        char_num = 0
        if len(word) == char_cnt:
          #karen char char
          #open folder 2smo Dict[word[0]] w 7ot l img b l name Dict[word[0]].3dd_l_img_f_folder_+1.png
          c_index = 1
          for c in word:
            #char path, img_cnt #modify
            char_path = main_char_path + "/" + Dict[c] 
            if not os.path.exists(char_path):
               os.makedirs(char_path)

            c_data_path = os.path.join(char_path,'*g')
            c_files = sorted(glob.glob(c_data_path), key=numericalSort)
            img_cnt = len(c_files)

            if(c_index == len(word) and (c == "س" or c == "ش" or c == "ج" or c == "ح" or c == "خ" or c == "ص" or c == "ض" or c == "ع" or c == "غ" or c == "ه" or c == "ة")):
              if(len(word) > 1 and ((c == "ه" and word[len(word)-1] == 'ا') or (c == "ة" and word[len(word)-1] == 'ا'))): char_path = char_path + "/" + Dict[c] + "end1." + str(img_cnt+1)+ ".png"
              else: char_path = char_path + "/" + Dict[c] + "end." + str(img_cnt+1)+ ".png"
            else: char_path = char_path + "/" + Dict[c] + "." + str(img_cnt+1)+ ".png" 

            #print("len(word) == char_cnt ")
            img_c = cv2.imread(char_files[char_num])
            cv2.imwrite(char_path,img_c)
            char_num += 1
            c_index += 1
        #Case lam2lf
        elif len(word) > char_cnt:
          #karen char char
          #open folder 2smo Dict[word[0]] w 7ot l img b l name Dict[word[0]].3dd_l_img_f_folder_+1.png
          c_index = 0
          for c in word:
            if(c == "ا" and (c_index+2 < len(word))): 
              word[c_index + 1] == "ل"
              word[c_index + 2] == "ا"
              c_index += 3
              #char path, img_cnt #modify
              char_path = main_char_path + "/" + Dict[c] 
              if not os.path.exists(char_path):
                  os.makedirs(char_path)

              c_data_path = os.path.join(char_path,'*g')
              c_files = sorted(glob.glob(c_data_path), key=numericalSort)
              img_cnt = len(c_files)
              char_path = char_path + "/" + Dict[c] + "." + str(img_cnt+1)+ ".png"
              img_c = cv2.imread(char_files[char_num])
              cv2.imwrite(char_path,img_c)
              char_num += 1

              #char path, img_cnt #modify
              char_path = main_char_path + "/" + Dict["لا"] 
              if not os.path.exists(char_path):
                  os.makedirs(char_path)

              c_data_path = os.path.join(char_path,'*g')
              c_files = sorted(glob.glob(c_data_path), key=numericalSort)
              img_cnt = len(c_files)
              char_path = char_path + "/" + Dict["لا"] + "." + str(img_cnt+1)+ ".png"
              img_c = cv2.imread(char_files[char_num])
              cv2.imwrite(char_path,img_c)
              char_num += 1
              continue

            elif(c_index == 0 and (c_index+1 < len(word))):
              word[c_index] == "ل"
              word[c_index + 1] == "ا"
              c_index += 2

              #char path, img_cnt #modify
              char_path = main_char_path + "/" + Dict["لا"] 
              if not os.path.exists(char_path):
                  os.makedirs(char_path)

              c_data_path = os.path.join(char_path,'*g')
              c_files = sorted(glob.glob(c_data_path), key=numericalSort)
              img_cnt = len(c_files)
              char_path = char_path + "/" + Dict["لا"] + "." + str(img_cnt+1)+ ".png"
              img_c = cv2.imread(char_files[char_num])
              cv2.imwrite(char_path,img_c)
              char_num += 1
              continue

            #char path, img_cnt #modify
            char_path = main_char_path + "/" + Dict[c] 
            if not os.path.exists(char_path):
                os.makedirs(char_path)

            c_data_path = os.path.join(char_path,'*g')
            c_files = sorted(glob.glob(c_data_path), key=numericalSort)
            img_cnt = len(c_files)

            if(c_index == len(word)-1 and (c == "س" or c == "ش" or c == "ج" or c == "ح" or c == "خ" or c == "ص" or c == "ض" or c == "ع" or c == "غ" or c == "ه" or c == "ة")):
              if(len(word) > 1 and ((c == "ه" and word[len(word)-1] == 'ا') or (c == "ة" and word[len(word)-1] == 'ا'))): char_path = char_path + "/" + Dict[c] + "end1." + str(img_cnt+1)+ ".png"
              else: char_path = char_path + "/" + Dict[c] + "end." + str(img_cnt+1)+ ".png"
            else: char_path = char_path + "/" + Dict[c] + "." + str(img_cnt+1)+ ".png" 

            #print("len(word) == char_cnt ")
            img_c = cv2.imread(char_files[char_num])
            cv2.imwrite(char_path,img_c)
            char_num += 1
            c_index += 1

        # elif len(word) < char_cnt:

        #   sen_cnt = 0
        #   reh_cnt = 0
        #   teh_cnt = 0
        #   sad_cnt = 0

        #   for c in word:
        #     if(c == "س" or c == "ش"):
        #       sen_cnt += 1
        #     # elif(c == "ر" or c == "ز"):
        #     #   reh_cnt += 1
        #     elif (c == "ص" or c == "ض"):
        #         sad_cnt += 1
        #   if(word[len(word)-1] == "ت" or word[len(word)-1] == "ث"or word[len(word)-1] == "ب"):
        #     teh_cnt += 1
   

        #   if(len(word) + 2*sen_cnt + sad_cnt == char_cnt):
        #     c_index = 1
        #     for c in word:
        #       if(c ==  "س" or c == "ش"):
        #         #char path, img_cnt #modify
        #         for i in range (1,4):
        #           char_path = main_char_path + "/" + Dict[c] + str(i) 
        #           if not os.path.exists(char_path):
        #              os.makedirs(char_path)

        #           c_data_path = os.path.join(char_path,'*g')
        #           c_files = sorted(glob.glob(c_data_path), key=numericalSort)
        #           img_cnt = len(c_files)
        #           if(c_index == len(word)): char_path = char_path + "/" + Dict[c] + str(i) + "end." + str(img_cnt+1)+ ".png"
        #           else: char_path = char_path + "/" + Dict[c] + str(i) + "." + str(img_cnt+1)+ ".png"
        #           #print("char_path ", char_path)
        #           #print("sen,  len(word) + 2*sen_cnt + sad_cnt == char_cnt")
        #           img_c = cv2.imread(char_files[char_num])
        #           cv2.imwrite(char_path, img_c)
        #           char_num += 1


        #       # elif(c == "ر" or c == "ز"):
        #       #   #char path, img_cnt #modify
        #       #   for i in range (1,3):
        #       #     char_path = main_char_path + "/" + Dict[c]+ str(i) 
        #       #     if not os.path.exists(char_path):
        #       #       os.makedirs(char_path)

        #       #     c_data_path = os.path.join(char_path,'*g')
        #       #     c_files = glob.glob(c_data_path)
        #       #     img_cnt = len(c_files)

        #       #     char_path = char_path + "/" + Dict[c] + str(i) + "." + str(img_cnt+1)+ ".png"
        #       #     #print("char_path ", char_path)
        #       #     img_c = cv2.imread(char_files[char_num])
        #       #     cv2.imwrite(char_path,img_c)
        #       #     char_num += 1

        #       # elif((c == "ت" and word[len(word)-1] == "ت") or (c == "ث" and word[len(word)-1] ="ث") or (c == "ب" and word[len(word)-1] == "ب")):
        #       #   #char path, img_cnt #modify
        #       #   for i in range (1,3):
        #       #     char_path = main_char_path +"/" + Dict[c]+ str(i)
        #       #     if not os.path.exists(char_path):
        #       #       os.makedirs(char_path)
                  
        #       #     c_data_path = os.path.join(char_path,'*g')
        #       #     c_files = glob.glob(c_data_path)
        #       #     img_cnt = len(c_files)

        #       #     char_path = char_path + "/" + Dict[c] +  str(i) + "." + str(img_cnt+1)+ ".png"
        #       #     #print("char_path ", char_path)
        #       #     img_c = cv2.imread(char_files[char_num])
        #       #     cv2.imwrite(char_path, img_c)
        #       #     char_num += 1
        #       elif (c == "ص" or c == "ض"):
        #           #char path, img_cnt #modify
        #           for i in range (1,3):
        #             char_path = main_char_path +"/" + Dict[c]+ str(i)
        #             if not os.path.exists(char_path):
        #               os.makedirs(char_path)
                    
        #             c_data_path = os.path.join(char_path,'*g')
        #             c_files = sorted(glob.glob(c_data_path), key=numericalSort)
        #             img_cnt = len(c_files)
        #             if(c_index == len(word)): char_path = char_path + "/" + Dict[c] +  str(i) + "end." + str(img_cnt+1)+ ".png"
        #             else: char_path = char_path + "/" + Dict[c] +  str(i) + "." + str(img_cnt+1)+ ".png"
        #             #print("char_path ", char_path)
        #             #print("len(word) + 2*sen_cnt + sad_cnt == char_cnt, sad")
        #             img_c = cv2.imread(char_files[char_num])
        #             cv2.imwrite(char_path, img_c)
        #             char_num += 1
        #       else:
        #           char_path = main_char_path +"/" + Dict[c]
        #           if not os.path.exists(char_path):
        #             os.makedirs(char_path)
                  
        #           c_data_path = os.path.join(char_path,'*g')
        #           c_files = sorted(glob.glob(c_data_path), key=numericalSort)
        #           img_cnt = len(c_files)
        #           if(c_index == len(word) and  (c == "ج" or c == "ح" or c == "خ"  or c == "ع" or c == "غ")): char_path = char_path + "/" + Dict[c] +  "end." + str(img_cnt+1)+ ".png"
        #           else: char_path = char_path + "/" + Dict[c] +  "." + str(img_cnt+1)+ ".png"
        #           #print("char_path ", char_path)
        #           #print("len(word) + 2*sen_cnt + sad_cnt == char_cnt, else")
        #           img_c = cv2.imread(char_files[char_num])
        #           cv2.imwrite(char_path, img_c)
        #           char_num += 1
        #       c_index += 1

        #   elif(len(word) + 2*sen_cnt + sad_cnt + reh_cnt == char_cnt):
        #     c_index = 1
        #     for c in word:
        #       if(c ==  "س" or c == "ش"):
        #         #char path, img_cnt #modify
        #         for i in range (1,4):
        #           char_path = main_char_path + "/" + Dict[c] + str(i) 
        #           if not os.path.exists(char_path):
        #              os.makedirs(char_path)

        #           c_data_path = os.path.join(char_path,'*g')
        #           c_files = sorted(glob.glob(c_data_path), key=numericalSort)
        #           img_cnt = len(c_files)

        #           if(c_index == len(word)):  char_path = char_path + "/" + Dict[c] + str(i) + "end." + str(img_cnt+1)+ ".png"
        #           else: char_path = char_path + "/" + Dict[c] + str(i) + "." + str(img_cnt+1)+ ".png"
        #           #print("char_path ", char_path)
        #           #print("len(word) + 2*sen_cnt + sad_cnt + reh_cnt == char_cnt, sen")
        #           img_c = cv2.imread(char_files[char_num])
        #           cv2.imwrite(char_path, img_c)
        #           char_num += 1

        #       # elif(c == "ر" or c == "ز"):
        #       #   #char path, img_cnt #modify
        #       #   for i in range (1,3):
        #       #     char_path = main_char_path + "/" + Dict[c]+ str(i) 
        #       #     if not os.path.exists(char_path):
        #       #       os.makedirs(char_path)

        #       #     c_data_path = os.path.join(char_path,'*g')
        #       #     c_files = sorted(glob.glob(c_data_path), key=numericalSort)
        #       #     img_cnt = len(c_files)

                  
        #       #     char_path = char_path + "/" + Dict[c] + str(i) + "." + str(img_cnt+1)+ ".png"
        #       #     #print("char_path ", char_path)
        #       #     #print("len(word) + 2*sen_cnt + sad_cnt + reh_cnt == char_cnt, zen")
        #       #     img_c = cv2.imread(char_files[char_num])
        #       #     cv2.imwrite(char_path,img_c)
        #       #     char_num += 1

        #       # elif((c == "ت" and word[len(word)-1] == "ت") or (c == "ث" and word[len(word)-1] ="ث") or (c == "ب" and word[len(word)-1] == "ب")):
        #       #   #char path, img_cnt #modify
        #       #   for i in range (1,3):
        #       #     char_path = main_char_path +"/" + Dict[c]+ str(i)
        #       #     if not os.path.exists(char_path):
        #       #       os.makedirs(char_path)
                  
        #       #     c_data_path = os.path.join(char_path,'*g')
        #       #     c_files = glob.glob(c_data_path)
        #       #     img_cnt = len(c_files)

        #       #     char_path = char_path + "/" + Dict[c] +  str(i) + "." + str(img_cnt+1)+ ".png"
        #       #     #print("char_path ", char_path)
        #       #     img_c = cv2.imread(char_files[char_num])
        #       #     cv2.imwrite(char_path, img_c)
        #       #     char_num += 1
        #       elif (c == "ص" or c == "ض"):
        #           #char path, img_cnt #modify
        #           for i in range (1,3):
        #             char_path = main_char_path +"/" + Dict[c]+ str(i)
        #             if not os.path.exists(char_path):
        #               os.makedirs(char_path)
                    
        #             c_data_path = os.path.join(char_path,'*g')
        #             c_files = sorted(glob.glob(c_data_path), key=numericalSort)
        #             img_cnt = len(c_files)

        #             if(c_index == len(word)): char_path = char_path + "/" + Dict[c] +  str(i) + "end." + str(img_cnt+1)+ ".png"
        #             else: char_path = char_path + "/" + Dict[c] +  str(i) + "." + str(img_cnt+1)+ ".png"
        #             #print("char_path ", char_path)
        #             #print("len(word) + 2*sen_cnt + sad_cnt + reh_cnt == char_cnt, sad")
        #             img_c = cv2.imread(char_files[char_num])
        #             cv2.imwrite(char_path, img_c)
        #             char_num += 1
        #       else:
        #           char_path = main_char_path +"/" + Dict[c]
        #           if not os.path.exists(char_path):
        #             os.makedirs(char_path)
                  
        #           c_data_path = os.path.join(char_path,'*g')
        #           c_files = sorted(glob.glob(c_data_path), key=numericalSort)
        #           img_cnt = len(c_files)
        #           if(c_index == len(word) and  (c == "ج" or c == "ح" or c == "خ"  or c == "ع" or c == "غ")): char_path = char_path + "/" + Dict[c] +  "end." + str(img_cnt+1)+ ".png"
        #           else: char_path = char_path + "/" + Dict[c] +  "." + str(img_cnt+1)+ ".png"
        #           #print("char_path ", char_path)
        #           #print("len(word) + 2*sen_cnt + sad_cnt + reh_cnt == char_cnt, else")
        #           img_c = cv2.imread(char_files[char_num])
        #           cv2.imwrite(char_path, img_c)
        #           char_num += 1
        #       c_index += 1    

        #   elif(len(word) + 2*sen_cnt + sad_cnt + teh_cnt == char_cnt):
        #     c_index = 1
        #     for c in word:
        #       if(c ==  "س" or c == "ش"):
        #         #char path, img_cnt #modify
        #         for i in range (1,4):
        #           char_path = main_char_path + "/" + Dict[c] + str(i) 
        #           if not os.path.exists(char_path):
        #              os.makedirs(char_path)

        #           c_data_path = os.path.join(char_path,'*g')
        #           c_files = sorted(glob.glob(c_data_path), key=numericalSort)
        #           img_cnt = len(c_files)
        #           if(c_index == len(word)): char_path = char_path + "/" + Dict[c] + str(i) + "end." + str(img_cnt+1)+ ".png"
        #           else: char_path = char_path + "/" + Dict[c] + str(i) + "." + str(img_cnt+1)+ ".png"
        #           #print("char_path ", char_path)
        #           #print("len(word) + 2*sen_cnt + sad_cnt + teh_cnt == char_cnt sen")
        #           img_c = cv2.imread(char_files[char_num])
        #           cv2.imwrite(char_path, img_c)
        #           char_num += 1
        #       elif (c == "ص" or c == "ض"):
        #           #char path, img_cnt #modify
        #           for i in range (1,3):
        #             char_path = main_char_path +"/" + Dict[c]+ str(i)
        #             if not os.path.exists(char_path):
        #               os.makedirs(char_path)
                    
        #             c_data_path = os.path.join(char_path,'*g')
        #             c_files = sorted(glob.glob(c_data_path), key=numericalSort)
        #             img_cnt = len(c_files)

        #             if(c_index == len(word)): char_path = char_path + "/" + Dict[c] +  str(i) + "end." + str(img_cnt+1)+ ".png"
        #             else: char_path = char_path + "/" + Dict[c] +  str(i) + "." + str(img_cnt+1)+ ".png"
        #             #print("char_path ", char_path)
        #             #print("len(word) + 2*sen_cnt + sad_cnt + teh_cnt == char_cnt sad")
        #             img_c = cv2.imread(char_files[char_num])
        #             cv2.imwrite(char_path, img_c)
        #             char_num += 1
        #       elif(not((c == "ت" or c == "ب" or c == "ث")and c_index == len(word))):
        #           char_path = main_char_path +"/" + Dict[c]
        #           if not os.path.exists(char_path):
        #             os.makedirs(char_path)
                  
        #           c_data_path = os.path.join(char_path,'*g')
        #           c_files = sorted(glob.glob(c_data_path), key=numericalSort)
        #           img_cnt = len(c_files)
        #           if(c_index == len(word) and  (c == "ج" or c == "ح" or c == "خ"  or c == "ع" or c == "غ")): char_path = char_path + "/" + Dict[c] +  "end." + str(img_cnt+1)+ ".png"
        #           else: char_path = char_path + "/" + Dict[c] +  "." + str(img_cnt+1)+ ".png"
        #           #print("char_path ", char_path)
        #           #print("len(word) + 2*sen_cnt + sad_cnt + teh_cnt == char_cnt else")
        #           img_c = cv2.imread(char_files[char_num])
        #           cv2.imwrite(char_path, img_c)
        #           char_num += 1
        #       c_index += 1
                  
        #     if((c == "ت" and word[len(word)-1] == "ت") or (c == "ث" and word[len(word)-1] == "ث") or (c == "ب" and word[len(word)-1] == "ب")):
        #         #char path, img_cnt #modify
        #         for i in range (1,3):
        #           char_path = main_char_path +"/" + Dict[c]+ str(i)
        #           if not os.path.exists(char_path):
        #             os.makedirs(char_path)
                  
        #           c_data_path = os.path.join(char_path,'*g')
        #           c_files = sorted(glob.glob(c_data_path), key=numericalSort)
        #           img_cnt = len(c_files)

        #           char_path = char_path + "/" + Dict[c] +  str(i) + "." + str(img_cnt+1)+ ".png"
        #           #print("char_path ", char_path)
        #           #print("char_num ", char_num)
        #           #print("len(word) + 2*sen_cnt + sad_cnt + teh_cnt == char_cnt teh")
        #           img_c = cv2.imread(char_files[char_num])
        #           cv2.imwrite(char_path, img_c)
        #           char_num += 1      

        #   elif(len(word) + 2*sen_cnt + sad_cnt + teh_cnt + reh_cnt == char_cnt):
        #     c_index = 1
        #     for c in word:
        #       if(c ==  "س" or c == "ش"):
        #         #char path, img_cnt #modify
        #         for i in range (1,4):
        #           char_path = main_char_path + "/" + Dict[c] + str(i) 
        #           if not os.path.exists(char_path):
        #              os.makedirs(char_path)

        #           c_data_path = os.path.join(char_path,'*g')
        #           c_files = sorted(glob.glob(c_data_path), key=numericalSort)
        #           img_cnt = len(c_files)

        #           if(c_index == len(word)):  char_path = char_path + "/" + Dict[c] + str(i) + "end." + str(img_cnt+1)+ ".png"
        #           else: char_path = char_path + "/" + Dict[c] + str(i) + "." + str(img_cnt+1)+ ".png"

        #           #print("char_path ", char_path)
        #           #print("(len(word) + 2*sen_cnt + sad_cnt + teh_cnt + reh_cnt == char_cnt sen")
        #           img_c = cv2.imread(char_files[char_num])
        #           cv2.imwrite(char_path, img_c)
        #           char_num += 1

        #       # elif(c == "ر" or c == "ز"):
        #       #   #char path, img_cnt #modify
        #       #   for i in range (1,3):
        #       #     char_path = main_char_path + "/" + Dict[c]+ str(i) 
        #       #     if not os.path.exists(char_path):
        #       #       os.makedirs(char_path)

        #       #     c_data_path = os.path.join(char_path,'*g')
        #       #     c_files = sorted(glob.glob(c_data_path), key=numericalSort)
        #       #     img_cnt = len(c_files)

        #       #     char_path = char_path + "/" + Dict[c] + str(i) + "." + str(img_cnt+1)+ ".png"
        #       #     #print("char_path ", char_path)
        #       #     #print("(len(word) + 2*sen_cnt + sad_cnt + teh_cnt + reh_cnt == char_cnt reh")
        #       #     img_c = cv2.imread(char_files[char_num])
        #       #     cv2.imwrite(char_path,img_c)
        #       #     char_num += 1
        #       elif (c == "ص" or c == "ض"):
        #           #char path, img_cnt #modify
        #           for i in range (1,3):
        #             char_path = main_char_path +"/" + Dict[c]+ str(i)
        #             if not os.path.exists(char_path):
        #               os.makedirs(char_path)
                    
        #             c_data_path = os.path.join(char_path,'*g')
        #             c_files = sorted(glob.glob(c_data_path), key=numericalSort)
        #             img_cnt = len(c_files)
        #             if(c_index == len(word)): char_path = char_path + "/" + Dict[c] +  str(i) + "end." + str(img_cnt+1)+ ".png"
        #             else: char_path = char_path + "/" + Dict[c] +  str(i) + "." + str(img_cnt+1)+ ".png"
        #             #print("char_path ", char_path)
        #             #print("(len(word) + 2*sen_cnt + sad_cnt + teh_cnt + reh_cnt == char_cnt sad")
        #             img_c = cv2.imread(char_files[char_num])
        #             cv2.imwrite(char_path, img_c)
        #             char_num += 1
        #       elif(not((c == "ت" or c == "ب" or c == "ث") and c_index == len(word))):
        #           char_path = main_char_path +"/" + Dict[c]
        #           if not os.path.exists(char_path):
        #             os.makedirs(char_path)
                  
        #           c_data_path = os.path.join(char_path,'*g')
        #           c_files = sorted(glob.glob(c_data_path), key=numericalSort)
        #           img_cnt = len(c_files)
        #           if(c_index == len(word) and  (c == "ج" or c == "ح" or c == "خ"  or c == "ع" or c == "غ")): char_path = char_path + "/" + Dict[c] +  "end." + str(img_cnt+1)+ ".png"
        #           else: char_path = char_path + "/" + Dict[c] +  "." + str(img_cnt+1)+ ".png"
        #           #print("char_path ", char_path)
        #           #print("(len(word) + 2*sen_cnt + sad_cnt + teh_cnt + reh_cnt == char_cnt else")
        #           img_c = cv2.imread(char_files[char_num])
        #           cv2.imwrite(char_path, img_c)
        #           char_num += 1
        #       c_index += 1
        #     if((c == "ت" and word[len(word)-1] == "ت") or (c == "ث" and word[len(word)-1] == "ث") or (c == "ب" and word[len(word)-1] == "ب")):
        #       #char path, img_cnt #modify
        #       for i in range (1,3):
        #         char_path = main_char_path +"/" + Dict[c]+ str(i)
        #         if not os.path.exists(char_path):
        #           os.makedirs(char_path)
                
        #         c_data_path = os.path.join(char_path,'*g')
        #         c_files = sorted(glob.glob(c_data_path), key=numericalSort)
        #         img_cnt = len(c_files)

        #         char_path = char_path + "/" + Dict[c] +  str(i) + "." + str(img_cnt+1)+ ".png"
        #         #print("char_path ", char_path)
        #         #print("(len(word) + 2*sen_cnt + sad_cnt + teh_cnt + reh_cnt == char_cnt teh")
        #         img_c = cv2.imread(char_files[char_num])
        #         cv2.imwrite(char_path, img_c)
        #         char_num += 1
        wordnum += 1


  txtnum += 1

  
# while True:
#     c = f.read(1)
#     if not c:
#       print("End of file")
#       break

#myfile = open("file.txt", "w", encoding="utf-8") 

# imgPath = "E:/college/fourth_year/4A/pattern/project/codes/images/chars/test/6.png"
# img = cv2.imread(imgPath)


        
    #print("Read a character:", c)

    #myfile.write(c)
    #path = "E:/college/fourth_year/4A/pattern/project/codes/"+ c +".png"
    # if c == "ا":
    # elif c == "ب":
    # elif c == "ب":
    # elif c == "ب":
    # elif c == "ب"
    # elif c == "ب":
    # elif c == "ب":
    # elif c == "ب":
    # elif c == "ب":
    # elif c == "ب":
    # elif c == "ب":
    # elif c == "ب":
    # elif c == "ب":
    # elif c == "ب":
    # elif c == "ب":
    # elif c == "ب":
    # elif c == "ب":
    # elif c == "ب":
    # elif c == "ب":
    # elif c == "ب":
    # elif c == "ب":
    # elif c == "ب":
    # elif c == "ب":
    # elif c == "ب":
    # elif c == "ب":
    # elif c == "ب":
    # elif c == "ب":
    # elif c == "ب":
    # elif c == "ب":
    #cv2.imwrite(path, img)
    #myfile.write(c)
    # with open("file.txt", "w", encoding="utf-8") as myfile:
    #     myfile.write(c)
    # break


# print(f.read())
# f2 = open('log.txt', 'w',encoding='windows-1256')
# f2.write("اب")

#worked
# s = "ذهب الطالب الى المدرسة"
# with open("file.txt", "w", encoding="utf-8") as myfile:
#     myfile.write(f.read())


# import arabic_reshaper

# text_to_be_reshaped =  'اللغة العربية رائعة'

# reshaped_text = arabic_reshaper.reshape(text_to_be_reshaped)

# rev_text = reshaped_text[::-1]  # slice backwards 

# print(rev_text)

