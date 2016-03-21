from __future__ import print_function
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import read

def drawImageUsingAudio(filepath):
    sr, audio = read(filepath)
    audio = audio - np.mean(audio)
    audio = audio / np.var(audio)
    #audio = audio[sr*20:sr*30]
    base = 0
    audioLength = len(audio)
    #frameSize = 0.025 * sr; frameShift = 0.015 * sr
    frameSize = 25; frameShift = 15
    amplitudes = None; indicies = None
    image = np.zeros((100, 100))
    i = image.shape[0]/2; j = image.shape[1]/2
    penDown = True
    delta_i = 0
    delta_j = 0
    vals = []
    while (base + frameSize < audioLength):
        frame = audio[base:base+frameSize]
        base += frameShift
        if penDown:
            image[i, j] = 255
        mean = frame.mean()
        vals.append(mean)
    plt.plot(vals)
    plt.show()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print ('\n\tpython ' + sys.argv[0] + ' <filepath>\n')
        sys.exit()
    filepath = sys.argv[1]
    drawImageUsingAudio(filepath)
