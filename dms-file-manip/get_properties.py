#! /usr/bin/python

from __future__ import print_function
import glob
import os
import properties
import re
import sys

# Get the directory as command line argument
repname = sys.argv[1:]
if (len(repname) < 1):
	print ('Please enter a repname.')
	sys.exit(-1)

path = './{}'.format(repname[0])

for filename in glob.glob(os.path.join(path, 'b_*.dms')):
	props = properties.properties.get_properties(filename)
	__,__,file = filename.rpartition('/')
	print ('{} - Temperature: {} Lambda: {}'.format(file, props['temperature'], props['lambda']))
