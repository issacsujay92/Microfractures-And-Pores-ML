# Import binary mask and the label map
binary_mask = io.imread("insert image path of the binary mask")
pores_mask = io.imread("insert path of the label map")

# visually inspect random subset of labels
rand_labels_df=pd.read_csv("insert path of the csv file containing the randomly selected labels")
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

io.imsave("insert image destination path", rand_labels_map_tif)

# Drawing the ellipse and bounding box
import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from skimage.draw import ellipse
from skimage.measure import label, regionprops, regionprops_table
import cv2

# Import the binary mask
image = cv2.imread("insert binary image path")
num_labels, pores_label_map = cv2.connectedComponents(pores_mask, connectivity = 8)
regions = regionprops(pores_label_map)

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

fig.savefig("insert image destination path")
