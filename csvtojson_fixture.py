## Adapted from: https://www.djangosnippets.org/snippets/1680/
import sys
import getopt
import csv
from os.path import dirname
import json

try:
    script, input_file_name, model_name = sys.argv
except ValueError:
    print("\nRun via:\n\n%s input_file_name model_name" % sys.argv[0])
    print("\ne.g. %s airport.csv app_airport.Airport" % sys.argv[0])
    print("\nNote: input_file_name should be a path relative to where this script is.")
    sys.exit()

in_file = dirname(__file__) + input_file_name
out_file = dirname(__file__) + input_file_name.replace(".csv","") + ".json"

print("Converting %s from CSV to JSON as %s" % (in_file, out_file))

f = open(in_file, 'r' )
fo = open(out_file, 'w')

reader = csv.reader( f )

header_row = []
entries = []
pk_counter = 1
for row in reader:
    if not header_row:
        header_row = row
        print(header_row)
        continue
        
    pk = pk_counter
    model = model_name
    fields = {}
    for i in range(len(row)):
        active_field = row[i]
        # if active_field.isdigit():
        #     try:
        #         new_number = int(active_field)
        #     except ValueError:
        #         new_number = float(active_field)
        #     fields[header_row[i]] = new_number
        # else:
        #     fields[header_row[i]] = active_field.strip()
        fields[header_row[i]] = str(active_field).strip()
    pk_counter = pk_counter + 1
        
    row_dict = {}
    row_dict["pk"] = int(pk)
    row_dict["model"] = model_name
    
    row_dict["fields"] = fields
    entries.append(row_dict)
fo.write("%s" % json.dumps(entries, indent=4))
f.close()
fo.close()