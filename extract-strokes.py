import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

def extractStrokes(image):
    xposes, yposes = np.where(image==255)
    strokes = []
    for x, y in zip(xposes, yposes):
        if image[x, y]==255:
            stroke = [(x, y)]
            image[x, y] = 0
            moved = True
            while True:
                if not moved:
                    break
                moved = False
                for i in range(x-1, x+2):
                    for j in range(y-1, y+2):
                        if i<0 or j<0 or i>=image.shape[0] or j>=image.shape[1]:
                            continue
                        if image[i, j]==255:
                            stroke.append((i, j))
                            image[i, j] = 0
                            x = i; y = j
                            moved = True
                            break
                    if moved:
                        break
            strokes.append(stroke)
    return strokes


basedir = 'caltech101/scorpion'
filepaths = [os.path.join(basedir, f) for f in os.listdir(basedir)]
for filepath in filepaths:
    image = cv2.GaussianBlur(cv2.resize(cv2.imread(filepath, 0), (100, 100)), (3, 3), 0)
    image = cv2.Canny(image, 100, 200)
    strokes = extractStrokes(image)
    for stroke in strokes:
        stroke = np.array(stroke)
        if len(stroke)>10:
            plt.plot(stroke[:, 0], stroke[:, 1])
    plt.show()
    
