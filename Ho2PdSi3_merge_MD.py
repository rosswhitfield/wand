from mantid.simpleapi import *

start = 1059
end = 1833
end = 1450

if 'mdh' in mtd:
    mtd.remove('mdh')
if 'van_mdh' in mtd:
    mtd.remove('van_mdh')

for run in range(start,end+1,1):
    if run == 1796:
        continue
    try:
        md = LoadMD(Filename='/SNS/users/rwp/wand/MDH/Ho2PdSi3_{}_data_MDH.nxs'.format(run))
        van = LoadMD(Filename='/SNS/users/rwp/wand/MDH/Ho2PdSi3_{}_van_MDH.nxs'.format(run))
    except:
        continue
    if 'mdh' in mtd:
        mdh = mdh + md
    else:
        mdh=CloneWorkspace(md)
    if 'van_mdh' in mtd:
        van_mdh = van_mdh + van
    else:
        van_mdh=CloneWorkspace(van)

norm = mdh/van_mdh
SaveMD('mdh', '/SNS/users/rwp/wand/Ho2PdSi3_data_MDH_{}_{}.nxs'.format(start, end))
SaveMD('van_mdh', '/SNS/users/rwp/wand/Ho2PdSi3_van_MDH_{}_{}.nxs'.format(start, end))
SaveMD('norm', '/SNS/users/rwp/wand/Ho2PdSi3_norm_MDH_{}_{}.nxs'.format(start, end))
