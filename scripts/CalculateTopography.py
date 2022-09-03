import pandas as pd 
import numpy as np

def calculateTopography(file, spacing, unit="degree", interpolate=False, delimiter=";"):
    """
    

    Parameters
    ----------
    file : String
        String to the file with angles. 
        File only containing angles als floats without header.
    spacing : Int/Float
        Spacing of the Electrodes used in the field.
    unit : String, optional
        Gives the unit in which the angles were measured
        So far only degree and radians can be handled. 
        The default is "degree".

    Returns
    -------
    electrodes_df : Dataframe
        Pandas Dataframe with 4 columns:
            x: The spacing as given by user
            x_real: The horizontal distance between two electrodes
            z: The z values
            angles: The angles as given by user

    """
    # create frame and read data
    electrodes_df = pd.read_csv(file, header=None, delimiter="\t")  # read measurements
    electrodes_df.columns = ["id", "angles"]
    electrodes_df["x"] = electrodes_df.index * spacing  # create x column
    
    if interpolate == True:
        electrodes_df.angles = electrodes_df.angles.interpolate()

    # calculate measured angles to radians
    if unit == "degree":
        # make radians if necesarry
        electrodes_df["radians"] = np.deg2rad(electrodes_df.angles)
    elif unit == "radians":
        electrodes_df["radians"] = electrodes_df.angles
    else:
        print("Can only handle degree and radians so far")
        print("Exiting Function now")
        return
    
    # calculate height difference (will be deleted later)
    electrodes_df["height_diff"] = np.sin(electrodes_df.radians)*spacing

    # calculate real x position and z
    for i in range(len(electrodes_df)):
        if i == 0:  # zero for the first row
            electrodes_df.loc[i, "x_real"] = 0
            electrodes_df.loc[i, "z"] = 0
        else:  # next lines (adding value of row before)
            electrodes_df.x_real.loc[i] = np.sqrt(
                spacing**2 - (electrodes_df.height_diff.loc[i])**2) + electrodes_df.x_real.loc[i-1]
            electrodes_df.z.loc[i] = electrodes_df.height_diff.loc[i] + \
                electrodes_df.z.loc[i-1]

    # only keep usefull columns
    electrodes_df = electrodes_df[["x", "x_real", "z", "angles"]]
    return electrodes_df

# make this if you want to use the function by itself:

# file = "C:/Users/domin/OneDrive/Desktop/masterarbeit/Tanneben/angles_raw.csv"
# df = calculateTopography(spacing=0.5, file=file, interpolate=True)  # execute function
# df  # show data if needed


