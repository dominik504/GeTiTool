#####
# BETAVERSION
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

## Examples
Here it is shown how to use the current possible Features of the Tool.
### getitool
As positional argument you need your raw Geotom Data. If you use the -t flag to include a Topography file you 
also need to use the -s flag to give the spacing. The -e flag can be used to give the absolute Height above Sealevel
of the first Electrode. The -r flag can be used to set any iteration settings possible by resipy. In the example
below the maximum of iterations was set on 2 iterations to minimize the calculation time.


```
getitool C:\Users\path\to\your\raw\data
-t C:\Users\path\to\your\measured\angles\data\angles_raw.csv 
-s 0.5 
-e 2995
-r max_iter,2
```

```
Authors Example
getitool C:\Users\domin\OneDrive\Desktop\masterarbeit\TimelapseTool\testdaten  -t C:\Users\domin\OneDrive\Desktop\masterarbeit\Tanneben\angles_raw.csv  -s 0.5  -e 720.1 -r max_iter,2
```

### getianalyze
As positional argument you need the path to your integrated csv files computed by paraview. With -p you can set 
the parameter that should be plotted, included in the csv files before. -a divides the integrated values by the
area to get an averaged value. -i gives the location to your file which gives the time when the measurment was active
and which datetime this measurement had. -m can be used to define the index from where and to where it should be plotted.
-s can be used to save the figure in the folder given as positional argument, otherwise it will just be shown.

```
getianalyze C:\Users\path\to\your\integrated\data
-p Resistivity(ohm.m)
-a 
-i C:\Users\path\to\your\aktive\measurments\data\ERT_aktiv.csv 
```

```
Authors example:
getianalyze C:\Users\domin\OneDrive\Desktop\masterarbeit\Tanneben\20220705_Daten\messung1_teil1_2_3_4_5\ergebnisse_teil1_2_3\slices -p Resistivity(ohm.m) -a -i C:/Users/domin/OneDrive/Desktop/masterarbeit/Tanneben/ERT_aktiv.csv
```

## Parameters that can be set with Resipy
### Including their default parameters
#### See also: https://gitlab.com/hkex/resipy/-/issues/460 and the resipy gitlab page

'lineTitle':'My beautiful survey',
'job_type':1,
'mesh_type':6, # meshx, meshy, topo should be defined
'flux_type':3,
'singular_type':0,
'res_matrix':1,
'scale':1, # only used for triangular mesh
'num_regions':1,
'regions':None, # should be defined by the number of element in the mesh
'patch_x':1,
'patch_z':1,
'inverse_type':1,
'target_decrease':0,
'qual_ratio':0,
'data_type':1,
'reg_mode':0,
'tolerance':1,
'max_iter':10,
'error_mod':2,
'alpha_aniso':1,
'alpha_s':10, # penalizing from starting model
'min_error':0.01, # for IP only
'a_wgt':0.01, # 0.02 for IP
'b_wgt':0.02, # 2 for IP
'rho_min':-1e10,
'rho_max':1e10,
'num_xz_poly':-1,
'xz_poly_table':np.zeros((5,2)),
'num_elec':None, #should be define when importing data
'elec_node':None # should be define when building the mesh

