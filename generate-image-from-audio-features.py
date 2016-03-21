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
    #audio = audio[:sr*30]
    base = 0
    audioLength = len(audio)
    #frameSize = 0.025 * sr; frameShift = 0.015 * sr
    frameSize = 25; frameShift = 15
    amplitudes = None; indicies = None
    featureVectors = []; fvs = []; frameCount = 0
    while (base + frameSize < audioLength):
        frame = audio[base:base+frameSize]
        fv = np.array([np.min(frame), np.max(frame), np.mean(frame), np.var(frame)])
        fvs.append(fv)
        frameCount += 1
        if frameCount%16==0:
            featureVectors.append(fvs)
            fvs = []
        base += frameShift
    return np.array(featureVectors)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print ('\n\tpython ' + sys.argv[0] + ' <filepath>\n')
        sys.exit()
    filepath = sys.argv[1]
    featureVectors = extractFeatureVectors(filepath)
    model = Sequential()
    model.add(LSTM(input_shape=(featureVectors.shape[1], featureVectors.shape[2]), output_dim=128, activation='sigmoid', inner_activation='hard_sigmoid'))
    model.add(Dense(10))
    model.add(Activation('softmax'))
    model.compile(loss='binary_crossentropy', optimizer='rmsprop')
    predictions = model.predict(featureVectors)
    print(predictions.shape)
    penState = predictions[:, -1] < 0.5
    predictions = predictions[:, :-1].reshape(predictions.shape[0], 3, 3)
    image = np.zeros((100, 100))
    base_i = image.shape[0]/2; base_j = image.shape[1]/2
    #base_i = 0; base_j = 0
    for p, isUp in zip(predictions, penState):
        if (isUp):
            pass
        image[base_i, base_j] = 255
        while True:
            delta_i, delta_j = np.unravel_index(p.argmax(), p.shape)
            delta_i -= 1; delta_j -= 1
            if (base_i+delta_i<0 or base_j+delta_j<0 or base_i+delta_i>=image.shape[0] or base_j+delta_j>=image.shape[1]):
                p[delta_i+1, delta_j+1] = 0
            else:
                base_i += delta_i
                base_j += delta_j
                break
    plt.imshow(image)
    plt.show()
