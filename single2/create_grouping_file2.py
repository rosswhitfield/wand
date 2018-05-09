#!/bin/env/env python
import time
from mantid.simpleapi import *

t0=time.time()
result = CreateGroupingWorkspace(InstrumentName = 'WAND')

grouping = result[0]

group = 0

for x in range(0,480*8,4):
    for y in range(0,512,4):
        group += 1
        for j in range(4):
            for i in range(4):
                grouping.dataY(y+i+(x+j)*512)[0] = group

t1=time.time()
#SaveDetectorsGrouping(grouping, "HB2C_4x4.xml")


t2=time.time()
result = CreateGroupingWorkspace(InstrumentName = 'WAND')

grouping = result[0]

group = 0

for x in range(0,480*8,2):
    for y in range(0,512,2):
        group += 1
        for j in range(2):
            for i in range(2):
                grouping.dataY(y+i+(x+j)*512)[0] = group

t3=time.time()

#SaveDetectorsGrouping(grouping, "HB2C_2x2.xml")

print(t1-t0)
print(t3-t2)
