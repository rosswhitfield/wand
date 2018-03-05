from mantid.simpleapi import LoadNexus, LoadWAND
from wand import reduceToPowder


name = 'Silicon'
append = False
IPTS = 7776
run = 
vanadium = None
use_autoreduced = True
use_autoreduced_van = True

units = 'Theta' # One of (Theta, ElasticQ, ElasticDSpacing)
Binning = '10,135,2500' # Min,Max,Number_of_bins


###############################################################################
#                    Do not edit below                                        #
###############################################################################

iptsdir = '/HFIR/HB2C/IPTS-{}/'.format(IPTS)

name_MDE = name+'_MDE'
filename = ''

if not append and name_MDE in mtd:
        DeleteWorkspace(name_MDE)
        

# Using all autoreduced
norm = LoadNexus(Filename='/HFIR/HB2C/IPTS-7776/shared/autoreduce/HB2C_6585.nxs')
si = LoadNexus(Filename='/HFIR/HB2C/IPTS-7776/shared/autoreduce/HB2C_6578.nxs')

reduceToPowder(si,'si_no_norm')
reduceToPowder(si, 'si_norm', norm)
