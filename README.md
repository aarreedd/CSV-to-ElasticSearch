# Simple CSV to ElasticSearch Importer

csv_to_elastic.py simplifies importing a csv file into ElasticSearch without the need to ElasticSearch plugins or Logstash.

## How it Works

The script creates an ElasticSearch API PUT request for 
each row in your CSV. It is similar to running:

    $ curl -XPUT 'http://localhost:9200/twitter/tweet/1' -d '{
        "user" : "elastic",
        "post_date" : "2015-09-25T14:12:12",
        "message" : "trying out Elasticsearch"
    }'

In both `json-struct` and `elastic-path`, the script will
insert your CSV data by replacing the column name wrapped in '%'
tags with the data for the given row. For example, `%id%` will be 
replaced with data from the `id` column of your CSV.

## Example

If your CSV looks like:

|  id  |  name  |      major       |
|------|--------|------------------|
|   1  |  Mike  |   Engineering    |
|   2  |  Erin  | Computer Science |

You could import it with this command:

    $ python csv_to_elastic.py \
        --csv-file input.csv \
        --elastic-path '<index>/<type>/%id%' \
        --json-struct '{
            "name" : "%name%",
            "major" : "%major%"
        }'

## Notes
- CSV must have headers
- localhost:9200 assumed

