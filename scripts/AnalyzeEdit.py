import os
import glob
import pandas as pd
import sys

def read_result(path, parameter):
    """
    Reads all the .csv files exported by paraview. Calculates the average value
    over the area. Gives back a pandas dataframe.

    Parameters
    ----------
    path : String
        Directory where the .csv files for all timesteps are. 
        They must be exported from paraview.
    parameter : String
        The Parameter which should be analyzed and plotted.

    Returns
    -------
    result : Dataframe
        A Pandas Dataframe with all timesteps in one dataframe.
        Includig a Field 'parameter_area' where the integrated values were
        divided by the area.

    """
    all_files = glob.glob(os.path.join(path, "*.csv")) # list of all .csv files in directory
    # read and concat all files within the directory in one dataframe
    result = pd.concat((pd.read_csv(f) for f in all_files), ignore_index=True)
    # calculate average over area
    result["parameter_area"] = result[f"{parameter}"] / result.Area
    return result

def add_index(path, parameter, index_file):
    """
    Using the 'read_result' function and adding a field ID and datetime to the 
    results. Therefore a .csv file is needed

    Parameters
    ----------
    path : String
        Directory where the .csv files for all timesteps are. 
        They must be exported from paraview.
    parameter : String
        The Parameter which should be analyzed and plotted.
    index_file : String
        Directory where the index file is located. It must be a .csv file without
        header and tapstop seperated. 3 columns with datetime, the ID (first active
        measurment = 1, before its NaN) and one column with 0 (ERT not active) or 
        1 (ERT active).

    Returns
    -------
    result_date : Dataframe
        A Pandas Dataframe same as from function 'read_results' containing the ID
        and Datetime.

    """
    # read and name index file
    active = pd.read_csv(index_file, sep="\t", header=None)
    active.columns = ["datetime", "ID", "active"]
    
    # extract all columns where measurment were active
    extraction = active[active.active==1]
    extraction.reset_index(drop=True, inplace=True)
    
    # read paraview results using 'read_result' function
    result = read_result(path=path, parameter=parameter)
    result.reset_index(drop=True, inplace=True)

    # check if index file and actual results have the same length of active ERTs
    if len(extraction) != len(result):
        raise IndexError("Different lengths of index_file and results \nCheck if there are as many active (=1) lines in index_file column 3 as result files")
        sys.exit()
    
    # concat datetime extraction to paraview results
    concat = pd.concat([extraction,result], axis=1)
    concat = concat.set_index("ID").drop("datetime", axis=1)

    # concat extraction with rest of index file to get the whole timerange
    active = active.set_index("ID").drop("active", axis=1)
    result_date = pd.concat([active, concat], axis=1)
    result_date = result_date.set_index("datetime")
    return result_date