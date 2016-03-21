import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


ims = []
for i in range(20):
    ims.append(np.random.rand(50, 50))

fig = plt.figure()
im = plt.imshow(np.zeros((50, 50)), cmap=plt.get_cmap('jet'), vmin=0, vmax=255, animated=True)

def update(j):
    im.set_array(ims[j])
    return im,

animation.FuncAnimation(fig, update, frames=range(20), interval=50, blit=False)
plt.show()

