# -*- coding: utf-8 -*-
"""
Created on Sun Apr 14 13:31:58 2019

@author: nithish k
"""


import glob
import os

import imageManipulations
import plotGridAndBound
import XMLParser
import assigngrid
import normalization
import denormalization
import generateTargetVariable
import decodePredictionArray

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import pickle
import nonMaxSupression
from image_operations import get_image_after_rotation

inpfilePattern = "./Train images/images/Arla*"
outputdir = "./Train images/Reshaped/images/"
outputAnnotations = "./Train images/Reshaped/annotations"
xmlFiles = "./Train images/annotations/xmls/Arla*"

AllImageList,AllObjectsList = [],[]
AllImageArray = []
AllImgTargetArray = []

for inpfile,inpXmlFile in zip(sorted(glob.glob(inpfilePattern)),sorted(glob.glob(xmlFiles))):
    
    
    angles = [90, 180, 270]
    outputfileName = os.path.basename(inpfile)
    imgOutputFilePath = outputdir + outputfileName
    imageManipulations.imageResize(inpfile,imgOutputFilePath,342,342)
    
    ### create image X variable
    plt.clf()
    img = plt.imread(imgOutputFilePath)
    AllImageArray.append(img)
    
    
    ##change attributes to reshaped
    origImgDict, origObjList = XMLParser.parseXMLtoDict(inpXmlFile)
    
    dictOfTranslations = {'resizeWidth' : 342, 'resizeHeight' : 342}
    newImageDict,newObjectList  = imageManipulations.ResizeDict(origImgDict,origObjList,dictOfTranslations)
    
    AllImageList.append(newImageDict)
    AllObjectsList.append(newObjectList)
    
#    To rotate images and get there image dict and object list
#    Then appending to the list of image dict and object dict
    for angle in angles:
        newImage, newImageDict, newObjectList = get_image_after_rotation(img, origImgDict, angle, origObjList)
        AllImageList.append(newImageDict)
        AllObjectsList.append(newObjectList)
    ### create img targets
    eachImgTarget = generateTargetVariable.genTargetArray('',newImageDict,newObjectList,19,19, {'milk': 0})
    AllImgTargetArray.append(eachImgTarget)


import pickle
with open(outputAnnotations+'/resizedImageDictsAllFiles.pkl', 'wb') as f:
   pickle.dump(AllImageList, f)

with open(outputAnnotations+'/resizedObjectListsAllFiles.pkl', 'wb') as f:
   pickle.dump(AllObjectsList, f)

with open(outputAnnotations+'/resizedAllImgArray.pkl', 'wb') as f:
   pickle.dump(AllImageArray, f)
   
with open(outputAnnotations+'/resizedAllTargetArray.pkl', 'wb') as f:
   pickle.dump(AllImgTargetArray, f)
#   

   
   
   
   
   

   


                  
