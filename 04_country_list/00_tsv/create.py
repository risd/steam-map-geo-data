# List of Countries that will be used
# for signing up

from os.path import abspath, dirname, join

import fiona

DATA_DIR = dirname(dirname(dirname(abspath(__file__))))

## world countries
PATH_COUNTRIES = join(DATA_DIR,
                      '00_data_original/' +
                      'ne_50m_admin_0_countries_lakes/' +
                      'ne_50m_admin_0_countries_lakes.shp')

# open a collection to write to
country_str = u'country\nUnited States of America\n'

with fiona.open(PATH_COUNTRIES, 'r') as countries:
    # count = 0
    try:
        for country in countries:
            if country['properties']['admin'] == 'United States of America':
                continue
            country_str += u'{0}\n'.format(country['properties']['admin'])

            # count += 1
            # if count > 5:
            #     break

    except Exception, e:
        print 'error: {0}'.format(e)

with open('countries.tsv', 'w') as country_tsv:
    country_tsv.write(country_str.encode('utf8'))
