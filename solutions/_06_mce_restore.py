#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  name:        _06_mce_restore.py
#  purpose:     Demonstrate multiple criteria evaluation (MCE) to prioritize
#               lands to reforest/restore.
#
#  author:      Jeff Howarth
#  update:      05/08/2023
#  license:     Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# import tools from WBT module

import sys
sys.path.insert(1, '/Users/jhowarth/tools')     # path points to my WBT directory
from WBT.whitebox_tools import WhiteboxTools

# declare a name for the tools

wbt = WhiteboxTools()

#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Working directories
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Define personal storage root.
# This is the path where you will store inputs and outputs from this workflow.
# For example, my root points to the directory (folder) of s23 in GEOG0310 
# on an external drive named drosera. 

root = "/Volumes/drosera/GEOG0310/s23"

inputs = root+"/inputs/"
keeps = root+"/keeps/"
mce = root+"/mce/"

# Define MCE as the primary working directory.
# The weighted overlay tool takes a list of input files as a string. This does not
# play nicely with the scheme I have been used to distinguish different directories
# as variables. So I added the step below the uses the 'mce' folder as the working directory
# for all layers generated in this workflow. 

wbt.work_dir = mce

#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Required datasets:
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Point to directory where you hold input data. 
# All but the last one are available on the public Google starter drive.
# The last layer gets kicked out by the _04_select_valley_corridor.py script. 

lc = inputs+"LCHP_1m_midd.tif" 
rare = inputs+"rare_nc_binary_0504.tif"
nc = inputs+"NC_from_soils_simple.tif"
corridors = keeps+"_0426_valley_corridors_not_developed_blocks_gte_XX_acres.tif"

# ------------------------------------------------------------------------------
# Make mama and align rasters
# ------------------------------------------------------------------------------

# Resample LCHP to 3 meter to make mama. 

wbt.resample(
    inputs = lc, 
    output = "_0601_lc_mama.tif", 
    cell_size = 3, 
    base = None, 
    method = "nn"
)

# Resample rare natural communities to match mama. 

wbt.resample(
    inputs = rare, 
    output = "_0602_rare_resample.tif", 
    cell_size = None, 
    base = mce+"_0601_lc_mama.tif", 
    method = "nn"
)

# Resample nc from soils to match mama. 

wbt.resample(
    inputs = nc, 
    output = "_0603_nc_resample.tif", 
    cell_size = None, 
    base = mce+"_0601_lc_mama.tif", 
    method = "nn"
)

# Resample lowland connectors to match mama. I know this is up-sampling, but ok for now.  

wbt.resample(
    inputs = corridors, 
    output = "_0604_corridors_resample.tif", 
    cell_size = None, 
    base = mce+"_0601_lc_mama.tif", 
    method = "nn"
)

# ------------------------------------------------------------------------------
# Define suitability scores. 
# ------------------------------------------------------------------------------

# Define land cover suitability: 2 ideal, 1 pretty good, 0 not contributing, but not excluded

wbt.reclass(
    i = "_0601_lc_mama.tif", 
    output = "_0612_lc_suitability.tif", 
    reclass_vals = "0;1;10;2;0;3;5;4;10;5;0;6;0;7;0;8;0;9;0;10", 
    assign_mode=True
)

# Define distance to rare natural community as a cost (suitability decreases as distance increases).

wbt.euclidean_distance(
    i = "_0602_rare_resample.tif", 
    output = "_0613_rare_suitability.tif",
)

# Define suitability of natural community from soils: 2 ideal, 1 pretty good, 0 not contributing, but not excluded.

wbt.reclass(
    i = "_0603_nc_resample.tif", 
    output = "_0614_nc_suitability.tif", 
    reclass_vals = "2;1;2;2;0;3", 
    assign_mode=True
)

# ------------------------------------------------------------------------------
# Compare layers with a weighted overlay. 
# ------------------------------------------------------------------------------

# Whitebox can be prickly here. It doesn't like spaces in the weights or cost lists. 

wbt.weighted_overlay(
    factors = "_0612_lc_suitability.tif; _0613_rare_suitability.tif; _0614_nc_suitability.tif", 
    weights = "0.2;0.4;0.4",    # This says distance to rare and nc soils are more important than lc. 
    output = '_0623_mce_result.tif', 
    cost = 'false;true;false', 
    constraints = "_0604_corridors_resample.tif", 
    scale_max = 100.0,
)
