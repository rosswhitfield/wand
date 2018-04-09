import numpy as np

data = np.load('IPTS_20367_data.npy')
phi = np.deg2rad(np.load('IPTS_20367_phi.npy'))

output = np.zeros((401,41,401)) # -10 to 10 (x and z) -1 to 1 y
bin_size = 0.05

s2 = 2.0
detz = 0.0
k = 2*np.pi/1.488

theta = np.deg2rad(np.linspace(0,120,8*480)+s2)[::-1]
x = np.sin(theta)*72
z = np.cos(theta)*72
y = np.linspace(-10,10,512)+detz

x_array = np.tile(x,(512,1))
z_array = np.tile(z,(512,1))
y_array = np.tile(y,(8*480,1)).T
xyz=np.dstack((x_array,y_array,z_array))
xyz_norm = np.linalg.norm(xyz,axis=2)

x_array_norm = xyz[:,:,0]/xyz_norm
y_array_norm = xyz[:,:,1]/xyz_norm
z_array_norm = xyz[:,:,2]/xyz_norm

qx_lab = x_array_norm*k/bin_size
qy_lab = y_array_norm*k/bin_size
qz_lab = z_array_norm*k/bin_size

qy_sample_int = qy_lab.astype(np.int)+20

for n, p in enumerate(phi):
    qx_sample_int = (qx_lab*np.cos(p) - qz_lab*np.sin(p)).astype(np.int)+200
    qz_sample_int = (qx_lab*np.sin(p) + qz_lab*np.cos(p)).astype(np.int)+200
    np.add.at(output, (qx_sample_int.ravel(),
                       qy_sample_int.ravel(),
                       qz_sample_int.ravel()), data[n].ravel())

import matplotlib.pyplot as plt
plt.imshow(output[:,20,:])
plt.show()

plt.imshow(output.sum(axis=1))
plt.show()
