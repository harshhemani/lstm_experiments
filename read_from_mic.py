import alsaaudio, time, audioop

inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE,alsaaudio.PCM_NONBLOCK)

inp.setchannels(1)
inp.setrate(8000)
inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)

inp.setperiodsize(160)
while True:
    l,data = inp.read()
    if l:
        print audioop.max(data, 0)
        #print audioop.max(data, 2)
    time.sleep(.001)
