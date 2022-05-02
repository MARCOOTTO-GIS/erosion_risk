import numpy as np
import rasterio as rio
import geopandas as gpd
import cartopy.crs as ccrs
from cartopy.feature import ShapelyFeature
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
from pathlib import Path

# optional work to be added: input for user specifying file names and/or explaining file import restrictions

# script assumes that raster imagery is prepared with identical resolution, as in identical cell size
paths = ('files/soil.tif','files/rainfall.tif','files/landcover.tif','files/slope.tif','files/research_area.shp',
		 'files/research_area.dbf','files/research_area.shx')
		# 'files/research_area.cpg','files/research_area.prj','files/research_area.sbn','files/research_area.shp.xml',
		# 'files/research_area.sbx' these are optional parts of the shapefiles, consider adding checks
        # checking file locations of tif files and all files typically belonging to a shapefile to confirm that they exist

for path in paths:
	p = Path(path)
	if p.exists():
		print(path + ' loaded successfully.')
	else:
		print('One or more files in incorrect location or not named correctly, please review README for instructions.')
		quit()

research_area = gpd.read_file('files/research_area.shp') # assigning research shapefile to variable using geopandas
soil = rio.open('files/soil.tif')
rainfall = rio.open('files/rainfall.tif')
landcover = rio.open('files/landcover.tif')
slope = rio.open('files/slope.tif') # assigning raster files of soil erosion risk factors to variables using rasterio

if research_area.crs != None:
	crs = research_area.crs # variable crs is assigned the CRS from the research_area shapefile if it has one
else:
	print('No Coordinate Reference System found in Research Area Shapefile, please check README')
	quit()	# if the research_area shapefile does not have a CRS, then the script will print an error and exit

# consider adding user input for CRS if research_area does not have one

print(crs)