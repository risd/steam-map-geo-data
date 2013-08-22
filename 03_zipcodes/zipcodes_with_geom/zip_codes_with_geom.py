# import logging
# from os.path import abspath, dirname, join
# import sys

# from shapely.geometry import mapping, shape

# import fiona


# ZIP_SHP_PATH = join(dirname(dirname(abspath(__file__))),
#                     'tl_2012_us_zcta510/tl_2012_us_zcta510.shp')



# with fiona.open(ZIP_SHP_PATH, 'r') as in_zip:

#     with fiona.open(
# 	    	'zip_codes_by_state.shp',
# 	    	schema={
# 	    		'geometry': 'MultiPolygon'
# 	    	})