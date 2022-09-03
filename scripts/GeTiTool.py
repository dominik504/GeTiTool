from resipy import Project
import pandas as pd

from . import ConvertGeotomDat
from . import CalculateTopography

# import ConvertGeotomDat
# import CalculateTopography

import warnings
warnings.filterwarnings('ignore')

def GeTiToolCalc(raw_data, topo, spacing, iterations, vtks):
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

    """
    # convert .wen Data to .dat Data
    ConvertGeotomDat.geotom_to_dat(directory=raw_data, file_ending=".wen", header_length=6, columns=3)
    datfiles = raw_data + "/datfiles/"
    
    # creating resipy object by using Project()
    k = Project(typ="R2")
    
    # define timelapse input from folder
    k.createTimeLapseSurvey(dirname=datfiles, ftype="ResInv")
    if topo != None:
        # calculating electrode topography
        electrodes = CalculateTopography.calculateTopography(file=topo, spacing=spacing, interpolate=True)
        electrodes["y"] = 0 # spaceholder, could be used for absolute coordinates later
        
            
        ## HARDCODED CHANGE!!!!
        # add x and y absolute coordinates
        # y = pd.read_csv("C:/Users/domin/OneDrive/Desktop/masterarbeit/Tanneben/Messung1/ungenau_Elektroden/y.txt", header=None)
        # electrodes.y = y
        # x = pd.read_csv("C:/Users/domin/OneDrive/Desktop/masterarbeit/Tanneben/Messung1/ungenau_Elektroden/x.txt", header=None)
        # electrodes.x = x
        electrodes.z = electrodes.z + 720.12
        
        # save csv topo and only keep xyz data (others are available- see the function)
        electrodes[["x", "y", "z"]].to_csv(raw_data + "/files/topo.csv", sep=",", index=False)
        k.importElec(raw_data + "/files/topo.csv") # get electrode topo from file
    
        # creating mesh
        depth = round(len(electrodes)/4)  # depth below first electrode
        # k.elec.z = electrodes.z #!!! should not me necesarry - done 4 lines up
    
        #  fmd is depth to be calculated, cl_factor reduces size in lower region --> faster calculation
        k.createMesh(fmd=depth, typ="trian", cl_factor=10)
    else:
        #  fmd is depth to be calculated, cl_factor reduces size in lower region --> faster calculation
        k.createMesh(typ="trian", cl_factor=10)
    
    k.showMesh()
    # define inversion settings
    k.param["max_iter"] = iterations
    # inverting the data
    k.invert(parallel=True)
    
    # save vtks
    k.saveVtks(vtks)
    # return k