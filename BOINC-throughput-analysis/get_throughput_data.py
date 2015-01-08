#! /usr/bin/python

# This script retrieves BOINC throughput data from the mySQL server
# It prints 2 files - .dat (formatted for plotting with gnuplot) and .out (human readable output)
# Correct usage is: get_throughput_data.py <(start date)YYYY/MM/DD> <(end date)YYYY/MM/DD>
# Ex: ./get_throughput_data.py 2014/12/01 2015/01/01

from __future__ import print_function
import calendar
import MySQLdb
import sys
import time
from datetime import datetime, date

# Connect to the boinc mySQL database
#db = ''
#db_user = ''
#db_pw = ''
db = MySQLdb.connect(user=db_user, passwd=db_pw, db=db)

# Create cursor object to execute queries
curr = db.cursor()

# Results that are NOT a Success
failed_outcomes = { 2 : 'COULDN\'T SEND' , 3 : 'COMPUTATION ERROR', 4 : 'NO REPLY', 5 : 'DIDN\'T NEED', 6 : 'VALIDATE ERROR', 7 : 'ABANDONED'}
completed = 5

# Get the date options
dates = sys.argv[1:]
if (len(dates) < 2):
	print ('Please enter start date and end date.')
	print ('Usage: ./get_throughput_data.py <YYYY/MM/DD> <YYYY/MM/DD>')
	sys.exit(-1)

start = str(dates[0])
end = str(dates[1])
start_struct = time.strptime(start, '%Y/%m/%d')
start_date = calendar.timegm(start_struct)
end_struct = time.strptime(end, '%Y/%m/%d')
# Add seconds for end of day on end_date
end_date = calendar.timegm(end_struct) + 86399

# Create output files
d = '/throughput_analysis/datafiles/' + time.strftime('%Y.%m.%d', time.gmtime(start_date)) + '-' + time.strftime('%Y.%m.%d', time.gmtime(end_date)) + '.dat' 
o = '/throughput_analysis/outfiles/' + time.strftime('%Y.%m.%d', time.gmtime(start_date)) + '-' + time.strftime('%Y.%m.%d', time.gmtime(end_date)) + '.out'
datafile = open(d, 'a+')
outputfile = open(o, 'a+')

# Query the database
get_finished_jobs = 'SELECT outcome from result where server_state = {} and received_time <= {} and received_time >= {}'.format(completed, end_date, start_date)
curr.execute(get_finished_jobs)
num_finished_jobs = curr.rowcount

print ('BOINCIMPACT THROUGHPUT DATA: \n==========================', file = outputfile)
print ('Completed jobs between {} and {}: {}'.format(start, end, num_finished_jobs), file = outputfile)
print ('#Date\tSuccess\tFailed', file = datafile)

start_of_day = start_date
failed_outcomes_count = [0]*6

while start_of_day <= end_date:
	num_success_jobs = 0
	num_failed_jobs = 0
	end_of_day = (start_of_day + 86399)
	curr.execute('SELECT outcome from result where server_state = {} and received_time <= {} and received_time >= {}'.format(completed, end_of_day, start_of_day))
	for outcome in curr:
		#outcome is returned as a tuple
		if (outcome[0] == 1):
			num_success_jobs += 1
		else:
			num_failed_jobs += 1
			failed_outcomes_count[(outcome[0]-2)] += 1

	# Formatting from epoch time to human readable time
	print (time.strftime('%Y/%m/%d', time.gmtime(start_of_day)) + ': {} success {} failed'.format(num_success_jobs, num_failed_jobs), file = outputfile)

	# Print to .dat file
	print (time.strftime('%Y/%m/%d', time.gmtime(start_of_day)) + '\t{}\t{}'.format(num_success_jobs, num_failed_jobs), file = datafile)	
	
	start_of_day += 86400

print ('\nREASONS FOR FAILURE: \n=========================', file = outputfile)
for outcome in failed_outcomes: 
	print ('{}: {}'.format(failed_outcomes.get(outcome), failed_outcomes_count[(outcome-2)]), file = outputfile)

# Disconnect from surver
db.close()
