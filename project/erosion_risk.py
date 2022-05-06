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
	print('CRS used for project: ' + str(research_area.crs)+'.')

else:
	print('No Coordinate Reference System found in Research Area Shapefile, please check README.')
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
		ra_meta = out_meta  # ra_meta as variable to be used later outside this if statement
		if os.path.exists('files/soil_clip.tif'):
			os.remove('files/soil_clip.tif') # deletes clipped file if it exists so that script can be run repeatedly
			with rasterio.open('files/soil_clip.tif', "w", **out_meta) as soil_clip:
				soil_clip.write(out_img) # output of clipped image with updated meta data
				print('Old soil_clip.tif has been replaced.')
		else:
			with rasterio.open('files/soil_clip.tif', "w", **out_meta) as soil_clip:
				soil_clip.write(out_img) # output of clipped image with updated meta data
				print('soil_clip.tif has been created.')
		with rasterio.open('files/soil_clip.tif') as clipped_soil: # necessary as the previously opened clipped tifs were
			soil = clipped_soil.read()							   # opened in write mode, preventing rasterio from reading
																   # assigning clipped tif to variable as numpy array

	else:
		print('Coordinate Reference System for soil.tif not identical to Research Area CRS.')
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
				print('Old rainfall_clip.tif has been replaced.')
		else:
			with rasterio.open('files/rainfall_clip.tif', "w", **out_meta) as rainfall_clip:
				rainfall_clip.write(out_img) # output of clipped image with updated meta data
				print('rainfall_clip.tif has been created.')
		with rasterio.open('files/rainfall_clip.tif') as clipped_rainfall: # necessary as the previously opened clipped tifs were
			rainfall = clipped_rainfall.read()  					# opened in write mode, preventing rasterio from reading
																	# assigning clipped tif to variable as numpy array
	else:
		print('Coordinate Reference System for rainfall.tif not identical to Research Area CRS.')
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
			print('Old landcover_clip.tif has been replaced.')
		else:
			with rasterio.open('files/landcover_clip.tif', "w", **out_meta) as landcover_clip:
				landcover_clip.write(out_img) # output of clipped image with updated meta data
				print('landcover_clip.tif has been created.')
		with rasterio.open('files/landcover_clip.tif') as clipped_landcover: # necessary as the previously opened clipped tifs were
			landcover = clipped_landcover.read()  	# opened in write mode, preventing rasterio from reading
													# assigning clipped tif to variable as numpy array
	else:
		print('Coordinate Reference System for landcover.tif not identical to Research Area CRS.')
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
			print('Old slope_clip.tif has been replaced.')
		else:
			with rasterio.open('files/slope_clip.tif', "w", **out_meta) as slope_clip:
				slope_clip.write(out_img) # output of clipped image with updated meta data
				print('slope_clip.tif has been created.')
		with rasterio.open('files/slope_clip.tif') as clipped_slope: # necessary as the previously opened clipped tifs were
			slope = clipped_slope.read()  							 # opened in write mode, preventing rasterio from reading
																	 # assigning clipped tif to variable as numpy array
	else:
		print('Coordinate Reference System for slope.tif not identical to Research Area CRS.')
		quit()



# the following code works, but had to be deprecated due to HOW it works: the CRS of the research_area is applied
# to an existing tif file, creating a transformed new tif, however due to the transformation the cell/pixel
# size may be changed slightly. This would, without work that was not able to be completed, prevent a raster
# calculation to work correctly, as the pixels no longer overlay correctly. Instead, the script will stop with
# an error message if the CRS of one of the files does not match the research_area CRS. Leaving for future use.
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
print('Data types: soil: '+ str(type(soil)) + ' , rainfall: ' + str(type(rainfall)) + ' , landcover: '
	  + str(type(landcover)) + ', slope: ' + str(type(slope))) # visual check that each variable is assigned a numpy array

#np.seterr(divide='ignore', invalid='ignore') # allowing numpy division by zero or invalid parameters

# calculations combining risk factors soil, slope and rainfall as follows, an error will appear if one or more of the
# tifs cover a smaller extent than the research area. Consider adding check by comparing width and height of clipped tifs.
very_high = ((soil == 1) & (slope > 7) & (rainfall >= 800))
high = ((soil == 1) & (slope >= 3) & (slope <= 7) & (rainfall >= 800)) | \
	   ((soil == 2) & (slope > 7) & (rainfall >= 800)) | \
	   ((soil == 1) & (slope > 7) & (rainfall < 800))
moderate = ((soil == 1) & (slope >= 3) & (slope <= 7) & (rainfall < 800)) | \
		   ((soil == 1) & (slope >= 2) & (slope <= 3) & (rainfall >= 800)) | \
		   ((soil == 2) & (slope > 7) & (rainfall < 800)) | \
		   ((soil == 2) & (slope >= 3) & (slope <= 7) & (rainfall >= 800))
lower = ((soil == 1) & (slope >= 2) & (slope <= 3) & (rainfall < 800)) | \
		((soil == 2) & (slope >= 2) & (slope <= 3) & (rainfall >= 800)) | \
		((soil == 3) & (slope > 7) & (rainfall >= 800))
slight = (soil == 4) | \
		 ((soil == 1) & (slope < 2) & (rainfall >= 800)) | \
		 ((soil == 2) & (slope < 2) & (rainfall >= 800)) | \
		 ((soil == 3) & (slope >= 3) & (slope <= 7) & (rainfall >= 800)) | \
		 ((soil == 3) & (slope >= 2) & (slope <= 3) & (rainfall >= 800)) | \
		 ((soil == 3) & (slope < 2) & (rainfall >= 800))

'''
with rasterio.open('files/high.tif', "w", **ra_meta) as high_risk:
	high_risk.write(high)  # output of clipped image with updated meta data
'''