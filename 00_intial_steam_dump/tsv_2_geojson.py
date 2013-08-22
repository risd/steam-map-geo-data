import codecs
import json
import time

from pygeocoder import Geocoder


class SteamData():
    """
    deal with steam data
    """

    _default_schema = {
        'properties': {
            'noteworthy': 0,
            'last_name': 1,
            'first_name': 2,
            'organization': 3,
            'phone': 4,
            'email': 5,
            'city': 6,
            'state': 7,
            'country': 8,
            'affiliation': 9,
            'type': 10,
            'tags': 11,
            'description': False,
            'link': 13,
            'on_map': 14,
            'private_public': 15,
            'relationship': 16,
            'list_type': 17,
        }
    }

    def __init__(self, filepath, schema=_default_schema):
        self.filepath = filepath

        self.schema = schema

        self.data = self.import_from_file(self.filepath)

    def geocode(self, fields):
        city = fields[
            self.schema['properties']['city']
        ].strip()

        state = fields[
            self.schema['properties']['state']
        ].strip()

        country = fields[
            self.schema['properties']['country']
        ].strip()

        location = ''
        if city and state and country:
            location = "{0}, {1}, {2}".format(city, state, country)
        elif state and country:
            location = "{0}, {1}".format(state, country)
        elif country:
            location = "{0}".format(country)
        else:
            return None

        if len(location):
            # time.sleep(0.5)
            coordinates = Geocoder.geocode(location)
        else:
            return None

        print "\n\n{0}".format(location)
        print "{0}\n\n".format(coordinates[0].coordinates)

        return [coordinates[0].coordinates[1],
                coordinates[0].coordinates[0]]

    def write(self, filepath):
        with open(filepath, 'w') as output:
            output.write(json.dumps(
                         self.data,
                         separators=(',', ':'),
                         ))

    def import_from_file(self, filepath):
        collection = {}
        collection['type'] = 'FeatureCollection'
        collection['features'] = []
        with codecs.open(filepath, 'r', 'utf-8') as raw_data:
            count = 0
            for line in raw_data:
                count += 1
                if count == 1:
                    # skip the first line
                    continue

                # if count > 5:
                    # test rest of script
                    # continue

                fields = line.split('\t')

                # every new line is a new feature
                feature = {}

                feature['type'] = 'Feature'

                feature['geometry'] = {}
                feature['geometry']['type'] = 'Point'

                feature['geometry']['coordinates'] = \
                    self.geocode(fields)

                if not feature['geometry']['coordinates']:
                    continue

                feature['properties'] = {}

                for prop in self.schema['properties']:
                    if self.schema['properties'][prop]:
                        feature['properties'][prop] = \
                            fields[
                                self.schema['properties'][prop]
                            ].strip()
                    else:
                        feature['properties'][prop] = ''

                collection['features'].append(feature)

        return collection


if __name__ == '__main__':
    steam = SteamData('STEAM All - STEAM All.tsv')
    steam.write('steam.geojson')
