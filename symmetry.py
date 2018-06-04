import numpy as np

# Need to run ConvertWANDSCDtoQ with KeepTemporaryWorkspaces=True

ws_name = 'hkl'

two_fold = False # Apply two fold rotataion symmetry in the rotation_axes plane
four_fold = True # Apply four fold rotataion symmetry in the rotation_axes plane
rotation_axes = (0,1) # plane of rotation
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

def flip(m, axis=None):
    if not hasattr(m, 'ndim'):
        m = np.asarray(m)
    if axis is None:
        indexer = (np.s_[::-1],) * m.ndim
    else:
        axis = _nx.normalize_axis_tuple(axis, m.ndim)
        indexer = [np.s_[:]] * m.ndim
        for ax in axis:
            indexer[ax] = np.s_[::-1]
        indexer = tuple(indexer)
    return m[indexer]

def rot90(m, k=1, axes=(0,1)):
    axes = tuple(axes)
    if len(axes) != 2:
        raise ValueError("len(axes) must be 2.")

    m = np.asanyarray(m)

    if axes[0] == axes[1] or np.absolute(axes[0] - axes[1]) == m.ndim:
        raise ValueError("Axes must be different.")

    if (axes[0] >= m.ndim or axes[0] < -m.ndim
        or axes[1] >= m.ndim or axes[1] < -m.ndim):
        raise ValueError("Axes={} out of range for array of ndim={}."
                         .format(axes, m.ndim))

    k %= 4

    if k == 0:
        return m[:]
    if k == 2:
        return flip(flip(m, axes[0]), axes[1])

    axes_list = arange(0, m.ndim)
    (axes_list[axes[0]], axes_list[axes[1]]) = (axes_list[axes[1]],
                                                axes_list[axes[0]])

    if k == 1:
        return np.transpose(flip(m,axes[1]), axes_list)
    else:
        # k == 3
        return flip(np.transpose(m, axes_list), axes[1])

if two_fold:
    d0=data.getDimension(rotation_axes[0])
    if not np.isclose(d0.getMaximum(), -d0.getMinimum()):
        raise RuntimeError('For two-fold symmetry the {} dimension must be centered on 0'.format(d0.getName()))
    d1=data.getDimension(rotation_axes[1])
    if not np.isclose(d1.getMaximum(), -d1.getMinimum()):
        raise RuntimeError('For two-fold symmetry the {} dimension must be centered on 0'.format(d1.getName()))
    data_signal = data_signal + np.flip(np.flip(data_signal, rotation_axes[0]), rotation_axes[1])
    norm_signal = norm_signal + np.flip(np.flip(norm_signal, rotation_axes[0]), rotation_axes[1])

if four_fold:
    d0=data.getDimension(rotation_axes[0])
    if not np.isclose(d0.getMaximum(), -d0.getMinimum()):
        raise RuntimeError('For four-fold symmetry the {} dimension must be centered on 0'.format(d0.getName()))
    d1=data.getDimension(rotation_axes[1])
    if not np.isclose(d1.getMaximum(), -d1.getMinimum()):
        raise RuntimeError('For four-fold symmetry the {} dimension must be centered on 0'.format(d1.getName()))
    if d0.getNBins() != d1.getNBins():
        raise RuntimeError('For four-fold symmetry the {} and {} dimensions must have equal number of bins'.format(d0.getName(),d1.getName()))
    axes_list = np.arange(0, data_signal.ndim)
    (axes_list[rotation_axes[0]], axes_list[rotation_axes[1]]) = (axes_list[rotation_axes[1]], axes_list[rotation_axes[0]])
    data_signal = data_signal + np.transpose(np.flip(data_signal,rotation_axes[1]), axes_list) + np.flip(np.flip(data_signal, rotation_axes[0]), rotation_axes[1]) + np.flip(np.transpose(data_signal, axes_list), rotation_axes[1])
    norm_signal = norm_signal + np.transpose(np.flip(norm_signal,rotation_axes[1]), axes_list) + np.flip(np.flip(norm_signal, rotation_axes[0]), rotation_axes[1]) + np.flip(np.transpose(norm_signal, axes_list), rotation_axes[1])

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
