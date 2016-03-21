import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

basedir = 'faces'
filepaths = [os.path.join(basedir, f) for f in os.listdir(basedir)]
for filepath in filepaths:
    image = cv2.imread(filepath, 0)
    image = cv2.Canny(image, 100, 200)
    plt.imshow(image, 'gray'); plt.show()
