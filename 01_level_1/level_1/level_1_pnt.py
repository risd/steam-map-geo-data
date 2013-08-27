# create shapefile of all points
# that could end up being home to
# steamie data.

# centroid of every country or US district

# indexed by their uid
# country 3 character code, or
# state abbr_district number

import json
from os.path import abspath, dirname, join

import fiona

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
PATH_LEVEL_1 = 'data/level_1_pnt.json'

level_1 = {}

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

            if uid == 'US':
                print 'skipping US'
                continue

            geom = shape(country['geometry'])
            centroid = geom.centroid

            latlon = mapping(centroid)['coordinates']

            level_1[uid] = {
                u'lat': latlon[1],
                u'lon': latlon[0],
            }

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

            geom = shape(district['geometry'])
            centroid = geom.centroid

            latlon = mapping(centroid)['coordinates']

            level_1[uid] = {
                u'lat': latlon[1],
                u'lon': latlon[0],
            }

            # count += 1
            # if count > 5:
            #     break

    except Exception, e:
        print 'error: {0}'.format(e)

print 'writing json'
with open(PATH_LEVEL_1, 'w') as out_file:
    out_file.write(json.dumps(level_1))
