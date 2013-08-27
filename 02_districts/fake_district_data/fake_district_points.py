# reads in district shapefile
# writes out fake district shapefile
# converts fake data from shp to geojson
# converts fake data from geojson to topojson


from collections import OrderedDict
import logging
from os.path import abspath, dirname, join
import random
from subprocess import call
import sys

from shapely.geometry import mapping, shape

import fiona

import us

logging.basicConfig(stream=sys.stderr, level=logging.INFO)

ROOT_PATH = dirname(abspath(__file__))

DISTRICT_SHP_PATH = join(dirname(dirname(dirname(abspath(__file__)))),
                         '00_data_original/' +
                         'districtShapes/districts112.shp')

GENERATED_SHP_PATH = join(dirname(abspath(__file__)),
                          'data/fake_district_points.shp')

with fiona.open(DISTRICT_SHP_PATH, 'r') as c_in:

    c_out_properties = {
        'state': 'str:50',
        'state_abbr': 'str:3',
        'work_edu': 'int',
        'work_res': 'int',
        'work_pol': 'int',
        'work_ind': 'int'
    }
    c_out_schema = {'geometry': 'Point'}
    c_out_schema['properties'] = \
        OrderedDict(sorted(c_out_properties.items(), key=lambda t: t[0]))

    with fiona.open(GENERATED_SHP_PATH, 'w',
                    crs=c_in.meta['crs'],
                    driver=c_in.meta['driver'],
                    schema=c_out_schema
                    ) as c_out:

        try:

            for f_in in c_in:
                state = f_in['properties']['STATENAME']
                state_abbr = us.states.lookup(state).abbr

                geom = shape(f_in['geometry'])

                centroid = geom.centroid

                f_out = {}

                f_out['geometry'] = mapping(centroid)
                f_out['properties'] = {}

                f_out['properties']['state'] = state

                f_out['properties']['state_abbr'] = state_abbr

                f_out['properties']['work_edu'] = \
                    random.randrange(50, 500)

                f_out['properties']['work_res'] = \
                    random.randrange(50, 500)

                f_out['properties']['work_pol'] = \
                    random.randrange(50, 500)

                f_out['properties']['work_ind'] = \
                    random.randrange(50, 500)

                c_out.write(f_out)

                print 'processed ', state

        except Exception, e:
            print 'error: {0}'.format(e)

# geojson it
geo_cmd = 'ogr2ogr -f GeoJSON {0}'.format(ROOT_PATH) +\
          '/data/fake_district_points.geojson ' +\
          '{0}'.format(GENERATED_SHP_PATH)
geo_cmd = geo_cmd.split(" ")
# print geo_cmd

print 'writing geojson'
call(geo_cmd)
