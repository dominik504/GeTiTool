import os

def dat_conversion(filename, export_name, header_length, columns):
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
    """saves all files within the given directory,
    with the defined ending in a new folder"""

    output = directory + "/datfiles/"
    if not os.path.exists(output):
        os.makedirs(output)
        
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