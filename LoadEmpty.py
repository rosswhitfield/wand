ws=LoadEmptyInstrument(Filename='/SNS/users/rwp/WAND_Definition_2018_02_20.xml')
AddSampleLog(ws, LogName='HB2C:Mot:s2.RBV', LogText='5', LogType='Number Series',NumberType='Double')
AddSampleLog(ws, LogName='HB2C:Mot:detz.RBV', LogText='100', LogType='Number Series',NumberType='Double')
LoadInstrument(ws, Filename='/SNS/users/rwp/WAND_Definition_2018_02_20.xml', RewriteSpectraMap=False)
