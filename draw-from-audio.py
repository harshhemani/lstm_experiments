from __future__ import print_function

import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import read
from scipy.ndimage import gaussian_filter as G

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('\nSyntax\n\tpython '+sys.argv[0]+' <path-to-audio>\n')
        sys.exit(255)
    filepath = sys.argv[1]
    try:
        sr, audio = read(filepath)
    except Exception as e:
        print('Error reading audio: ' + e)
    if sr != 16000:
        print('Invalid audio! Sampling rate must be 16k.')
        sys.exit()
    if len(audio.shape)>1:
        audio = np.mean(audio, 0)
    frame_base = 0
    frame_size = 0.050 * sr
    frame_shift = 0.020 * sr
    pitch_list = []
    while frame_base + frame_size < len(audio):
        frame = audio[frame_base:frame_base+frame_size]
        spectrum = np.fft.rfft(frame).__abs__()
        pitch = (spectrum.argmax()/float(len(spectrum))) * (sr/2.0)
        pitch_list.append(pitch)
        frame_base += frame_shift
    #plt.plot(pitch_list)
    pitch_list = np.array(pitch_list)
    smooth_pitch_list = G(pitch_list, 9)
    #plt.plot(smooth_pitch_list)
    #plt.show()
    magic1 = 627.0
    magic2 = 577.0
    angles_in_radians = ((smooth_pitch_list % int(magic1)) / magic1) * 2 * np.pi
    colors = ((smooth_pitch_list % int(magic2)) / magic2) * 255.0
    xlim = 500
    ylim = 500
    img = np.zeros((xlim, ylim))
    base_x = np.random.randint(xlim/13, 5*xlim/13)
    base_y = np.random.randint(ylim/13, 5*ylim/13)
    for angle, color in zip(angles_in_radians, colors):
        img[base_x, base_y] = color
        base_x += np.cos(angle)
        base_y += np.sin(angle)
        if base_x < 0:
            base_x = 0
        if base_y < 0:
            base_y = 0
        if base_x > xlim-1:
            base_x = xlim-1
        if base_y > ylim-1:
            base_y = ylim-1
    plt.imshow(img)
    plt.show()
