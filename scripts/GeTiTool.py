from resipy import Project
import pandas as pd
import numpy as np
import argparse
import datetime
import os
import sys
import subprocess

# from . import ConvertGeotomDat
# from . import CalculateTopography

import ConvertGeotomDat
import CalculateTopography

import warnings
warnings.filterwarnings('ignore')

def GeTiToolCalc(raw_data, topo, spacing, iterations, vtks):
    # convert .wen Data to .dat Data
    ConvertGeotomDat.geotom_to_dat(directory=raw_data, file_ending=".wen", header_length=6, columns=3)  # geotom_to_dat Function from conversion.py file
    
    # creating resipy object by using Project()
    datfiles = raw_data + "/datfiles/"
    k = Project(typ="R2")
    
    # define timelapse input from folder
    k.createTimeLapseSurvey(dirname=datfiles, ftype="ResInv")
    if topo != None:
        # calculating electrode topography
        electrodes = CalculateTopography.calculateTopography(file=topo, spacing=spacing, interpolate=True)
        electrodes["y"] = 0 # spaceholder, could be used for absolute coordinates later
        
            
        ## HARDCODED CHANGE!!!!
        # add x and y absolute coordinates
        y = pd.read_csv("C:/Users/domin/OneDrive/Desktop/masterarbeit/Tanneben/Messung1/ungenau_Elektroden/y.txt", header=None)
        electrodes.y = y
        x = pd.read_csv("C:/Users/domin/OneDrive/Desktop/masterarbeit/Tanneben/Messung1/ungenau_Elektroden/x.txt", header=None)
        electrodes.x = x
        electrodes.z = electrodes.z + 720.12
        
        # save csv topo and only keep xyz data (others are available- see the function)
        electrodes[["x", "y", "z"]].to_csv(raw_data + "/files/topo.csv", sep=",", index=False)
        k.importElec(raw_data + "/files/topo.csv")
    
        # creating mesh
        depth = round(len(electrodes)/4)  # depth below first electrode
        k.elec.z = electrodes.z
    
        #  fmd is depth to be calculated, cl_factor reduces size in lower region --> faster calculation
        k.createMesh(fmd=depth, typ="trian", cl_factor=10)
    else:
        #  fmd is depth to be calculated, cl_factor reduces size in lower region --> faster calculation
        k.createMesh(typ="trian", cl_factor=10)
    
    k.showMesh()
    # inverting the data
    k.param["max_iter"] = iterations
    k.invert(parallel=True)
    
    # save vtks
    k.saveVtks(vtks)
    return k