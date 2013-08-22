var fs = require('fs');
var d3 = require('d3');

DEBUG = true;

remove_before_execute(['fake-steam-level-1.geojson']);

fake_data = {
    "type": "FeatureCollection",
    'features': []
};

fs.readFile('us-states.geojson', 'utf8', function (err, data) {
    var i;
    data = JSON.parse(data);

    for (i=0; i < data.features.length; i++) {
        data.features[i].properties.level_1_postal =
            data.features[i].properties.postal;

        data.features[i].properties.level_1_us_bool = 1;

        data.features[i].properties.level_1_work_in_edu =
            random([50,500]);

        data.features[i].properties.level_1_work_in_research =
            random([50,500]);

        data.features[i].properties.level_1_work_in_policy =
            random([50,500]);

        data.features[i].properties.level_1_work_in_industry =
            random([50,500]);

        var centroid = d3.geo.centroid(data.features[i]);

        data.features[i].geometry.type = 'Point';
        data.features[i].geometry.coordinates = centroid;

        var to_keep = ['level_1_postal',
                        'level_1_us_bool',
                        'level_1_work_in_edu',
                        'level_1_work_in_research',
                        'level_1_work_in_policy',
                        'level_1_work_in_industry'];

        var j;
        for (var key in data.features[i].properties) {
            if (to_keep.indexOf(key) === -1) {
                delete data.features[i].properties[key];
            }
        }

        if (DEBUG) console.log(data.features[i].properties);
    }

    write_data(data);
});

function remove_before_execute(to_delete) {
    if (DEBUG) console.log('Cleaning up files before execution');
    var i;
    for (i=0; i < to_delete.length; i++) {
        if (fs.existsSync(to_delete[i])) {
            fs.unlinkSync(to_delete[i]);

            if (DEBUG) console.log('deleted ', to_delete[i]);
        }
    }
    if (DEBUG) console.log('Done cleaning.');
}

function write_data (fake_data) {
    fs.writeFileSync('fake-steam-level-1.geojson',
                        JSON.stringify(fake_data));
}

function random (args) {
    var min = args[0],
        max = args[1];

    var range = max - min;

    var random_value = Math.floor(Math.random() * range);

    return min + random_value;
}