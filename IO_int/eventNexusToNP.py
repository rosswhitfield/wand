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

for n, run in enumerate(runs):
    filename='/HFIR/HB2C/IPTS-{}/nexus/HB2C_{}.nxs.h5'.format(ipts,run)
    print(filename)
    with h5py.File(filename, 'r') as f_in:
        bc = np.zeros((pixels),dtype=np.int64)
        for b in range(8):
            bc += np.bincount(f_in['/entry/bank'+str(b+1)+'_events/event_id'].value,minlength=pixels)
        bc=bc.reshape((-1,512)).T
        data_array[n] = bc
        phi_array[n] = f_in['/entry/DASlogs/HB2C:Mot:s1.RBV/average_value'].value[0]
        duration_array[n] = f_in['/entry/duration'].value
        run_number_array[n] = f_in['/entry/run_number'].value
        monitor_count_array[n] = f_in['/entry/monitor1/total_counts'].value
        start_time_array.append(f_in['/entry/start_time'].value[0])

np.save('IPTS_20367_data.npy',data_array)
np.save('IPTS_20367_phi.npy',phi_array)
