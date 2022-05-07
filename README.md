# erosion_risk
EGM722 assessment project

The script and all required files are publicly available on https://github.com/MARCOOTTO-GIS/erosion_risk. The environment.yml file can be used to obtain any dependencies that are required and the channels from where a download is possible, which are as follows:

channels:
 	 - conda-forge
  	- defaults
dependencies:
  	- python=3.9
  	- numpy
  	- geopandas
 	 - cartopy
  	- matplotlib
	- rasterio
	- pycrs
  	- os
	- pathlib

The dependencies should be added into an appropriately named condo environment, such as soil_erosion.
The folder ‘project’ located in above repository contains the actual script both as a Python script and as a Jupyter Notebook. These should be saved locally and within that folder a new subfolder should be created called ‘files’. This subfolder is where the script will attempt to read the raster and vector files required for it, and where it will also attempt to save the newly created raster files. Test data is available in the repository within the subfolder of that name as well.

The data structure should thus be as follows and include the following files:
…/erosion_risk.py
…/erosion_risk.ipynb
…/files/soil.tif
…/files/rainfall.tif
…/files/landcover.tif
…/files/slope.tif
…/files/research_area.shp
…/files/research_area.dbf
…/files/research_area.shx

Further files that are part of the shapefile but not strictly necessary for its function are recommended to be downloaded into the same folder ‘files’ folder as well and are provided too. The files must be in the correct folder and be named correctly as listed above, otherwise the script’s execution will be terminated with an appropriate error message.

If own test data is used, then the above naming and folder conventions must be adhered to, and there are several restrictions:
•	Pixel sizes and locations must be identical for all raster images
•	Each file must have a coordinate reference system assigned to it
•	All files must use the same coordinate reference system
•	Values for rainfall.tif need to show yearly precipitation in millimetres
•	Values for slope.tif need to show the slope in percent
•	Values for soil.tif need to be integers between 1 (highest risk) and 4 (lowest risk)
•	Values for landcover.tif need to be integers between 0 (lowest risk) and 4 (highest risk)
