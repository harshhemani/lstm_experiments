
import numpy as np
from scipy.signal import fftconvolve
from matplotlib.mlab import find


def parabolic(f, x):
    if x+1 == len(f):
        x = x-1
    denominator = (f[x-1] - 2 * f[x] + f[x+1])
    if denominator == 0:
        denominator = 1.0E-50
    xv = 1/2. * (f[x-1] - f[x+1]) / denominator + x
    yv = f[x] - 1/4. * (f[x-1] - f[x+1]) * (xv - x)
    return (xv, yv)

def get_pitch(sr, audio):
    corr = fftconvolve(audio, audio[::-1], mode='full')
    corr = corr[len(corr)/2:]
    d = np.diff(corr)
    something = find(d>0)
    if(len(something)==0):
        return 0
    start = something[0]
    peak = np.argmax(corr[start:]) + start
    px, py = parabolic(corr, peak)
    return sr / px

if __name__ == '__main__':
    # generate a dummy signal
    x300 = 0.6 * np.sin((np.arange(8000.) / 8000.) * 2 * np.pi * 300)
    x450 = 0.2 * np.sin((np.arange(8000.) / 8000.) * 2 * np.pi * 450)
    x750 = 0.2 * np.sin((np.arange(8000.) / 8000.) * 2 * np.pi * 750)
    x = x300 + x450 + x750
    sr = 16000
    print get_pitch(sr, x) # should print a value close to 300 because freq 300 has highest amplitude.
    
    
