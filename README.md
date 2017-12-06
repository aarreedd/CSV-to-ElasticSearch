# Simple CSV to ElasticSearch Importer

csv_to_elastic.py simplifies importing a csv file into ElasticSearch without the need for ElasticSearch plugins or Logstash.
It can also update existing Elastic data.

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

## EXAMPLES
    1. CREATE example:

    $ python csv_to_elastic.py \
        --elastic-address 'localhost:9200' \
        --csv-file input.csv \
        --elastic-index 'index' \
        --datetime-field=dateField \
        --json-struct '{
            "name" : "%name%",
            "major" : "%major%"
        }'

    CSV:

|  name  |      major       |
|--------|------------------|
|  Mike  |   Engineering    |
|  Erin  | Computer Science |


    2. CREATE/UPDATE example:

    $ python csv_to_elastic.py \
        --elastic-address 'localhost:9200' \
        --csv-file input.csv \
        --elastic-index 'index' \
        --datetime-field=dateField \
        --json-struct '{
            "name" : "%name%",
            "major" : "%major%"
        }'
        --id-column id
CSV:

|  id  |  name  |      major       |
|------|--------|------------------|
|   1  |  Mike  |   Engineering    |
|   2  |  Erin  | Computer Science |

## Notes
    - CSV must have headers
    - insert elastic address (with port) as argument, it defaults to localhost:9200
    - Bulk insert method is used, because inserting row by row is unbelievably slow