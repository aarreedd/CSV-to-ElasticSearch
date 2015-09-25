#!/usr/bin/python 2

"""
DESCRIPTION
	Simple python script to import a csv into ElasticSearch.

HOW IT WORKS
	The script creates an ElasticSearch API PUT request for 
	each row in your CSV. It is similar to running:

	$ curl -XPUT localhost:9200/<index>/<type>/<id> -d '{ ... }'

	In both `json-struct` and `elastic-path` path, the script will
	insert your csv data by replacing the column name wrapped in '%'
	with the data for the given row. For example, `%id%` will be 
	replaced with data from the `id` column of your CSV.
	
NOTES
	- CSV must have headers
	- localhost:9200 assumed

EXAMPLES

    $ python csv_to_elastic.py \
        --csv-file input.csv \
        --elastic-path '<index>/<type>/%id%' \
        --json-struct '{
            "name" : "%name%",
            "major" : "%major%"
        }'

CSV:

|  id  |  name  |      major       |
|------|--------|------------------|
|   1  |  Mike  |   Engineering    |
|   2  |  Erin  | Computer Science |

"""

import argparse
import urllib2
import httplib
import pprint
import csv

parser = argparse.ArgumentParser(description='CSV to ElasticSearch.')

parser.add_argument(	'--csv-file',
			required=True,
			type=str,
			help='path to csv to import')
parser.add_argument(	'--json-struct',
			required=True,
			type=str,
			help='json to be inserted')
parser.add_argument(	'--elastic-path',
			required=True,
			type=str,
			help='<index>/</type>/%id%')
parser.add_argument(	'--max-rows',
			type=int,
			default=10,
			help='max rows to import')

args = parser.parse_args()

url  = "localhost:9200"
path = "/" + args.elastic_path.strip("/")

print("")
print(" ----- CSV to ElasticSearch ----- ")
print("Importing %s rows into `%s` from '%s'" %(args.max_rows,args.elastic_path.strip("/"),args.csv_file))
print("")

count = 0
headers = []
with open(args.csv_file, 'rb') as csvfile:
	reader = csv.reader(csvfile, delimiter=',', quotechar='"')
	for row in reader:
		if count == 0:
			for col in row:
				headers.append(col)
		elif count >= args.max_rows:
			exit('Max rows imported - exit')
		else:
			pos = 0
			_data = args.json_struct.replace("'",'"')
			_path = path
			for header in headers:
				_path = _path.replace('%'+header+'%',row[pos])
				_data = _data.replace('%'+header+'%',row[pos])
				pos += 1
			# Send the request
			connection = httplib.HTTPConnection(url)
			connection.request('PUT', _path, _data)
			response = connection.getresponse()
			print response.status, response.reason
			data = response.read()
			print data
			# raw_input('...')
			
		count += 1

exit('Reached end of CSV - exit')
