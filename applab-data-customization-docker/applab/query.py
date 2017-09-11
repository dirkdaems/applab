#!/env/python

import sys
import os
import time
import argparse
import datetime

# import catalog client
from catalogclient import catalog

# Creates a directory tree.
def mkdir(name,mode=0777):
    if os.path.isdir(name) == False:
        try:
            os.makedirs(name, mode)

        except Exception as e:
            time.sleep(0.1)

            if (os.path.isdir(name) == True):
                # a parallel process has just created this directory
                pass
            else:
                print 'Error creating directory "%s":' % name
                print type(e), e

    return os.path.isdir(name)

# Parse command-line arguments
parser = argparse.ArgumentParser()

parser.add_argument('-startdate', action='store', dest='startdate', required=True, help='Start date (format: YYYYMMDD)')
parser.add_argument('-enddate',   action='store', dest='enddate',   required=True, help='End date (format: YYYYMMDD)')
parser.add_argument('-type',      action='store', dest='type',      required=True, help='Product type.')
parser.add_argument('-out',       action='store', dest='output',    required=True, help='Full path to the output listing file.')

results = parser.parse_args()

dt1 = datetime.strptime(results.startdate, "%Y%m%d");
dt2 = datetime.strptime(results.enddate, "%Y%m%d");

# Create output directory if not yet existing
mkdir(os.path.dirname(results.output))

# Query catalog
catalog = catalog.Catalog()

products = catalog.get_products(results.type, startdate=dt1.date(), enddate=dt2.date());

filenames = []

for product in products:

    fn = product.files[0].filename

    if fn.startswith("file:"):
        fn = 'file://' + inputfile[5:]

    print fn

    filenames.append(fn)

# Write filenames to output listing file
with open(results.output, 'w') as f:

    for fn in filenames:
        f.write(fn + os.linesep);

    f.close();

