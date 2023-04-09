## VT Conservation    

A collection of geographic data workflows for teaching and doing conservation planning using examples from Vermont, USA.   

### Practice  

The practice scripts outline workflows that you can implement with python and [WhiteboxTools Open Core][wb1]. The idea is that you learn by trying to fill in the blanks. For technical documentation on WhiteboxTools, please refer to the [WhiteboxTools manual][wb2]. To check your work, please refer to the solution for each problem.  

| Practice    | Description   | Solution  |
| :--       | :---          | :---:      |
| [_01p_simple_landforms.py][01p] | Classify landforms with geomorphons. | [01][01s] |
| [_02p_valley_bottoms.py][02p]   | Classify landforms with geomorphons, threshold to isolate valley bottoms, smooth with neighborhood majority filter. |  [02][02s]
| [_03p_forest_habitat_blocks][03p] | Classify forest habitat blocks. | [03][03s]

### Data repository  

You can access data for the practice scripts [here][data].  

| Dataset   | Description   | 
| :---      | :---          |
| DEM_10m_midd.tif  | 10m 3DEP for Middlebury, Vermont.  |
| LCHP_1m_midd.tif  | 1m Vermont Land Cover dataset with agriculture, roads, and building zones for Middlebury, Vermont. | 


To use this data in the practice scripts, you will need to:  

1. Create four sub-directories in a root directory on a drive as shown below. The three directories should be named:

    * inputs
    * keeps
    * projects 
    * temps 

![directory](assets/directory_.png) 

2. Download the required datasets and place them in the inputs folder.  

3. In the practice script, update the root variable so that it provides the path to your root folder. For example:  

```python
root = "/Volumes/drosera/GEOG0310/s23"
```

In the above example, the root variable points to the s23 folder in GEOG0310 on an external hardrive named drosera. 

### Solutions 

### Contact 

Jeff Howarth  
Associate Professor of Geography  
Middlebury College  


[data]: https://drive.google.com/drive/folders/1H_9ShSYgT1qYIMOfpEarzISFqd3OnGSu?usp=sharing

[wb1]: https://www.whiteboxgeo.com/geospatial-software/

[wb2]: https://www.whiteboxgeo.com/manual/wbt_book/available_tools/index.html

[01p]: practice/_01p_simple_landforms.py 
[01s]: solutions/_01s_simple_landforms.py

[02p]: practice/_02p_valley_bottoms.py
[02s]: solutions/_02s_valley_bottoms.py

[03p]: practice/_03p_forest_habitat_blocks.py
[03s]: solutions/_03s_forest_habitat_blocks.py
