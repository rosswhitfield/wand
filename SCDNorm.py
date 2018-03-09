from wand import convertToHKL
from mantid.simpleapi import (LoadMD, DeleteWorkspace, LoadWAND,
                              SaveMD, BinMD, ConvertToMD, mtd)

# change to following values

name = 'EuPdIn4'
IPTS = 20319
first_run = 7562
last_run = first_run+100 #8762
vanadium = 7553
load_every = 1
ub_file = '/HFIR/HB2C/IPTS-20319/shared/EuPdIn4_MDE.mat'

# Binning for MD histo workspace; min,max,number_of_bins
Uproj=(1,0,0)
Vproj=(0,1,0)
Wproj=(0,0,1)
BinningDim0 = '-10,10,200'
BinningDim1 = '-10,10,200'
BinningDim2 = '-10,10,200'

###############################################################################
###############################################################################
###############################################################################

iptsdir = '/HFIR/HB2C/IPTS-{}/'.format(IPTS)

data = name+'_data'
norm = name+'_norm'

# Get UB from file
CreateSingleValuedWorkspace(OutputWorkspace='__ub')
LoadIsawUB('__ub',ub_file)
ub=mtd['__ub'].sample().getOrientedLattice().getUB().copy()
DeleteWorkspace(Workspace='__ub')

if 'cal' not in mtd: # Only load vanadium once
        LoadWAND(Filename=iptsdir+'shared/autoreduce/HB2C_{}.nxs.h5'.format(vanadium), OutputWorkspace='cal')

if data in mtd:
    DeleteWorkspace(data)

if norm in mtd:
    DeleteWorkspace(norm)

for run in range(first_run, last_run+1, load_every):
    filename = iptsdir+'nexus/HB2C_{}.nxs.h5'.format(run)
    LoadWAND(filename, OutputWorkspace='__ws')
    CopyInstrumentParameters('__ws', cal)
    mtd['cal'].run().getGoniometer().setR(mtd['__ws'].getExperimentInfo(0).run().getGoniometer().getR())
    convertToHKL('__ws', OutputWorkspace=data, UB=ub, Append=True, Uproj=Uproj, Vproj=Vproj, Wproj=Wproj)
    convertToHKL(cal, OutputWorkspace=norm, UB=ub, Append=True, Uproj=Uproj, Vproj=Vproj, Wproj=Wproj, Scale=mtd['__ws'].getProtonCharge())


SaveMD(data, iptsdir+'shared/{}_MDH_{}_to_{}_every_{}.nxs'.format(data, first_run, last_run, load_every))
SaveMD(norm, iptsdir+'shared/{}_MDH_{}_to_{}_every_{}.nxs'.format(norm, first_run, last_run, load_every))

