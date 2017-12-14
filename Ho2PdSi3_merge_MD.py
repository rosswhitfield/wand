from mantid.simpleapi import *

start = 1059
end = 1833

for run in range(start,end+1,1):
    if run == 1796:
        continue
    md = LoadNexus(Filename='/SNS/users/rwp/wand/Ho2PdSi3_{}_data_MDH.nxs'.format(run))
    van = LoadNexus(Filename='/SNS/users/rwp/wand/Ho2PdSi3_{}_van_MDH.nxs'.format(run))
    if 'mdh' in mtd:
        mdh = mdh + mdh_tmp
    else:
        mdh=CloneWorkspace(mdh_tmp)
    if 'van_mdh' in mtd:
        van_mdh = van_mdh + van_mdh_tmp
    else:
        van_mdh=CloneWorkspace(van_mdh_tmp)

norm = mdh/van_mdh
SaveMD('mdh', '/SNS/users/rwp/wand/Ho2PdSi3_data_MDH_{}_{}.nxs'.format(start, end))
SaveMD('van_mdh', '/SNS/users/rwp/wand/Ho2PdSi3_van_MDH_{}_{}.nxs'.format(start, end))
SaveMD('norm', '/SNS/users/rwp/wand/Ho2PdSi3_norm_MDH_{}_{}.nxs'.format(start, end))
