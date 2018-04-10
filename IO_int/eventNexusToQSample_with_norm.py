import h5py
import numpy as np
import time
t0=time.time()
runs=range(15954, 15954+1801,1) #17754+1)
ipts=20367

instrument='WAND'
wavelength = 1.488

output = np.zeros((401,41,401)) # -8 to 8 (x and z) -0.8 to 0.8 y
output_norm = np.zeros((401,41,401)) # -8 to 8 (x and z) -0.8 to 0.8 y
bin_size = 0.04

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
z_array_norm = xyz[:,:,2]/xyz_norm-1 # Kf - Ki

qx_lab = x_array_norm*k/bin_size
qy_lab = y_array_norm*k/bin_size
qz_lab = z_array_norm*k/bin_size

qy_sample_int = qy_lab.astype(np.int)+20

pixels = 480*512*8
npoints = len(runs)

data_array = np.empty((npoints, 512, 480*8), dtype=np.int64)
phi_array = np.empty((npoints), dtype=np.float64)

def load_data(ipts, run):
    filename='/HFIR/HB2C/IPTS-{}/nexus/HB2C_{}.nxs.h5'.format(ipts,run)
    print('Loading: {}'.format(filename))
    with h5py.File(filename, 'r') as f_in:
        bc = np.zeros((pixels),dtype=np.int64)
        for b in range(8):
            bc += np.bincount(f_in['/entry/bank'+str(b+1)+'_events/event_id'].value,minlength=pixels)
        bc=bc.reshape((-1,512)).T
        phi = np.deg2rad(f_in['/entry/DASlogs/HB2C:Mot:s1.RBV/average_value'].value[0])
    return bc, phi

cal, _ = load_data(7776, 26509)

for n, run in enumerate(runs):
    data, phi = load_data(ipts, run)
    qx_sample_int = (qx_lab*np.cos(phi) - qz_lab*np.sin(phi)).astype(np.int)+200
    qz_sample_int = (qx_lab*np.sin(phi) + qz_lab*np.cos(phi)).astype(np.int)+200
    np.add.at(output, (qx_sample_int.ravel(),
                       qy_sample_int.ravel(),
                       qz_sample_int.ravel()), data.ravel())
    np.add.at(output_norm, (qx_sample_int.ravel(),
                            qy_sample_int.ravel(),
                            qz_sample_int.ravel()), cal.ravel())

t1=time.time()
norm_data = output/output_norm
print(t1-t0)
import matplotlib.pyplot as plt
plt.imshow(norm_data[:,20,:])
plt.show()

plt.imshow(norm_data.sum(axis=1))
plt.show()
