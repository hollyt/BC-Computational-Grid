#! /usr/bin/python

# This program retrieves the lambda and temperature from an output file and
# adds them to a new table (properties) in each corresponding .dms file, for
# every file in a given directory.
# Usage: ./add-lambda-temp.py <directory>

import glob
import os
import re
import sqlite3
import sys

class Job:
	def __init__(self, name, num, temp, lam):
		self.name = name
		self.num = num
		self.temp = temp
		self.lam = lam

def get_temp_lam(filename):
	temp_pattern = re.compile('Target temperature \(K\) = \d\d\d')
	lam_pattern = re.compile('lambda \d\.\d')
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
		lam = (re.search('\d\.\d', l.group(0))).group(0)
	na = re.search(name_pattern, filename)
	if na:
		name = na.group(0)
	nu = re.search(num_pattern, name)
	if nu:
		num = nu.group(0)

	newjob = Job(name, num, temp, lam)
	return newjob

# Get the filename as command line argument
repname = sys.argv[1:]
if (len(repname) < 1):
	print ('Please enter a repname.')
	sys.exit(-1)

path = './{}'.format(repname[0])
default_path = path

for filename in glob.glob(os.path.join(path, '*.out')):
	job = get_temp_lam(filename)
		
	rcpt = default_path + '/b_rcpt_{}.dms'.format(job.num)
	lig = defualt_path + '/b_lig_{}.dms'.format(job.num)

	# Connect to .dms file
	try:
		rcpt_conn = sqlite3.connect(rcpt)
		lig_conn = sqlite3.connect(lig)
		c_rcpt = rcpt_conn.cursor()
		c_lig = lig_conn.cursor()

		# Create a new table - properties for each .dms file and add 2 columns - temp and lambda
		values = (int(job.temp), float(job.lam))
		create = 'CREATE TABLE properties(Id INT, TempK INT, Lambda REAL)'
		insert = 'INSERT INTO properties VALUES(1,%d,%d)' % (int(job.temp), float(job.lam))
		print ('Adding to {}...'.format(rcpt))
		c_rcpt.execute(create)
		c_rcpt.execute(insert)
		rcpt_conn.commit()
		print ('Adding to {}...\n'.format(lig))
		c_lig.execute(create)
		c_lig.execute(insert)
		lig_conn.commit()

	except Exception as e:
		rcpt_conn.rollback()
		lig_conn.rollback()
		raise e

	finally:
		rcpt_conn.close()
		lig_conn.close()
	

