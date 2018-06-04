import numpy as np

# Need to run ConvertWANDSCDtoQ with KeepTemporaryWorkspaces=True

ws_name = 'hkl'

two_fold = True # Apply two fold rotataion symmetry around the z axis
rotation_axis = 2 # dimension number to rotate arond, starting at 0
mirror_x = True # Mirror in the first dimension
mirror_y = True # Mirror in the second dimension
mirror_z = False # Mirror in the third dimension

#######################################################################################################

try:
    data = mtd[ws_name+'_data']
    data_signal = data.getSignalArray()
    norm = mtd[ws_name+'_normalization']
    norm_signal = norm.getSignalArray()
except KeyError:
    raise RuntimeError('ws_name should be base name and you need to run ConvertWANDSCDtoQ with '
                       'KeepTemporaryWorkspaces=True. {} and {} must exist'.format(ws_name+'_data', ws_name+'_normalization'))

if two_fold:
    d0=data.getDimension(0)
    if not np.isclose(d0.getMaximum(), -d0.getMinimum()):
        raise RuntimeError('For two-fold symmetry the {} dimension must be centered on 0'.format(d0.getName()))
    d1=data.getDimension(1)
    if not np.isclose(d1.getMaximum(), -d1.getMinimum()):
        raise RuntimeError('For two-fold symmetry the {} dimension must be centered on 0'.format(d1.getName()))
    data_signal = data_signal + data_signal[::-1,::-1,:]
    norm_signal = norm_signal + norm_signal[::-1,::-1,:]

if mirror_x:
    d0=data.getDimension(0)
    if not np.isclose(d0.getMaximum(), -d0.getMinimum()):
        raise RuntimeError('To mirror x the {} dimension must be centered on 0'.format(d0.getName()))
    print('Applying mirror symmetry in the {} direction'.format(d0.getName()))
    data_signal = data_signal + data_signal[::-1,:,:]
    norm_signal = norm_signal + norm_signal[::-1,:,:]

if mirror_y:
    d1=data.getDimension(1)
    if not np.isclose(d1.getMaximum(), -d1.getMinimum()):
        raise RuntimeError('To mirror y the {} dimension must be centered on 0'.format(d1.getName()))
    print('Applying mirror symmetry in the {} direction'.format(d1.getName()))
    data_signal = data_signal + data_signal[:,::-1,:]
    norm_signal = norm_signal + norm_signal[:,::-1,:]

if mirror_z:
    d2=data.getDimension(2)
    if not np.isclose(d2.getMaximum(), -d2.getMinimum()):
        raise RuntimeError('To mirror z the {} dimension must be centered on 0'.format(d2.getName()))
    print('Applying mirror symmetry in the {} direction'.format(d2.getName()))
    data_signal = data_signal + data_signal[:,:,::-1]
    norm_signal = norm_signal + norm_signal[:,:,::-1]

CloneMDWorkspace(ws_name+'_data', OutputWorkspace=ws_name+'_data_symmetry')
CloneMDWorkspace(ws_name+'_normalization', OutputWorkspace=ws_name+'_normalization_symmetry')
mtd[ws_name+'_data_symmetry'].setSignalArray(data_signal)
mtd[ws_name+'_normalization_symmetry'].setSignalArray(norm_signal)
DivideMD(ws_name+'_data_symmetry', ws_name+'_normalization_symmetry', OutputWorkspace=ws_name+'_symmetry')
