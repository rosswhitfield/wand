#!/bin/env/env python
from mantid.simpleapi import *

result = CreateGroupingWorkspace(InstrumentName = 'WAND')

grouping = result[0]

group = 0

for x in range(0,480*8,4):
    for y in range(0,512,4):
        group += 1
        for j in range(4):
            for i in range(4):
                grouping.dataY(y+i+(x+j)*512)[0] = group

SaveDetectorsGrouping(grouping, "HB2C_4x4.xml")


result = CreateGroupingWorkspace(InstrumentName = 'WAND')

grouping = result[0]

group = 0

for x in range(0,480*8,2):
    for y in range(0,512,2):
        group += 1
        for j in range(2):
            for i in range(2):
                grouping.dataY(y+i+(x+j)*512)[0] = group

SaveDetectorsGrouping(grouping, "HB2C_2x2.xml")
