# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 11:08:44 2022

@author: Holly Gibbs
"""


#loading relevant libraries
from skimage import io, img_as_ubyte, img_as_float, measure
from skimage.measure import label, regionprops, regionprops_table
from skimage.morphology import medial_axis, skeletonize
import matplotlib
from matplotlib import pyplot as plt
import numpy as np
import scipy.ndimage as ndi
import cv2
import pandas as pd
from pyefd import elliptic_fourier_descriptors
import skan
import mahotas
import imutils

#importing images
binary_mask = io.imread("insert image path here")
pores_mask = io.imread("insert label map here")
plt.imshow(pores_mask, cmap = "gray")

#clear border (can be activated if needed)
#from skimage.segmentation import clear_border
#pores_mask1 = clear_border(pores_mask)
#plt.imshow(pores_mask1, cmap = "gray")
#cv2.imwrite("D:/Microfractures project/Data/Thin sections/Wayne Ahr dataset/Shortlisted images/tained/SWC-A56B/SWC-A56B_binary.border.removed.tif", pores_mask1)

#connected components analysis
num_labels, pores_label_map = cv2.connectedComponents(pores_mask, connectivity = 8)
plt.imshow(pores_label_map, cmap = "turbo")
#cv2.imwrite("insert image destination here", pores_label_map)

#Region properties
pores_props = pd.DataFrame(regionprops_table(pores_label_map, properties = ['label','area', 'perimeter', 'perimeter_crofton', 'equivalent_diameter','convex_area', 'solidity','major_axis_length', 'minor_axis_length', 'eccentricity','extent', 'feret_diameter_max', 'filled_area']))

pores_props.to_csv("pores_props.csv")


#colormap for predicted classes
predicted_classes = pd.read_csv("insert path of CSV file with predicted labels")
#convert to numpy array
class_array=np.asarray(predicted_classes)
#pull out labels and classes 
labels=class_array[:,2]
classes=class_array[:,4]
#preallocate new classifier map same size as label map
[x,y]=np.shape(pores_label_map)
classifier_map=np.zeros([x,y])
#loop through label map pixel by pixel and reassign intensity value to reflect class
for i in range(x):
    for j in range(y):
        #check pixel for label
        l=pores_label_map[i,j]
        if l>0:
            r=np.where(labels==l)
            if classes[r]=='Crack':
                classifier_map[i,j]=1
            elif classes[r]=='Pore':
                classifier_map[i,j]=2
                
plt.imshow(classifier_map, cmap = "bwr")

cv2.imwrite("insert destination path for color label map", classifier_map)
                

