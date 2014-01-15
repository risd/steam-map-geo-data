# Ensure the Natural Earth Admin data
# does not have any duplicate names.
# Names will be used as a key for countries
# stored in TopLevelGeo

import fiona

admin_names_list = []
admin_names_set = set()

with fiona.open('ne_50m_admin_0_countries_lakes.shp', 'r') as countries:
    for country in countries:
        admin_names_list.append(country['properties']['admin'])
        admin_names_set.add(country['properties']['admin'])

print "{0} countries in list".format(str(len(admin_names_list)))
print "{0} countries in set".format(str(len(admin_names_set)))
print "{0} difference".format(
    str(len(admin_names_list) - len(admin_names_set)))