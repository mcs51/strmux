#!/usr/bin/python3.4

#####################################################################
#                                                                   #
#   Генерация .sh скрипта по схеме yaml                             #
#                                                                   #
#   -h, --help  show this help message and exit                     #
#   -o FILE     set the name of output file                         #
#                                                                   #
# TODO1: FILEPATH_* можно тоже свернуть в ассоциативный массив bash #
# TODO2: setuptools разобраться                                     #
#                                                                   #
#####################################################################

import yaml
import sys
import numbers
import strmuxgen.strmuxgen
from optparse import OptionParser

#parse options and arguments
usage = "usage: %prog [options] schema"
parser = OptionParser(usage=usage)
parser.add_option("-o", dest="filename", default="script.sh", help="set the name of output file", metavar="FILE")

(options, args) = parser.parse_args()
outputfile=options.filename
if not args:
    print("Error: schema file needed\n")
    parser.print_help()
    exit(1)
if len(args)>1:
    print("Error: too many arguments\n")
    parser.print_help()
    exit(2)
schema=args[0]

yaml_code=open(schema).read()
res=yaml.load(yaml_code)


res['formatter'][None] = "echo \"$1\""

outputstr=strmuxgen.strmuxgen.strmuxgen(res)

bash_script = open(outputfile, 'w')

bash_script.write(outputstr)
