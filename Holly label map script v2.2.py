# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 11:08:44 2022

@author: holly
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
binary_mask = io.imread("Shortlisted images/Stained/ST-35-9811.4/ST-35-9811.4_HSB+LAB.binary.tif")
pores_mask = io.imread("Shortlisted images/Unstained/SWC A34/SWC A34_label.map.tif")
plt.imshow(pores_mask, cmap = "gray")

#clear border
#from skimage.segmentation import clear_border
#pores_mask1 = clear_border(pores_mask)
#plt.imshow(pores_mask1, cmap = "gray")
#cv2.imwrite("D:/Microfractures project/Data/Thin sections/Wayne Ahr dataset/Shortlisted images/tained/SWC-A56B/SWC-A56B_binary.border.removed.tif", pores_mask1)

#connected components analysis
num_labels, pores_label_map = cv2.connectedComponents(pores_mask, connectivity = 8)
plt.imshow(pores_label_map, cmap = "turbo")
#cv2.imwrite("D:/Microfractures project/Data/Thin sections/Wayne Ahr dataset/Shortlisted images/Unstained/SWC-A56B/SWC-A56B_label.map.tif", pores_label_map)

#Region properties
pores_props = pd.DataFrame(regionprops_table(pores_label_map, properties = ['label','area', 'perimeter', 'perimeter_crofton', 'equivalent_diameter','convex_area', 'solidity','major_axis_length', 'minor_axis_length', 'eccentricity','extent', 'feret_diameter_max', 'filled_area']))

pores_props.to_csv("pores_props.csv")


#colormap for predicted classes
predicted_classes = pd.read_csv("D:/Microfractures project/Code/Code working directory/MLR_predictions_allobjects_DK-75-9763.1.csv")
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

cv2.imwrite("D:/Microfractures project/Code/Code working directory/DK-75-9763.1_predicted_map.tif", classifier_map)
                
# #######Complex Shape descriptors

# #get contours
contours = cv2.findContours(pores_mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
cnts=imutils.grab_contours(contours)
blank_mask = np.zeros((pores_mask.shape), np.uint8)
contour_map = cv2.drawContours(blank_mask, contours[0], -1, 255, 1)
plt.imshow(contour_map, cmap = "gray") 

# #get zernike moments for each CC element 
# #https://cvexplained.wordpress.com/2020/07/21/10-5-zernike-moments/
features=[]
for c in cnts:
    #create an empty mask for the contour and draw it
    mask = np.zeros(pores_mask.shape[:2],dtype="uint8")
    cv2.drawContours(mask, [c], -1,255,-1)
    #extract the bounding box ROI from the mask
    (x,y,w,h)=cv2.boundingRect(c)
    roi=mask[y:y+h,x:x+w]
    # compute Zernike Momemnts for the ROI 
    z = mahotas.features.zernike_moments(roi, cv2.minEnclosingCircle(c)[1], degree=8)
    features.append(z)
    
    features_df = pd.DataFrame(features)
    features_df.to_csv("D:/Crack ML project/Zernike_test_88map3.csv")

# #Fourier descriptors
fd_coeffs = []
for c in cnts:
     # Find the coefficients of all contours
     fd_coeffs.append(elliptic_fourier_descriptors(np.squeeze(c), order=10))

import pyefd
a0, c0 = pyefd.calculate_dc_coefficients(cnts)
pyefd.plot_efd(fd_coeffs, locus=(a0,c0), contour=contours)

fd_coeffs.flatten()[3:]
fd_df = pd.DataFrame(fd_coeffs)


# #Skeleton analysis
skel, distance = medial_axis(pores_mask, return_distance=True)
skel = skeletonize(pores_mask, method = 'lee')
from skan import draw
fig, ax = plt.subplots()
draw.overlay_skeleton_2d(pores_mask, skel, dilate=1, axes=ax)

from skan import Skeleton, summarize
branch_data = summarize(Skeleton(skel))
branch_data.head()

# branch_data.to_csv("D:/Crack ML project/branch data.csv")



# visually inspect random subset of labels
rand_labels_df=pd.read_csv('Shortlisted images/Unstained/SWC A34/Diagrams/SWC A34_diagram_labels.csv')
rand_labels_array=np.asarray(rand_labels_df)
rand_labels=rand_labels_array[:,2]

# loop through label map and set undesired ones to zero
[x,y]=np.shape(pores_label_map)
rand_labels_map=np.zeros([x,y]) #pre-allocate subset label map
for i in range(x):
    for j in range(y):
        if pores_label_map[i,j]>0:
        # check pixel if on random labels list
            if pores_label_map[i,j] in rand_labels: 
                 rand_labels_map[i,j]=pores_label_map[i,j]

plt.figure(1)
plt.imshow(rand_labels_map, cmap = 'turbo')
plt.figure(2)
plt.imshow(pores_label_map, cmap = "turbo")

rand_labels_map_tif = np.uint8(rand_labels_map)

rand_labels_map_int32 = rand_labels_map.astype(np.int32)

io.imsave("Shortlisted images/Unstained/SWC A34/Diagrams/SWC A34_diagram_labels_map.tif", rand_labels_map_tif)


# Drawing the ellipse and bounding box
import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from skimage.draw import ellipse
from skimage.measure import label, regionprops, regionprops_table

regions = regionprops(rand_labels_map_int32)

fig, ax = plt.subplots()
ax.imshow(rand_labels_map_int32, cmap=plt.cm.gray)

for props in regions:
    y0, x0 = props.centroid
    orientation = props.orientation
    x1 = x0 + math.cos(orientation) * 0.5 * props.axis_minor_length
    y1 = y0 - math.sin(orientation) * 0.5 * props.axis_minor_length
    x2 = x0 - math.sin(orientation) * 0.5 * props.axis_major_length
    y2 = y0 - math.cos(orientation) * 0.5 * props.axis_major_length


    ax.plot((x0, x1), (y0, y1), '-r', linewidth=1.5)
    ax.plot((x0, x2), (y0, y2), '-r', linewidth=1.5)
    
    ax.plot(x0, y0, '.g', markersize=5)

    minr, minc, maxr, maxc = props.bbox
    bx = (minc, maxc, maxc, minc, minc)
    by = (minr, minr, maxr, maxr, minr)
    ax.plot(bx, by, '-b', linewidth=2)

fig.savefig('Shortlisted images/Unstained/SWC A34/Diagrams/SWC_A34_cracks_diagram.pdf')
