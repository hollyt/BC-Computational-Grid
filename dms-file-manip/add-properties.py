#! /usr/bin/python

# This program retrieves the lambda and temperature from an output file and
# adds them to a new table (properties) in each corresponding .dms file, for
# every file in a given directory.
# Usage: ./add-lambda-temp.py <directory>

from __future__ import print_function
import glob
import os
import properties
import re
import sys

def get_properties(filename):
	temp_pattern = re.compile('Target temperature \(K\) = \d\d\d')
	lam_pattern = re.compile('lambda \d\.\d*')
	name_pattern = re.compile('b_\d{1,3}')
	num_pattern = re.compile('\d{1,3}')
	
	f = open(filename, 'r')
	text = f.read()
	f.close()
	
	t = re.search(temp_pattern, text)
	if t:
		temp = (re.search('\d\d\d', t.group(0))).group(0)
	l = re.search(lam_pattern, text)
	if l:
		lam = (re.search('\d\.\d*', l.group(0))).group(0)
	na = re.search(name_pattern, filename)
	if na:
		name = na.group(0)
	nu = re.search(num_pattern, name)
	if nu:
		num = nu.group(0)

	return (name, temp, lam)

def add_properties(file, props):
	temp, lam = props
	p = properties.properties(file, temp, lam)
	p.connect()

	if (p.add_properties()):
		return True
	else:
		return False


# Get the directory as command line argument
repname = sys.argv[1:]
if (len(repname) < 1):
	print ('Please enter a repname.')
	sys.exit(-1)

path = './{}'.format(repname[0])
default_path = path

for filename in glob.glob(os.path.join(path, '*.out')):
	# Compile receptor and ligand filenames
	props = get_properties(filename)
	name, props = props[0], props[1:]
	__,__,num = name.rpartition('_')
		
	rcpt = default_path + '/b_rcpt_{}.dms'.format(num)
	lig = default_path + '/b_lig_{}.dms'.format(num)
		
	
	if (add_properties(rcpt, props)):
		print ('Success! Properties added to receptor: {}'.format(rcpt))
	else:
		print ('Error adding properties to receptor: {}'.format(rcpt))
	if (add_properties(lig, props)):
		print ('Success! Properties added to ligand: {}'.format(lig))
	else:
		print ('Error adding properties to ligand: {}'.format(lig))
