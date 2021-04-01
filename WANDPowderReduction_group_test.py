# import mantid algorithms, numpy and matplotlib
from mantid.simpleapi import *
import matplotlib.pyplot as plt
import numpy as np

from mantid.simpleapi import (
    WANDPowderReduction,
    CreateSampleWorkspace,CloneWorkspace, GroupWorkspaces
)
from mantid.api import WorkspaceGroup
import numpy as np


event_data = CreateSampleWorkspace(
    NumBanks=1,
    BinWidth=20000,
    PixelSpacing=0.1,
    BankPixelWidth=100,
    WorkspaceType="Event",
)
event_cal = CreateSampleWorkspace(
    NumBanks=1,
    BinWidth=20000,
    PixelSpacing=0.1,
    BankPixelWidth=100,
    WorkspaceType="Event",
    Function="Flat background",
)
event_bkg = CreateSampleWorkspace(
    NumBanks=1,
    BinWidth=20000,
    PixelSpacing=0.1,
    BankPixelWidth=100,
    WorkspaceType="Event",
    Function="Flat background",
)

pd_out = WANDPowderReduction(
    InputWorkspace=[event_data, event_data],
    CalibrationWorkspace=event_cal,
    BackgroundWorkspace=event_bkg,
    Target="Theta",
    NumberBins=1000,
    NormaliseBy="None",
    Sum=True,
)

pd_out2 = WANDPowderReduction(
    InputWorkspace=[event_data, event_data],
    CalibrationWorkspace=event_cal,
    BackgroundWorkspace=event_bkg,
    Target="Theta",
    NumberBins=1000,
    NormaliseBy="None",
    Sum=True,
)

event_data2 = CloneWorkspace(event_data)

event_data_group2 = WorkspaceGroup()
event_data_group2.addWorkspace(event_data)
event_data_group2.addWorkspace(event_data2)

pd_out = WANDPowderReduction(
    InputWorkspace=event_data_group2,
    CalibrationWorkspace=event_cal,
    BackgroundWorkspace=event_bkg,
    Target="Theta",
    NumberBins=1000,
    NormaliseBy="None",
    Sum=False,
)

event_data_group = GroupWorkspaces([event_data,event_data2])
pd_out = WANDPowderReduction(
    InputWorkspace=event_data_group,
    CalibrationWorkspace=event_cal,
    BackgroundWorkspace=event_bkg,
    Target="Theta",
    NumberBins=1000,
    NormaliseBy="None",
    Sum=False,
)