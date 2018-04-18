import multiprocessing as mp
import h5py
import numpy as np
runs=range(15954, 15954+1801,1) #17754+1)
ipts=20367

instrument='WAND'
wavelength = 1.488

pixels = 480*512*8
npoints = len(runs)

data_array = np.empty((npoints, 512, 480*8), dtype=np.int64)
phi_array = np.empty((npoints), dtype=np.float64)
duration_array = np.empty((npoints), dtype=np.float64)
run_number_array = np.empty((npoints), dtype=np.int64)
monitor_count_array = np.empty((npoints), dtype=np.int64)
start_time_array = []

def load_file(run):
    filename='/HFIR/HB2C/IPTS-{}/nexus/HB2C_{}.nxs.h5'.format(ipts,run)
    print(filename)
    with h5py.File(filename, 'r') as f_in:
        bc = np.zeros((pixels),dtype=np.int64)
        for b in range(8):
            bc += np.bincount(f_in['/entry/bank'+str(b+1)+'_events/event_id'].value,minlength=pixels)
        bc=bc.reshape((-1,512)).T
        return bc

pool = mp.Pool(mp.cpu_count())

data_array = np.array(pool.map(load_file, runs))

np.save('IPTS_20367_data_mp.npy',data_array)
