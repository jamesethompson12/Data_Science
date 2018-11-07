#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 13:19:40 2018

@author: jamesthompson
"""


import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# ---------------------------------------------------------------------
# Image import
# ---------------------------------------------------------------------

cwd = os.getcwd() + '/Image_Manipulation/img/raw/'


# load the image and flatten to 1d array
floating_garden = plt.imread(cwd + 'floating_garden.jpg')

# setup figure(s) and image(s) save dirs
img_save = os.getcwd() + '/Image_Manipulation/img/'
fig_save = os.getcwd() + '/Image_Manipulation/figs/'


# ---------------------------------------------------------------------
# Image exploration
# ---------------------------------------------------------------------

# separate the rgb values into arrays
red, green, blue = floating_garden[:, :, 0], floating_garden[:, :, 1], floating_garden[:, :, 2]

# flatten rgb arrays to display as hist(s)
red_pix, green_pix, blue_pix = red.flatten(), green.flatten(), blue.flatten()



# display the original image for reference
plt.subplot(2, 1, 1)
plt.title('Original Image')
plt.axis('off')
plt.imshow(floating_garden)

# display the histogram of the rgb vlaues underneath the original image
plt.subplot(2, 1, 2)
plt.title('RGB histogram')
plt.xlim(0, 256)
plt.hist(red_pix, color = 'red', density = True, bins = 64, alpha = 0.2, label = 'red')
plt.hist(green_pix, color = 'green', density = True, bins = 64, alpha = 0.2, label = 'green')
plt.hist(blue_pix, color = 'blue', density = True, bins = 64, alpha = 0.2, label = 'blue')
plt.legend(loc = 'upper right')

plt.savefig(fig_save + 'float_gard_rbg.jpg')
plt.show()

plt.clf()


# ---------------------------------------------------------------------
# Greyscale conversion
# ---------------------------------------------------------------------

# convert the pixel arrays to a dataframe  
grey_img = pd.DataFrame.from_dict({'red' : red_pix, 'green' : green_pix, 'blue' : blue_pix})

# avg the values and extract
grey_img['greyscale'] = grey_img.mean(axis = 1)

grey_ver = np.array(grey_img['greyscale']).reshape(floating_garden.shape[0:2])

# output the converted image to the console and save to file
plt.axis('off')
plt.title('Floating Garden greyscale conversion')
plt.imshow(grey_ver, cmap = 'gray')

plt.savefig(img_save + 'float_gard_grey.jpg', dpi = 600)

# plot PDF with CDF overlay for greyscale pixel values 
plt.clf()
plt.title('PDF and CDF of greyscale pixel values')
plt.hist(grey_img['greyscale'], bins = 64, density = True, range = (0, 256), alpha = 0.4)
plt.ylabel('Pixel value frequency')
plt.xlabel('Pixel value')
plt.twinx()
plt.hist(grey_img['greyscale'], bins = 64, density = True, range = (0, 256), cumulative = True, alpha = 0.4, color = 'red')
plt.ylabel('CDF')

plt.savefig(fig_save + 'greyscale_pixel_dist.jpg')
plt.show()
