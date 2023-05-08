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

# Define personal storage root: a path where to store inputs and outputs.
# In this example, the root points to a directory (folder) named s23 in GEOG0310 
# on an external drive named drosera. 

root = "/Volumes/drosera/GEOG0310/s23"

# These are the other folders referenced by the workflow. 

inputs = root+"/inputs/"
keeps = root+"/keeps/"
mce = root+"/mce/"

# Define mce as the primary working directory.
# The weighted overlay tool takes a list of input files as a string. This does not
# play nicely with the scheme that I have been using to distinguish different directories
# as variables. So I added the step below to define the 'mce' folder as the place to put
# all layers generated in this workflow. 

wbt.work_dir = mce

#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Required datasets
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# This stores inputs as variables to make updates easier in the future. 
# All but the last one are currently available on the public Google starter drive.
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
    reclass_vals = "2;1;2;2;0;3;1;4;2;5;0;6;0;7;0;8;0;9;0;10", 
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

# ------------------------------------------------------------------------------
# Mask land outside of the region of interest (Town of Middlebury)
# ------------------------------------------------------------------------------

# Make binary of land in region of interest. 

wbt.not_equal_to(
    input1 = "_0603_nc_resample.tif", 
    input2 = 0, 
    output = "_0631_roi.tif"
)

# Mask locations outside of roi.

wbt.set_nodata_value(
    i = "_0631_roi.tif", 
    output = "_0632_roi_mask.tif", 
    back_value=0.0, 
)


# Apply mask to mce results.

wbt.multiply(
    input1 = "_0632_roi_mask.tif", 
    input2 = '_0623_mce_result.tif', 
    output = "_0633_mce_results_in_roi.tif", 
)
