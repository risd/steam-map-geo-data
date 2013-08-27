# write out only district lines within state
# boundaries for use in TileMill

# for some reason, the shapely unary union
# is not merging the jams.

from os.path import abspath, dirname, join
from subprocess import call

import fiona
from fiona.crs import from_epsg

from shapely.geometry import mapping, shape
from shapely.ops import unary_union

import us

DEBUG = True

DATA_DIR = dirname(dirname(dirname(abspath(__file__))))

# districts
PATH_DISTRICT = join(DATA_DIR,
                     '00_data_original/' +
                     'districtShapes/' +
                     'districts112.shp')

# output district lines
PATH_DISTRICT_LINES = 'data/districts_dissolved.shp'

# open a collection to write to
with fiona.open(
        PATH_DISTRICT_LINES, 'w',
        crs=from_epsg(4326),
        driver='ESRI Shapefile',
        schema={
            'geometry': 'Polygon',
            'properties': {
                'uid': 'str'
            }
        }) as district_lines:

    states = {}

    with fiona.open(PATH_DISTRICT, 'r') as districts:
        count = 0
        try:
            for district in districts:
                state_abbr = us.states.lookup(
                    district['properties']['STATENAME']).abbr

                uid = '{0}_'.format(state_abbr) +\
                    '{0}'.format(district['properties']['DISTRICT'])

                print 'currently processing: ', uid

                if state_abbr not in (states.keys()):
                    # state is not already in here
                    states[state_abbr] = []
                    print 'created state ref: ', state_abbr

                states[state_abbr].append(shape(district['geometry']))

                count += 1
                if count > 5:
                    break

        except Exception, e:
            print 'error: {0}'.format(e)

    for state in states.keys():
        print state
        print states[state]
        if len(states[state]) > 1:
            union = unary_union(states[state])
            print union
            geom = mapping(union)
        else:
            geom = mapping(states[state][0])

        feature = {}
        feature['properties'] = {}
        feature['properties']['uid'] = 'word'

        feature['geometry'] = geom

        district_lines.write(feature)


geojson_cmd = 'ogr2ogr -f GeoJSON {0} '.format(PATH_DISTRICT_LINES
                                               .replace('.shp',
                                                        '.geojson')) +\
              '{0}'.format(PATH_LEVEL_1)
geojson_cmd = geojson_cmd.split(" ")

print 'writing ogr2ogr shp to geojson'
call(geojson_cmd)

# topojson -o level_1.topojson -p uid  -- level_1.geojson
