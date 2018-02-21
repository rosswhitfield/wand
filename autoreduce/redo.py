import os
import numpy as np
from wand import loadIntegrateData, convertToQSample
from mantid.simpleapi import SaveMD

windows = 4
hostnames = ['ndav1.sns.gov', 'ndav2.sns.gov','ndav3.sns.gov']
node_numbers = windows * len(hostnames)

try:
    window = int(os.environ['WINDOW'])
except KeyError:
    exit("Run in screen")

if window >= windows:
    exit("window out of range")

try:
    hostname = hostnames.index(os.environ['HOSTNAME'])
except ValueError:
    exit("Hostname not in list")

node = hostname * windows + window
print("Node {} out of {}".format(node, node_numbers))


all_runs = range(4756,6557+1)
runs = np.array_split(all_runs, node_numbers)[node]

for run in runs:
    in_file = '/HFIR/HB2C/IPTS-7776/nexus/HB2C_{}.nxs.h5'.format(run)
    out_file = '/SNS/snfs1/testing/ndav/rwp/PNO/HB2C_{}_MDE.nxs'.format(run)
    SaveMD(convertToQSample(loadIntegrateData(in_file)), out_file)
