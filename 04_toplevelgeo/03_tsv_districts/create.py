# write out districts and centroids for toplevelgeo import

from os.path import abspath, dirname, join

import fiona

from shapely.geometry import shape

import us

DEBUG = True

DATA_DIR = dirname(dirname(dirname(abspath(__file__))))

# districts
PATH_DISTRICT = join(DATA_DIR,
                     '00_data_original/' +
                     'districtShapes/' +
                     'districts112.shp')

districts_str = 'us_state\t' +\
                'us_state_abbr\t' +\
                'us_district\t' +\
                'us_district_ordinal\t' +\
                'lon\t' +\
                'lat\t' +\
                'minx\t' +\
                'miny\t' +\
                'maxx\t' +\
                'maxy\n'

ordinal = lambda n: "%d%s" %\
                (n,"tsnrhtdd"[(n/10%10!=1)*(n%10<4)*n%10::4])

with fiona.open(PATH_DISTRICT, 'r') as districts:
    count = 0
    try:
        for district in districts:
            state = district['properties']['STATENAME']
            state_abbr = us.states.lookup(
                district['properties']['STATENAME']).abbr
            us_district = int(district['properties']['DISTRICT'])
            us_district_ordinal = ordinal(us_district)

            geom = shape(district['geometry'])
            centroid = geom.centroid
            
            lon, lat = centroid.x, centroid.y
            minx, miny, maxx, maxy = geom.bounds

            current = '{0}\t'.format(state) +\
                      '{0}\t'.format(state_abbr) +\
                      '{0}\t'.format(us_district) +\
                      '{0}\t'.format(us_district_ordinal) +\
                      '{0}\t'.format(lon) +\
                      '{0}\t'.format(lat) +\
                      '{0}\t'.format(minx) +\
                      '{0}\t'.format(miny) +\
                      '{0}\t'.format(maxx) +\
                      '{0}\n'.format(maxy)

            districts_str += current
            print current

            # count += 1
            # if count > 5:
            #     break

    except Exception, e:
        print 'error: {0}'.format(e)

with open('districts.tsv', 'w') as districts_tsv:
    districts_tsv.write(districts_str)
