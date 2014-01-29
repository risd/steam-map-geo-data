# second pass to ensure it wasn't a rate
# limiting problem that was being run into
# instead of an inability to actually geocode

from pygeocoder import Geocoder


countries_list = None
geocoded_str = u'country\tlon\tlat\n'
not_geocoded_str = u'country\n'

with open('countries_NOT_geocoded.tsv', 'r') as countries:
    countries_list = countries.read().decode('utf8').split('\n')[1:]

for country in countries_list:
    try:
        geocoded = Geocoder.geocode(country)
        lon = geocoded[0].coordinates[1]
        lat = geocoded[0].coordinates[0]

        geocoded_str += u'{0}\t{1}\t{2}\n'.format(country, lon, lat)

    except:
        not_geocoded_str += u'{0}\n'.format(country)

with open('countries_geocoded_second.tsv', 'w') as countries_tsv:
    countries_tsv.write(geocoded_str.encode('utf8'))

with open('countries_NOT_geocoded_second.tsv', 'w') as not_countries_tsv:
    not_countries_tsv.write(not_geocoded_str.encode('utf8'))