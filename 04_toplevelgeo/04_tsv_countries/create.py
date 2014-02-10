# List of Countries that will be used
# for signing up

from os.path import abspath, dirname, join

import fiona

from shapely.geometry import shape

DATA_DIR = dirname(dirname(dirname(abspath(__file__))))

## world countries
PATH_COUNTRIES = join(DATA_DIR,
                      '00_data_original/' +
                      'ne_50m_admin_0_countries_lakes/' +
                      'ne_50m_admin_0_countries_lakes.shp')

# open a collection to write to
country_str = 'country\t' +\
              'lon\t' +\
              'lat\t' +\
              'minx\t' +\
              'miny\t' +\
              'maxx\t' +\
              'maxy\n'
                

with fiona.open(PATH_COUNTRIES, 'r') as countries:
    count = 0
    try:
        for country in countries:
            if country['properties']['admin'] == \
               'United States of America':
                continue

            geom = shape(country['geometry'])
            centroid = geom.centroid
            lon, lat = centroid.x, centroid.y
            minx, miny, maxx, maxy = geom.bounds

            current = u'{0}\t'.format(country['properties']['admin']) +\
                      u'{0}\t'.format(lon) +\
                      u'{0}\t'.format(lat) +\
                      u'{0}\t'.format(minx) +\
                      u'{0}\t'.format(miny) +\
                      u'{0}\t'.format(maxx) +\
                      u'{0}\n'.format(maxy)
            
            country_str += current
            print current

            # count += 1
            # if count > 5:
            #     break

    except Exception, e:
        print 'error: {0}'.format(e)

with open('countries.tsv', 'w') as country_tsv:
    country_tsv.write(country_str.encode('utf8'))
