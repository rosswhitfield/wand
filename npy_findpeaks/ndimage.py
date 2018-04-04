import numpy as np
from scipy import ndimage
import matplotlib.pyplot as plt

a = np.load('/SNS/users/rwp/WAND_hex_array.npy')

threshold = 1e-8

b=a[:,:,250]
b[np.isnan(b)]=0
b[threshold]=0


plt.imshow(b,vmin=threshold)
plt.colorbar()
plt.show()

labeled_array, num_features = ndimage.label(b)

com = ndimage.measurements.center_of_mass(b, labeled_array, list(range(1, num_features+1)))

x=[]
y=[]
for xxx, yyy in com:
    x.append(xxx)
    y.append(yyy)

plt.scatter(x, y)
plt.show()


plt.imshow(b,vmin=threshold)
plt.scatter(x, y)
plt.colorbar()
plt.show()
