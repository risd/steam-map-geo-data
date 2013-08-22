zipcodes = {}

count = 0
with open('zipcodes.tsv', 'r') as f:
    raw = f.read()
    raw_lines = raw.split('\n')
    for line in raw_lines:
        count += 1
        # skip the first line
        if count == 1:
            continue

        # lon,lat,zip
        split_data = line.strip().split('\t')
        if len(split_data) == 3:
            geo = {}
            geo['lon'] = split_data[0]
            geo['lat'] = split_data[1]
            zipcodes[split_data[2]] = geo

# write to json
import json
with open('zipcodes.json', 'w') as f:
    f.write(json.dumps(zipcodes, separators=(",", ":")))
