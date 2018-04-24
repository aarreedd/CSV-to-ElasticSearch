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

This script requires Python 3 with the python-dateutils and http modules to be installed (pip3 install python-dateutils http)

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

## Flags
Required:
```
--csv-file CSV_FILE
  Name of csv file to read
--json-struct JSON_STRUCT
  JSON structure (See example above)
--elastic-index ELASTIC_INDEX
  Elasticsearch index name
```
  Optional:
  ```
  --elastic-address ELASTIC_ADDRESS
    Address of Elasticsearch server (Default: localhost:9200)
  --elastic-type ELASTIC_TYPE
    Elasticsearch type name (Now deprecated in Elasticsearch)
  --max-rows MAX_ROWS
    Maxmimum number of rows to read from csv file
  --datetime-field DATETIME_FIELD
    Indicate that a field is a datetime. That way it will be parsed and incerted correctly.
  --id-column ID_COLUMN
    Specify row ID column. Used for updating data. 
  --delimiter DELIMITER
    Delimiter to use in csv file (default is ';')
```

## Notes
    - CSV must have headers
    - insert elastic address (with port) as argument, it defaults to localhost:9200
    - Bulk insert method is used, because inserting row by row is unbelievably slow
