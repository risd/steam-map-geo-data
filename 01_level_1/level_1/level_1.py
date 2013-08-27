# Create shapefile of worldwide boundaries
# Get the centroid of each level 1 polygon

from os.path import abspath, dirname, join
from subprocess import call

import fiona
from fiona.crs import from_epsg

from shapely.geometry import mapping, shape

import us

DEBUG = True

DATA_DIR = dirname(dirname(dirname(abspath(__file__))))

## world countries
PATH_COUNTRIES = join(DATA_DIR,
                      '00_data_original/' +
                      'ne_50m_admin_0_countries_lakes/' +
                      'ne_50m_admin_0_countries_lakes.shp')

# districts
PATH_DISTRICT = join(DATA_DIR,
                     '00_data_original/' +
                     'districtShapes/' +
                     'districts112.shp')

# output level 1
PATH_LEVEL_1 = 'data/level_1.shp'

# open a collection to write to
with fiona.open(
        PATH_LEVEL_1, 'w',
        crs=from_epsg(4326),
        driver='ESRI Shapefile',
        schema={
            'geometry': 'Polygon',
            'properties': {
                'uid': 'str'
            }
        }) as level_1:

    with fiona.open(PATH_COUNTRIES, 'r') as countries:
        count = 0
        try:
            for country in countries:
                # 2 character abbr
                country_abbr_2 = country['properties']['iso_a2']
                # 3 character abbr
                country_abbr_3 = country['properties']['iso_a3']

                uid = country_abbr_2 if country_abbr_2 != u'-99' \
                                     else country_abbr_3

                print 'currently processing: ', uid
                # print country['properties']

                if uid == 'USA':
                    print 'skipping USA'
                    continue

                feature = {}
                feature['properties'] = {}
                feature['properties']['uid'] = uid

                geom = shape(country['geometry'])

                feature['geometry'] = mapping(geom)

                level_1.write(feature)

                # count += 1
                # if count > 5:
                #     break

        except Exception, e:
            print 'error: {0}'.format(e)

    with fiona.open(PATH_DISTRICT, 'r') as districts:
        count = 0
        try:
            for district in districts:
                state_abbr = us.states.lookup(
                    district['properties']['STATENAME']).abbr

                uid = '{0}_'.format(state_abbr) +\
                    '{0}'.format(district['properties']['DISTRICT'])

                print 'currently processing: ', uid

                feature = {}
                feature['properties'] = {}
                feature['properties']['uid'] = uid

                geom = shape(district['geometry'])

                feature['geometry'] = mapping(geom)

                level_1.write(feature)

                # count += 1
                # if count > 5:
                #     break

        except Exception, e:
            print 'error: {0}'.format(e)

geojson_cmd = 'ogr2ogr -f GeoJSON {0} '.format(PATH_LEVEL_1
                                               .replace('.shp',
                                                        '.geojson')) +\
              '{0}'.format(PATH_LEVEL_1)
geojson_cmd = geojson_cmd.split(" ")

print 'writing ogr2ogr shp to geojson'
call(geojson_cmd)

# topojson -o level_1.topojson -p uid  -- level_1.geojson
