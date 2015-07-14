from __future__ import print_function
from scipy.io.wavfile import read, write
from sptools_pitch import get_pitch
from pybrain.datasets import SequentialDataSet
from pybrain.tools.shortcuts import buildNetwork
from pybrain.structure.modules import LSTMLayer
from pybrain.supervised import RPropMinusTrainer
from sys import stdout
import matplotlib.pyplot as plt
import cPickle

sr, audio = read('test.wav')
net = cPickle.load(open('nnet.pkl', 'r'))
base = 0
frame_size = int(0.025 * sr)
frame_shift = int(0.010 * sr)
pitches = []
inputs = []
outputs = []
while base + frame_size <= len(audio):
    frame = audio[base:base+frame_size]
    pitch = get_pitch(sr, frame)
    pitches.append(pitch)
    base += frame_shift
    outputs.append(frame)

inputs.append([-1, -1, -1, -1, pitches[0]])
inputs.append([-1, -1, -1, pitches[0], pitches[1]])
inputs.append([-1, -1, pitches[0], pitches[1], pitches[2]])
inputs.append([-1, pitches[0], pitches[1], pitches[2], pitches[3]])

for i in range(4, len(pitches)):
    inputs.append([pitches[i-4], pitches[i-3], pitches[i-2], pitches[i-1], pitches[i]])

for sample, target in zip(inputs, outputs):
    print(sample)
    print(net.activate(sample))
    print(target)
