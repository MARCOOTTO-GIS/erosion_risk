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
from rasterio.plot import show
from rasterio.plot import show_hist
from rasterio.mask import mask
from shapely.geometry import box
from fiona.crs import from_epsg
import pycrs
import os

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
	cooref = research_area.crs # variable cooref is assigned the CRS from the research_area shapefile if it has one
	print('CRS used for project: ' + str(research_area.crs))

else:
	print('No Coordinate Reference System found in Research Area Shapefile, please check README')
	quit()	# if the research_area shapefile does not have a CRS, then the script will print an error and exit

# consider adding user input for CRS if research_area does not have one

# code for clipping adapted from https://automating-gis-processes.github.io/CSC18/lessons/L6/clipping-raster.html
def getFeatures(gdf):
    #Function to transform research area shapefile into coordinates that rasterio can use
    import json
    return [json.loads(gdf.to_json())['features'][0]['geometry']]

clip_coords = getFeatures(research_area) # boundary of research_area assigned as coordinates to clip_coords

with rio.open('files/soil.tif') as dataset1:
	if dataset1.crs == cooref: # script only continues when crs for research_area and soil.tif are identical
		out_img, out_transform = mask(dataset=dataset1, shapes=clip_coords, crop=True) # cropping image to research_area
		out_meta = dataset1.meta.copy() # copying original image meta data
		epsg_code = int(dataset1.crs.data['init'][5:]) # reading CRS data from original image
		out_meta.update({"driver": "GTiff",
						 "height": out_img.shape[1],
						 "width": out_img.shape[2],
						 "transform": out_transform,
						 "crs": pycrs.parse.from_epsg_code(epsg_code).to_proj4()}) # updating meta data for new cropped image
		if os.path.exists('files/soil_clip.tif'):
			os.remove('files/soil_clip.tif') # deletes clipped file if it exists so that script can be run repeatedly
			with rasterio.open('files/soil_clip.tif', "w", **out_meta) as soil_clip:
				soil_clip.write(out_img) # output of clipped image with updated meta data
				soil = soil_clip
			print('Old soil_clip.tif has been replaced')
		else:
			with rasterio.open('files/soil_clip.tif', "w", **out_meta) as soil_clip:
				soil_clip.write(out_img) # output of clipped image with updated meta data
				rainfall = soil_clip # assigning clipped image to variable
		#xmin, ymin, xmax, ymax = dataset1.bounds

	else:
		print('Coordinate Reference System for soil.tif not identical to Research Area CRS')
		quit()

with rio.open('files/rainfall.tif') as dataset2:
	if dataset2.crs == cooref: # script only continues when crs for research_area and rainfall.tif are identical
		out_img, out_transform = mask(dataset=dataset2, shapes=clip_coords, crop=True)
		out_meta = dataset2.meta.copy()
		epsg_code = int(dataset2.crs.data['init'][5:])
		out_meta.update({"driver": "GTiff",
						 "height": out_img.shape[1],
						 "width": out_img.shape[2],
						 "transform": out_transform,
						 "crs": pycrs.parse.from_epsg_code(epsg_code).to_proj4()})
		if os.path.exists('files/rainfall_clip.tif'):
			os.remove('files/rainfall_clip.tif') # deletes clipped file if it exists so that script can be run repeatedly
			with rasterio.open('files/rainfall_clip.tif', "w", **out_meta) as rainfall_clip:
				rainfall_clip.write(out_img) # output of clipped image with updated meta data
				rainfall = rainfall_clip
			print('Old rainfall_clip.tif has been replaced')
		else:
			with rasterio.open('files/rainfall_clip.tif', "w", **out_meta) as rainfall_clip:
				rainfall_clip.write(out_img) # output of clipped image with updated meta data
				rainfall = rainfall_clip # assigning clipped image to variable
		#xmin, ymin, xmax, ymax = dataset2.bounds
	else:
		print('Coordinate Reference System for rainfall.tif not identical to Research Area CRS')
		quit()

with rio.open('files/landcover.tif') as dataset3:
	if dataset3.crs == cooref:  # script only continues when crs for research_area and landcover.tif are identical
		out_img, out_transform = mask(dataset=dataset3, shapes=clip_coords, crop=True)
		out_meta = dataset3.meta.copy()
		epsg_code = int(dataset3.crs.data['init'][5:])
		out_meta.update({"driver": "GTiff",
						 "height": out_img.shape[1],
						 "width": out_img.shape[2],
						 "transform": out_transform,
						 "crs": pycrs.parse.from_epsg_code(epsg_code).to_proj4()})
		if os.path.exists('files/landcover_clip.tif'):
			os.remove('files/landcover_clip.tif') # deletes clipped file if it exists so that script can be run repeatedly
			with rasterio.open('files/landcover_clip.tif', "w", **out_meta) as landcover_clip:
				landcover_clip.write(out_img) # output of clipped image with updated meta data
				landcover = landcover_clip
			print('Old landcover_clip.tif has been replaced')
		else:
			with rasterio.open('files/landcover_clip.tif', "w", **out_meta) as landcover_clip:
				landcover_clip.write(out_img) # output of clipped image with updated meta data
				landcover = landcover_clip # assigning clipped image to variable
		#xmin, ymin, xmax, ymax = dataset3.bounds
	else:
		print('Coordinate Reference System for landcover.tif not identical to Research Area CRS')
		quit()

with rio.open('files/slope.tif') as dataset4:
	if dataset4.crs == cooref:  # script only continues when crs for research_area and slope.tif are identical
		out_img, out_transform = mask(dataset=dataset4, shapes=clip_coords, crop=True)
		out_meta = dataset4.meta.copy()
		epsg_code = int(dataset4.crs.data['init'][5:])
		out_meta.update({"driver": "GTiff",
						 "height": out_img.shape[1],
						 "width": out_img.shape[2],
						 "transform": out_transform,
						 "crs": pycrs.parse.from_epsg_code(epsg_code).to_proj4()})
		if os.path.exists('files/slope_clip.tif'):
			os.remove('files/slope_clip.tif') # deletes clipped file if it exists so that script can be run repeatedly
			with rasterio.open('files/slope_clip.tif', "w", **out_meta) as slope_clip:
				slope_clip.write(out_img) # output of clipped image with updated meta data
				slope = slope_clip
			print('Old slope_clip.tif has been replaced')
		else:
			with rasterio.open('files/slope_clip.tif', "w", **out_meta) as slope_clip:
				slope_clip.write(out_img) # output of clipped image with updated meta data
				slope = slope_clip # assigning clipped image to variable
		#xmin, ymin, xmax, ymax = dataset2.bounds
	else:
		print('Coordinate Reference System for slope.tif not identical to Research Area CRS')
		quit()



# the following code works, but had to be deprecated due to HOW it works: the CRS of the research_area is applied
# to an existing tif file, creating a transformed new tif, however due to the transformation the cell/pixel
# size may be changed slightly. This would, without work that was not able to be completed, prevent a raster
# calculation to work correctly, as the pixels no longer overlay correctly. Instead, the script will stop with
# an error message if the CRS of one of the files does not match the research_area CRS.
'''
dst_crs = cooref  # destination CRS is based on the previously assigned CRS of the research_area,
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