#####
# BETAVERSION
# TEST
#####

# GeTiTool

A Tool to calculate geoelectrical timelapse, taking the raw data and topography as input and giving calculated vtk Files as output.

It provides the following shell script: `getitool`.
For usage information, type `getitool --help`.

## Installation

Use the following command in the base directory to install:

```bash
python -m pip install .
```

## Prerequisites

You need a working Python environment, and `pip` installed.
It is importand to have a python version between 3.6 and 3.8, otherwise resipy will not work.
E.g., with `conda`:

```bash
conda create --name mynewenv python=3.8
conda activate mynewenv
python -m pip install -e .
```

## Example

```
getitool C:\Users\path\to\your\raw\data
-t C:\Users\path\to\your\measured\angles\data\angles_raw.csv 
-s 0.5 
-i 2
```

```
getitool C:\Users\domin\OneDrive\Desktop\masterarbeit\resipyTrial\data  -t C:\Users\domin\OneDrive\Desktop\masterarbeit\Tanneben\angles_raw.csv  -s 0.5  -i 2
```