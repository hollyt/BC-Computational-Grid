# /usr/bin/python

# This script retrieves the number of successfully completed jobs for each client on
# your BOINC grid, for each day within a given time period
# and prints to a .dat file (formatted for plotting with gnuplot)
# Correct usage is: client_analysis.py <(start date)YYYY/MM/DD> <(end date)YYYY/MM/DD>
# Ex: ./client_analysis.py 2014/12/01 2015/01/01

from __future__ import print_function
from datetime import datetime, date
import calendar
import MySQLdb
import sys
import time

# Connect to the boinc mySQL database
#db = ''
#db_user = ''
#db_pw = ''
db = MySQLdb.connect(user=db_user, passwd=db_pw, db=db)

# Create cursor object to execute queries
curr = db.cursor()

# Get the date options
start = str(sys.argv[1])
end = str(sys.argv[2])
start_struct = time.strptime(start, '%Y/%m/%d')
start_date = calendar.timegm(start_struct)
end_struct = time.strptime(end,'%Y/%m/%d')
# Add seconds for end of day on end_date
end_date = calendar.timegm(end_struct) + 86399

# Create output file
d = 'datafiles/' + time.strftime('%Y.%m.%d', time.gmtime(start_date)) + '-' + time.strftime('%Y.%m.%d', time.gmtime(end_date)) + '.dat' 
datafile = open(d, 'a+')
print ('#Date\tHost\tSuccessful Jobs', file = datafile)

# Query the database
start_of_day = start_date

while start_of_day <= end_date:
	num_success_jobs = 0
	end_of_day = (start_of_day + 86399)
	for host in range(1,482):
		curr.execute('SELECT COUNT(*) from result where hostid = {} and server_state = "5" and outcome = "1" and received_time <= {} and received_time >= {}'.format(host, end_of_day, start_of_day))
		data = curr.fetchone()
		print (time.strftime('%Y/%m/%d', time.gmtime(start_of_day)) + '\t{}\t{}'.format(host, data[0]), file = datafile)
	start_of_day += 86400
