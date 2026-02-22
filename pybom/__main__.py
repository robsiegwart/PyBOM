'''
Run the program from the command line via python module mode.

> python -m pyBOM FOLDER ACTION

    FOLDER      the folder name containing Excel files
    ACTION      the property to call on the ``BOM`` object

'''

import sys
import argparse
from .BOM import BOM


parser = argparse.ArgumentParser(
    prog='python -m pyBOM',
    description='Parse a folder of Excel Bill-of-Materials.'
)


group = parser.add_mutually_exclusive_group(required=True)
group.add_argument(
    '-f', '--file',
    help='The name of a single Excel BOM file.',
    metavar='FILE'
)
group.add_argument(
    '-d', '--dir',
    help='The name of the folder containing Excel BOM files.',
    metavar='FOLDER'
)

parser.add_argument(
    'action',
    help='What to do with the resulting BOM.',
    default='tree'
)

ns = parser.parse_args()

if ns.file:
    bom = BOM.single_file(ns.file)
elif ns.dir:
    bom = BOM.from_folder(ns.dir)
else:
    raise ValueError('Either --file or --dir must be specified.')

print(getattr(bom, ns.action))