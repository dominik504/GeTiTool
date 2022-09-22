import argparse
import os
import sys

from . import GeTiTool
# import GeTiTool

import warnings
warnings.filterwarnings('ignore')

def geti():
    """
    This function is used by the config file to initialize the tool and therefore
    needs no arguments.

    Raises
    ------
    TypeError
        If a Topography file is given, but no Spacing.
    """
    # handling argparse input
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=str,
                        help="directory where raw geotom data is located")
    parser.add_argument("-t", "--topo",
                        help="directory where electrode angles are located, including fileending. Also give the spacing in this case")
    parser.add_argument("-s", "--spacing", type=float,
                        help="Give the spacing used in the field")
    parser.add_argument("-r", "--resipy_settings", type=str,
                        help="Give setting and parameter, seperated by a space, for resipy inversion you wish to change from default. Seperate different parameters with ';'.")
    parser.add_argument("-e", "--elevation", type=float, default=0,
                        help="Add the absolut height of the first electrode above sea level to the calculated topography")
    args=parser.parse_args()
    
    print("##########--------------------##########")
    print("----------   STARTING TOOL    ----------")
    print("##########--------------------##########")
    
    # save argparse arguments into variables
    raw_data = args.directory # e.g. '.wen' files
    topo = args.topo # angles and electrode IDs
    spacing = args.spacing # spacing between electrodes in meter
    height = args.elevation # the absolute height above sea level of Electrode 0
    resipy = args.resipy_settings
    
    # set folder names
    files = raw_data + "/files/"
    vtks = raw_data + "/vtkFiles/"
    datfiles = raw_data + "/datfiles/"
    
    print("----------   CREATING FOLDERS    ----------")
    # check if folders already exist and if yes ask user to continue or not
    if (os.path.isdir(vtks) and os.path.isdir(files) and os.path.isdir(datfiles)) == True:
        print("######################################")
        if os.path.isdir(vtks):
            print("WARNING: Folder for vtk Files already exists.")
        if os.path.isdir(files):
            print("WARNING: Folder for files Files already exists.")
        if os.path.isdir(datfiles):
            print("WARNING: Folder for datfiles Files already exists.")
        print("The Data within this Folder may be overwritten.\n")
        print("Do you want to continue?")
        answer = input("Yes/ No: ")
        if answer[0].lower() == "n":
            sys.exit()
        else:
            print(f"Your answer was {answer}, understood as 'yes'. The Program will continue with its inversion")
        
    ## make output directories
    os.makedirs(raw_data + "/files/", exist_ok=True)
    os.makedirs(raw_data + "/vtkFiles/", exist_ok=True)
    os.makedirs(raw_data + "/datfiles/", exist_ok=True)

    # check if both, spacing and topo is given for the case topo should be considered
    if topo is not None and spacing is None:
        parser.error("Both, spacing and topo must be given")
    
    # initialize tool with user inputs
    print("----------   INITIALIZE INVERSION    ----------")
    GeTiTool.GeTiToolCalc(raw_data=raw_data,
                          topo=topo,
                          spacing=spacing,
                          vtks=vtks,
                          resipy=resipy,
                          height=height,
                          datfiles=datfiles)
    
    print("   ######   #   #   #   #   #####   #    #   ######   ###")
    print("   #        #   ##  #   #   #       #    #   #        #  #")
    print("   ###      #   # # #   #   #####   ######   ###      #   #")
    print("   #        #   #  ##   #       #   #    #   #        #  #")
    print("   #        #   #   #   #   #####   #    #   ######   ###")