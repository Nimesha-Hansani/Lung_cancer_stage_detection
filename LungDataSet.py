#!/usr/bin/env python
# coding: utf-8

# In[14]:


import os
import pydicom
import torch
import numpy as np
import matplotlib.pyplot as plt
from easyfsl.utils import plot_images, sliding_average


# In[2]:


root_path ='C:/Nimesha/MSC_UOM/Research/Lung_cancer_stage_detection/Data/Support'

def load_scan(path):
    slices = [pydicom.dcmread(root_path + '/' + s) for s in os.listdir(path)]
    slices = [s for s in slices if 'SliceLocation' in s]
    
    try:
        slice_thickness = np.abs(slices[0].ImagePositionPatient[2] - slices[1].ImagePositionPatient[2])
    except:
        slice_thickness = np.abs(slices[0].SliceLocation - slices[1].SliceLocation)
    
    for s in slices:
        s.SliceThickness = slice_thickness
    return slices


# In[3]:


def get_pixels_hu(scans):
    
    image = np.stack([s.pixel_array for s in scans])
    image = image.astype(np.int16)
    # Set outside-of-scan pixels to 0
    # The intercept is usually -1024, so air is approximately 0
    image[image == -2000] = 0
    
    # Convert to Hounsfield units (HU)
    intercept = scans[0].RescaleIntercept
    slope = scans[0].RescaleSlope
    
    if slope != 1:
        image = slope * image.astype(np.float64)
        image = image.astype(np.int16)
        
    image += np.int16(intercept)
    
    return np.array(image, dtype=np.int16)


# In[16]:


patient_dicom=load_scan(root_path)
patient_pixels = get_pixels_hu(patient_dicom)
patient_tensor= torch.from_numpy(patient_pixels)


# In[ ]:


plot_images(patient_tensor, "support images", images_per_row=5)


# In[ ]:




