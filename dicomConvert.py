import pydicom as dicom
import numpy as np
from PIL import Image
import matplotlib.pylab as plt

image_path = 'C:\\Users\\User\\Downloads\\CHEST_PA_2577.dcm';
ds = dicom.dcmread(image_path)
plt.imshow(ds.pixel_array)