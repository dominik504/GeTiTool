from resipy import Project
import pandas as pd

from . import ConvertGeotomDat
from . import CalculateTopography

# import ConvertGeotomDat
# import CalculateTopography

import warnings
warnings.filterwarnings('ignore')

def GeTiToolCalc(raw_data, topo, spacing, vtks, resipy, height, datfiles):
    """
    This is the main function to run the inversion using resipy.
    It takes all the user inputs and by using the other function calculates
    all necessary stuff before the inversion can start

    Parameters
    ----------
    raw_data : String
        Folder where all the measured raw data is within.
    topo : String
        File including the path where the Topography can be found.
    spacing : Float
        Spacing of the electrodes.
    iterations : Integer
        Number of iterations to calculate.
    vtks : String
        Folder where the results as vtk files should be saved.
    resipy : String
        settings for resipy inversion. If there is more than one setting they must
        be seperated by a ';'. The values per setting must be seperated by a space.
    height : Float
        The absolute Height above Sealevel which will be added to the Electrodes 
        z values.
    datfiles : String
        Path where the datfiles are located for timelapse inversion

    """
    # convert .wen Data to .dat Data
    print("----------   CONVERT GEOTOM RAW DATA    ----------")
    ConvertGeotomDat.geotom_to_dat(directory=raw_data, file_ending=".wen", header_length=6, columns=3)
    
    # creating resipy object
    k = Project(typ="R2")
    
    # define timelapse input from folder
    k.createTimeLapseSurvey(dirname=datfiles, ftype="ResInv")
    
    if topo:
        print("----------   CALCULATE TOPOGRAPHY    ----------")
        # calculating electrode topography
        electrodes = CalculateTopography.calculateTopography(file=topo, spacing=spacing)
        electrodes["y"] = 0 # spaceholder, may be used for absolute coordinates later
        electrodes.z = electrodes.z + height
        
        # save csv topo and only keep xyz data (others are available- see the function)
        electrodes[["x", "y", "z"]].to_csv(raw_data + "/files/topo.csv", sep=",", index=False)
        k.importElec(raw_data + "/files/topo.csv") # get electrode topo from file
    
        # creating mesh
        depth = round(len(electrodes)/4)  # depth below first electrode
    
        # fmd is depth to be calculated, cl_factor reduces size in lower region --> faster calculation
        k.createMesh(fmd=depth, typ="trian", cl_factor=10)
    else:
        # cl_factor reduces size in lower region --> faster calculation
        k.createMesh(typ="trian", cl_factor=10)
    
    k.showMesh()

    # set resipy parameter inversion settings given by user    
    if resipy != None:
        for i in range(len(resipy.split(";"))):
            k.param[f"{resipy.split(';')[i].split(',')[0]}"] = resipy.split(';')[i].split(',')[1:][0]
    
    # inverting the data
    print("----------   START INVERSION    ----------")
    k.invert(parallel=True)
    
    print("----------   SAVE RESULTS    ----------")
    k.saveVtks(vtks)
    print("##########--------------------##########")
    print(f"- Your results can be found in {vtks} -")
    print("##########--------------------##########")