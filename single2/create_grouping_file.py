#!/bin/env/env python

groupingFileContent = "122880\n"

group = 0

for x in range(0,480*8,4):
    for y in range(0,512,4):
        group += 1
        groupingFileContent += str(group) + "\n16\n"
        detID = []
        for j in range(4):
            for i in range(4):
                detID.append(str(1+y+i+(x+j)*512))
        groupingFileContent += ' '.join(detID)
        groupingFileContent += "\n"

with open("HB2C_4x4.map", 'w') as f:
    f.write(groupingFileContent)
