import numpy as np
from scipy import ndimage
import matplotlib.pyplot as plt

a = np.load('/SNS/users/rwp/WAND_hex_array.npy')

threshold = 1e-8

b=a[:,:,250]
b[np.isnan(b)]=0
b[b<threshold]=0


plt.imshow(b,vmin=threshold,vmax=threshold*2)
plt.colorbar()
plt.show()

labeled_array, num_features = ndimage.label(b)

com = ndimage.measurements.center_of_mass(b, labeled_array, list(range(1, num_features+1)))

x=[]
y=[]
for xxx, yyy in com:
    x.append(xxx)
    y.append(yyy)

plt.scatter(y,-np.array(x))
plt.show()



plt.pcolormesh(a[:,:,250],vmax=threshold)
plt.colorbar()
plt.scatter(y, x, marker='x', color='r')
plt.show()


c=a[:,:,250]
c[np.isnan(c)]=0
c=ndimage.grey_dilation(c,size=(3,3))
threshold=2e-9
c[c<threshold]=0

plt.imshow(c,vmax=threshold)
plt.colorbar()
plt.show()



minimums, maximums, min_positions, max_positions = ndimage.extrema(b, labeled_array, list(range(1, num_features+1)))

max_pos = np.array([[_x,_y] for _x,_y in max_positions])

