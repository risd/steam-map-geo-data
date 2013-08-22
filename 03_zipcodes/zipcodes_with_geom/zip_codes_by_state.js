// creates seperate zipcode geojson files
// for each state

// TODO: needs geometry for zipcodes.

var state_name_abbr = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY'
};

var state_abbr_name = {
    'AL': 'Alabama',
    'AK': 'Alaska',
    'AZ': 'Arizona',
    'AR': 'Arkansas',
    'CA': 'California',
    'CO': 'Colorado',
    'CT': 'Connecticut',
    'DE': 'Delaware',
    'FL': 'Florida',
    'GA': 'Georgia',
    'HI': 'Hawaii',
    'ID': 'Idaho',
    'IL': 'Illinois',
    'IN': 'Indiana',
    'IA': 'Iowa',
    'KS': 'Kansas',
    'KY': 'Kentucky',
    'LA': 'Louisiana',
    'ME': 'Maine',
    'MD': 'Maryland',
    'MA': 'Massachusetts',
    'MI': 'Michigan',
    'MN': 'Minnesota',
    'MS': 'Mississippi',
    'MO': 'Missouri',
    'MT': 'Montana',
    'NE': 'Nebraska',
    'NV': 'Nevada',
    'NH': 'New Hampshire',
    'NJ': 'New Jersey',
    'NM': 'New Mexico',
    'NY': 'New York',
    'NC': 'North Carolina',
    'ND': 'North Dakota',
    'OH': 'Ohio',
    'OK': 'Oklahoma',
    'OR': 'Oregon',
    'PA': 'Pennsylvania',
    'RI': 'Rhode Island',
    'SC': 'South Carolina',
    'SD': 'South Dakota',
    'TN': 'Tennessee',
    'TX': 'Texas',
    'UT': 'Utah',
    'VT': 'Vermont',
    'VA': 'Virginia',
    'WA': 'Washington',
    'WV': 'West Virginia',
    'WI': 'Wisconsin',
    'WY': 'Wyoming'
};

var fs = require('fs');
var d3 = require('d3');

DEBUG = true;

// remove_before_execute(['zip_codes_by_state.json']);
var zip_codes = {};

fs.readFileSync('zip_code_database.csv',
                'utf8', function (err, raw_zip) {

    if (DEBUG) console.log('reading in zip code database');

    // go through each row, and append it into zip_codes
    // if the state name is in the variables defined above
    // (50 states)
    d3.csv.parse(raw_zip, function (c) {
        var state = state_abbr_name[c.state];
        if (state) {
            // should be unique values
            zip_codes[c.zip] = {
                'state': state,
                'state_abbr': c.state,
                'zip': c.zip,
                'zip_lat': c.latitude,
                'zip_lon': c.longitude
            };
        }
    });
});


// write zip code properties in order to use them
// when wanting to look up a zip code locally
// and determinig what state it is in.
if (DEBUG) console.log('writing zip codes with data data ref file');

fs.writeFileSync('zip_codes_with_state_data.json',
                JSON.stringify(zip_codes));


// read in all zip code data in order to create
// grab references to their geometries
// and put them alongside your properties in
// geojson file.

// keep track of all the files that need to be
// written, and the data that goes into them.
var state_files = {};

if (DEBUG) console.log('reading in huge geojson zip code file');

fs.readFileSync('tl_2012_us_zcta510.geojson',
        function (err, raw_zip_geom) {
    for (var i = 0; i < raw_zip_geom.features.length; i++) {
        var zip = zip_codes[raw_zip_geom
                                .features[i]
                                .properties
                                .GEOID10];
        if (zip) {
            if (DEBUG) console.log('found zip in huge file', zip.zip);

            // setup new geojson feature using properties
            // and geometry from other data structures
            var feature = {};
            feature.type = 'Feature';
            feature.properties = zip;
            features.geometry = raw_zip_geom
                                    .features[i]
                                    .geometry;

            // given a state, reference the current file
            var cur_file = 'states/' + zip.state_abbr +
                             '.geojson';
            if (state_files
                    .indexOf(cur_file) === -1) {

                if (DEBUG) console.log(
                                'creating new state file ',
                                cur_file);

                state_files[cur_file] = {
                    'type': 'FeatureCollection',
                    'features': []
                };
            }
            state_files[cur_file].features.append(feature);
        } else {
            if (DEBUG) console.log(
                            'could not find zip in huge geojson ',
                            zip.zip);
        }
    }
});

// write out individual geojson files that house
// geometries for zip codes in that state.
for (var file_path in state_files) {
    fs.writeFileSync(file_path, JSON.stringify(state_files[file_path]));
}