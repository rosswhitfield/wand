#!/bin/bash

for i in `seq 4756 5000`;
do
    echo $i
    mantidpythonnightly /HFIR/HB2C/shared/autoreduce/reduce_HB2C.py /HFIR/HB2C/IPTS-7776/nexus/HB2C_$i.nxs.h5 /HFIR/HB2C/IPTS-7776/shared/autoreduce/
done

