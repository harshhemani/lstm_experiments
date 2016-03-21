from __future__ import print_function
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import read
from keras.models import Sequential
from keras.layers.recurrent import LSTM
from keras.layers.core import Dense, Dropout, Activation

def extractFeatureVectors(filepath):
    sr, audio = read(filepath)
    audio = audio - np.mean(audio)
    audio = audio / np.var(audio)
    base = 0
    audioLength = len(audio)
    frameSize = 0.025 * sr
    frameShift = 0.015 * sr
    amplitudes = None
    indicies = None
    frameCount = 0
    featureVectors = []
    while (base + frameSize < audioLength):
        frame = audio[base:base+frameSize]
        logEnergySpectrum = np.log(np.absolute(np.fft.rfft(frame)) ** 2)
        top10Indices = np.argsort(logEnergySpectrum)[::-1][:10]
        top10Amplitudes = logEnergySpectrum[top10Indices]
        top10Indices = top10Indices/200.0
        if amplitudes is None:
            amplitudes = top10Amplitudes
        else:
            amplitudes = np.vstack((amplitudes, top10Amplitudes))
        if indicies is None:
            indicies = top10Indices
        else:
            indicies = np.vstack((indicies, top10Indices))
        base += frameShift
        frameCount += 1
        if frameCount%5==0:
            featureVector = np.hstack((indicies, amplitudes))
            featureVectors.append(featureVector)
            indicies = None
            amplitudes = None
    return np.array(featureVectors)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print ('\n\tpython ' + sys.argv[0] + ' <filepath>\n')
        sys.exit()
    filepath = sys.argv[1]
    featureVectors = extractFeatureVectors(filepath)
    print(featureVectors.shape)
    #featureVectors = np.random.rand(1274, 10, 20)
    model = Sequential()
    model.add(LSTM(input_shape=(5, 20), output_dim=128, activation='sigmoid', inner_activation='hard_sigmoid'))
    model.add(Dropout(0.5))
    model.add(Dense(10))
    model.add(Activation('softmax'))
    print('compiling model')
    model.compile(loss='binary_crossentropy', optimizer='rmsprop')
    print('model compilation finished')
    prediction = model.predict(featureVectors)
    image = np.zeros((40, 40))
    i = image.shape[0] / 2
    j = image.shape[1] / 2
    for p in prediction:
        penPosition = p[9] < 0.5
        if penPosition:
            image[i, j] = 255
        grid = p[:-1].reshape(3, 3)
        delta_i, delta_j = np.unravel_index(grid.argmax(), grid.shape)
        delta_i -= 1
        delta_j -= 1
        while True:
            if i + delta_i < 0 or i + delta_i >= image.shape[0] or j + delta_j < 0 or j + delta_j >= image.shape[1]:
                grid[delta_i+1][delta_j+1] = 0
                delta_i, delta_j = np.unravel_index(grid.argmax(), grid.shape)
                delta_i -= 1
                delta_j -= 1
            else:
                i = i + delta_i
                j = j + delta_j
                break;
    plt.imshow(image)
    plt.show()
