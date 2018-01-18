import numpy as np
import matplotlib.pyplot as plt

s=np.load('data_norm.npy')
plt.imshow(s[:,21,:],vmax=np.nanmax(s)/100)
plt.show()


np.where(s>0.05)

