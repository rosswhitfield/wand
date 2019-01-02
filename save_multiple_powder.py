grp = mtd['group_name']

# Save by run number
for ws in grp:
    SaveFocusedXYE(ws, SplitFiles=False, IncludeHeader=False,
                   Filename='{}.xye'.format(ws.getTitle()))

# Save by title
for ws in grp:
    SaveFocusedXYE(ws, SplitFiles=False, IncludeHeader=False,
                   Filename='{}.xye'.format(ws.getRunNumber()))

# Save by run number and title
for ws in grp:
    SaveFocusedXYE(ws, SplitFiles=False, IncludeHeader=False,
                   Filename='{}-{}.xye'.format(ws.getRunNumber(), ws.getTitle()))

# Save by average log value
logName = "HB2C:SE:SampleTemp"
for ws in grp:
    SaveFocusedXYE(ws, SplitFiles=False, IncludeHeader=False,
                   Filename='{}-{}.xye'.format(ws.getRunNumber(), ws.getRun().getLogData(logName).timeAverageValue()))
