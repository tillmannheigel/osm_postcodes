#!/bin/zsh

while getopts o:f: flag
do
    case "${flag}" in
        o) output_filename=${OPTARG};;
        f) input_filename=${OPTARG};;
    esac
done

osmium tags-filter ${input_filename} boundary=postal_code -o postal_codes.osm.pbf -O

osmium export postal_codes.osm.pbf -o postcodes.geojson -O

rm postal_codes.osm.pbf

echo '{"type":"FeatureCollection","features":[' > output.geojson

grep MultiPolygon postcodes.geojson >> output.geojson

rm postcodes.geojson

echo ']}' >> output.geojson
