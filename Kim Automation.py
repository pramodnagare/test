#Author: Pramod Nagare#
#Date: 02/11/2019#
#This script is for automating the following processes:
#PDF package to image conversion
#Creating MISMO folders
#Populating Dataset for Deep Vision Classified for Document classification

import pandas as pd
import numpy as np
import os
import time
import shutil
import glob
import csv


package_folder = r"C:\Users\pnagare\Documents\TA" #Considering all the pdf packages are at same folder
image_folder = r"C:\Users\pnagare\Documents\TA" #The main folder where each pdf package will split into images with folder
class_folder =r"C:\Users\pnagare\Documents\TA\MISMO" #The MISMO Classification folder


#Get the pdf packages from the package_folder
packages = glob.glob(package_folder+"/*.pdf")


#Do you want to create the MISMO Folders?
mismo = False
mismo_class = 600

if mismo:
    start = time.time()
    for i in range(0,mismo_class):
        os.mkdir(class_folder+"/"+str('%03d' %i))
    end = time.time()
    print("Time for MISMO folders creation: " + str(end-start) + " secs")


#Convert each pdf package to images
start = time.time()
with open(r'pdf2png.sh','w') as f:
    f.write('#!/bin/bash')
    f.write('\n')
    for i in range(0,len(packages)):
        p = packages[i].split("\\")[-1]
        os.mkdir(image_folder+"/"+p.split(".")[0].replace(" ","_"))
        f.write("gm convert -density 300 -quality 100 -channel Gray +adjoin \""+ packages[i] + "\" \""+ image_folder+"/"+p.split(".")[0].replace(" ","_")+"/%04d.png\"")
        f.write('\n')
os.system(r'pdf2png.sh')
end = time.time()
print("Time for PDF to PNG conversion for " + str(len(packages)) + " packages: " + str(end-start) + " secs")


start = time.time()
for i in range(0,len(packages)):
    p = packages[i].split("\\")[-1].split('.pdf')[0].replace(' ','_')
    X = [['Sr.No','Image Name','Class']]
    images = glob.glob(image_folder+"/"+p+"/*.png")
    for j in range(0,len(images)):
        img = str(images[j].split('\\')[-1])
        X.append([str(j),str(img),''])
    df = pd.DataFrame(X, columns=X.pop(0))
    df.to_csv(image_folder+"/"+p+"/"+p+".csv", index=False)
end = time.time()
print("Time for creating excels for each package: " + str(end-start) + " secs")


#Creating python script for post class file transfer
start = time.time()
for i in range(0,len(packages)):
    p = packages[i].split("\\")[-1].split('.pdf')[0].replace(' ','_')
    t = p
    p = image_folder+"/"+p
    with open(p+"/"+t+".py",'w') as f:
		f.write('#Author: Pramod Nagare# \n')
        f.write('import pandas as pd \n')
        f.write('import csv \n')
        f.write('import shutil \n')
        f.write('\n')
        f.write('class_folder =r'+"\""+class_folder+"\""+" #The MISMO Classification folder \n \n")
        f.write('p = r\"'+p+"/\"\n")
        f.write('tf = pd.read_csv(r\'' + p+"/"+t+".csv\')\n")
        f.write('for i in range(tf.shape[0]):\n')
        f.write("    if str(tf['Class'][i])!='nan':\n")
        f.write("        shutil.copy(p + tf['Image Name'][i],class_folder+'/'+str('%03d' %tf['Class'][i])+'/'+str("+str(i)+")+'-'+tf['Image Name'][i])")
end = time.time()
print("Time for execution for creating python script: " + str(end-start) + " secs")

