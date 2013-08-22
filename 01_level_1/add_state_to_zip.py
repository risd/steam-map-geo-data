# Get the centroid of each level 1 polygon

import fiona
from fiona.crs import from_epsg

# open a collection to write to
with fiona.open(
    'level_1.shp', 'w',
    crs=from_epsg(4326),
    driver='ESRI Shapefile',
    schema={
        'geometry': 'Polygon',
        'properties': {
            'zip_center_lat': 'float',
            'zip_center_lon': 'float',
        }
    }) as output:

    # read in data from zip shapefile
    print output.schema