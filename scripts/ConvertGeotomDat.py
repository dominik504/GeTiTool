import os
import sys

def dat_conversion(filename, export_name, header_length, columns):
    """
    Takes the values from the raw file (e.g. '.wen') and converts it to a 
    .dat file with the format used from the RES2DInv program.

    Parameters
    ----------
    filename : String
        Filname and directory that should be converted.
    export_name : String
        Filename and directory where it should be saved.
    header_length : Integer
        Number of lines the header has.
    columns : Integer
        Number of columns to export, this should be all columns with data before
        the ';' and usually is 3 or 4.

    """
    datfile = []  # empty list for data
    # Define the line where blocks end (start counting with 0):
    header_begin = 10
    header_end = header_begin + header_length - 1
    data_length = columns * 10 - 1

    # Define Data End
    with open(filename) as inputfile:
        for i, line in enumerate(inputfile):
            data_end = sum(1 for line in inputfile) - 4

    # carry out conversion
    with open(filename) as inputfile:
        for i, line in enumerate(inputfile):
            # append the needed lines
            if i >= header_begin and i <= header_end:
                datfile.append(line[:-1])
            elif i >= header_end + 1 and i <= data_end:
                datfile.append(line[0:data_length])
            elif i >= data_end + 1:
                datfile.append(line[:-1])

        with open(export_name, "w") as file:
            for row in datfile:
                s = "".join(map(str, row))
                file.write(s + "\n")

def geotom_to_dat(directory, file_ending=".wen", header_length=6, columns=3):
    """
    Saves all files within the given directory, with the defined ending in a 
    new folder. The function basically loops over all files in the folder and
    uses the filenames as input for the function 'dat_conversion'.

    Parameters
    ----------
    directory : String
        Folder where the raw data is.
    file_ending : String, optional
        The ending of the files whicht should be converted. 
        The default is ".wen".
    header_length : Int, optional
        Number of lines the header has. The default is 6.
    columns : TYPE, optional
        Number of columns to export, this should be all columns with data before
        the ';' and usually is 3 or 4. The default is 3.
    
    Raises
    ------
    FileNotFoundError
        If the Folder 'datfiles' were not created before, this would lead to 
        an error.
    """

    output = directory + "/datfiles/"
    if not os.path.exists(output):
        raise FileNotFoundError("There may be no Subfolder 'datfiles' in your directroy")
        sys.exit()
        
    for files in os.listdir(directory):
        if files.endswith(file_ending):
            dat_conversion(
                filename=directory + "/" + files,
                export_name=directory
                + "/datfiles/"
                + (os.path.splitext(files)[0])
                + ".dat",
                header_length=header_length,
                columns=columns,
            )