geocodeable_countries_list = None
geocoded_country_str = u'country\n'


# filtered countries list
with open('../01_ensure_geocode/countries_geocoded.tsv', 'r') as countries:
    geocodeable_countries_list =\
        countries.read().decode('utf8').split('\n')[1:]

for country in geocodeable_countries_list:
    geocoded_country_str += u'{0}\n'.format(country.split('\t')[0])

with open('countries_geocodable.tsv', 'w') as countries_tsv:
    countries_tsv.write(geocoded_country_str.encode('utf8'))
