from resipy import Project
import pandas as pd
import numpy as np
import argparse
import datetime
import os
import sys
import subprocess

# from . import GeTiTool
import GeTiTool

import warnings
warnings.filterwarnings('ignore')

def geti():
    # handling argparse input
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=str,
                        help="directory where raw geotom data is located")
    parser.add_argument("-t", "--topo",
                        help="directory where electrode angles are located, including fileending. Also give the spacing in this case")
    parser.add_argument("-s", "--spacing", type=float,
                        help="Give the spacing used in the field")
    parser.add_argument("-i", "--iterations", type=int, default=5,
                        help="Give the number of maximum iterations, default is five.")
    args=parser.parse_args()
    
    # save argparse arguments into variables
    raw_data = args.directory
    topo = args.topo
    spacing = args.spacing
    iterations = args.iterations
    
    # set folder names and check if they already exist
    files = raw_data + "/files/"
    vtks = raw_data + "/vtkFiles/"
    datfiles = raw_data + "/datfiles/"
    
    if (os.path.isdir(vtks) and os.path.isdir(files) and os.path.isdir(datfiles)) == True:
        print("######################################")
        if os.path.isdir(vtks):
            print("WARNING: Folder for vtk Files already exists.")
        if os.path.isdir(files):
            print("WARNING: Folder for files Files already exists.")
        if os.path.isdir(datfiles):
            print("WARNING: Folder for datfiles Files already exists.")
        print("The Data within this Folder may be overwritten.\n")
        print("Do you want to continue? (yes/no)")
        answer = input()
        if answer[0].lower() == "n":
            sys.exit()
        else:
            print(f"Your answer was {answer}, understood as 'yes'. The Program will continue with its inversion")
        
    ## make output directories
    # make directory for files, vtks and datfiles to save if needed
    os.makedirs(raw_data + "/files/", exist_ok=True)
    os.makedirs(raw_data + "/vtkFiles/", exist_ok=True)
    # folder for datfiles is made within geotom_to_dat Function
    
    # check if both, spacing and topo is given for the case topo should be considered
    if topo is not None and spacing is None:
        raise TypeError("Both, spacing and topo must be given")
        sys.exit()

    GeTiTool.GeTiToolCalc(raw_data, topo, spacing, iterations, vtks)
geti()