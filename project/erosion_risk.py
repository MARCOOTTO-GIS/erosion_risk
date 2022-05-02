import numpy as np
import rasterio as rio
import geopandas as gpd
import cartopy.crs as ccrs
from cartopy.feature import ShapelyFeature
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
from pathlib import Path
import rasterio.warp

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

if research_area.crs != None:
	crs = research_area.crs # variable crs is assigned the CRS from the research_area shapefile if it has one
else:
	print('No Coordinate Reference System found in Research Area Shapefile, please check README')
	quit()	# if the research_area shapefile does not have a CRS, then the script will print an error and exit

# consider adding user input for CRS if research_area does not have one

with rio.open('files/soil.tif') as dataset1:
	if dataset1.crs == crs: # script only continues when crs for research_area and soil.tif are identical
		soil = dataset1.read()
		xmin, ymin, xmax, ymax = dataset1.bounds
	else:
		print('Coordinate Reference System for soil.tif not identical to Research Area CRS')
		quit()

with rio.open('files/rainfall.tif') as dataset2:
	if dataset2.crs == crs: # script only continues when crs for research_area and rainfall.tif are identical
		rainfall = dataset2.read()
		xmin, ymin, xmax, ymax = dataset2.bounds
	else:
		print('Coordinate Reference System for rainfall.tif not identical to Research Area CRS')
		quit()

with rio.open('files/landcover.tif') as dataset3:
	if dataset3.crs == crs:  # script only continues when crs for research_area and landcover.tif are identical
		landcover = dataset3.read()
		xmin, ymin, xmax, ymax = dataset2.bounds
	else:
		print('Coordinate Reference System for landcover.tif not identical to Research Area CRS')
		quit()

with rio.open('files/slope.tif') as dataset4:
	if dataset4.crs == crs:  # script only continues when crs for research_area and slope.tif are identical
		slope = dataset4.read()
		xmin, ymin, xmax, ymax = dataset2.bounds
	else:
		print('Coordinate Reference System for slope.tif not identical to Research Area CRS')
		quit()

print(research_area.crs)

# the following code works, but had to be deprecated due to HOW it works: the CRS of the research_area is applied
# to an existing tif file, creating a transformed new tif, however due to the transformation the cell/pixel
# size may be changed slightly. This would, without work that was not able to be completed, prevent a raster
# calculation to work correctly, as the pixels no longer overlay correctly. Instead, the script will stop with
# an error message if the CRS of one of the files does not match the research_area CRS.
'''
dst_crs = crs  # destination CRS is based on the previously assigned CRS of the research_area,
			   # following script adapted from https://rasterio.readthedocs.io/en/latest/topics/reproject.html

with rio.open('files/soil.tif') as src:
	transform, width, height = rio.warp.calculate_default_transform(
		src.crs, dst_crs, src.width, src.height, *src.bounds)
	kwargs = src.meta.copy()  # this copies the meta dict object
	kwargs.update({
		'crs': dst_crs,
		'transform': transform,
		'width': width,
		'height': height
	})

	with rio.open('files/soil_updated.tif', 'w', **kwargs) as dst:
		for i in range(1, src.count + 1):
			rio.warp.reproject(
				source=rio.band(src, i),
				destination=rio.band(dst, i),
				src_transform=src.transform,
				src_crs=src.crs,
				dst_transform=transform,
				dst_crs=dst_crs,
				resampling=rio.warp.Resampling.nearest)
'''