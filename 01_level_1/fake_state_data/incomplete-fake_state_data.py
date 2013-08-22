# Create fake data at the center of every state

from os.path import abspath, dirname, join
from os import remove
import random

import fiona
from fiona.crs import from_epsg

from shapely.geometry import MultiPolygon, Polygon, Point


def return_coords(coords):
    if len(coords) == 1:
        return return_coords(coords[0])
    else:
        return coords

def centroid(geom):
    print '\ngetting centroid:\n{0}\n\n'.format(geom)

    if geom['type'] == 'MultiPolygon':
        multi_coordinates = []
        for poly in geom['coordinates']:
            multi_coordinates.append(return_coords(poly))

        print '\nmulti_coordinates:\n{0}\n\n'.format(multi_coordinates)

        try:
            p = MultiPolygon(multi_coordinates)
        except Exception:
            print 'not a multipolygon'

    elif geom['type'] == 'Polygon':
        coordinates = return_coords(geom['coordinates'])
        try:
            p = Polygon(coordinates)
        except Exception:
            print 'not a polygon either'
            exit()

    print '\npolygon\n{0}\n\n'.format(p)
    print list(p.centroid.coords)[0]

    return list(p.centroid.coords)[0]


IN_PATH = join(dirname(abspath(__file__)), 'us-states.geojson')
OUT_PATH = join(dirname(abspath(__file__)), 'fake-steam-state.geojson')

try:
    with open(OUT_PATH):
        pass
    remove(OUT_PATH)
    print 'Ready to start. Existing file deleted'
except IOError:
    print 'Ready to start. No file to delete.'

# open a collection to write to
with fiona.open(
        'us-states.geojson',
        crs=from_epsg(4326),
        driver='GeoJSON') as states_in:

    # read in data from zip shapefile
    print 'states in schema: \n{0}\n\n'.format(states_in.schema)

    with fiona.open(
            'fake-steam-state.geojson', 'w',
            crs=from_epsg(4326),
            driver='GeoJSON',
            schema={
                'geometry': 'Point',
                'properties': {
                    'level_1_postal': 'str',
                    'level_1_us_bool': 'int',
                    'level_1_work_in_edu': 'int',
                    'level_1_work_in_research': 'int',
                    'level_1_work_in_policy': 'int',
                    'level_1_work_in_industry': 'int'
                }
            }) as states_out:

        # read in data from zip shapefile
        print 'states out schema: \n{0}\n\n'.format(states_out.schema)

        try:
            # loop through all in states
            for f_in in states_in:
                f_out = {}
                f_out['geometry'] = {}
                f_out['properties'] = {}

                f_out['geometry']['type'] = 'Point'

                f_out['geometry']['coordinates'] = \
                    centroid(f_in['geometry'])

                f_out['properties']['level_1_postal'] = \
                    f_in['properties']['postal']

                f_out['properties']['level_1_us_bool'] = 1

                f_out['properties']['level_1_work_in_edu'] = \
                    random.randrange(50, 500)

                f_out['properties']['level_1_work_in_policy'] = \
                    random.randrange(50, 500)

                f_out['properties']['level_1_work_in_research'] = \
                    random.randrange(50, 500)

                f_out['properties']['level_1_work_in_industry'] = \
                    random.randrange(50, 500)

                states_out.write(f_out)

        except Exception, e:
            print 'error'
