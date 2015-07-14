
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

sr, audio = read('train.wav')

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

ds = SequentialDataSet(5, frame_size)
for i, o in zip(inputs, outputs):
    ds.addSample(i, o)


net = buildNetwork(5, 10, frame_size, hiddenclass=LSTMLayer, outputbias=False, recurrent=True)
trainer = RPropMinusTrainer(net, dataset=ds)
train_errors = [] # save errors for plotting later
EPOCHS_PER_CYCLE = 5
CYCLES = 10
EPOCHS = EPOCHS_PER_CYCLE * CYCLES
for i in xrange(CYCLES):
    trainer.trainEpochs(EPOCHS_PER_CYCLE)
    train_errors.append(trainer.testOnData())
    epoch = (i+1) * EPOCHS_PER_CYCLE
    print("\r epoch {}/{}".format(epoch, EPOCHS), end="")
    stdout.flush()
print()
print("final error =", train_errors[-1])


cPickle.dump(net, open('nnet.pkl', 'w'))


plt.plot(range(0, EPOCHS, EPOCHS_PER_CYCLE), train_errors)
plt.xlabel('epoch')
plt.ylabel('error')
plt.show()
