=== Calculate BOINC throughput data and client analysis ===

Usage: get_throughput_data.py <(start date) YYYY/MM/DD> <(end date) YYYY/MM/DD>
client_analysis.py <(start date) YYYY/MM/DD> <(end date) YYYY/MM/DD>

What is it?
------------
get_throughput_data - This is a simple python script to calcuate throughput data for a BOINC grid computing server. The script outputs two files - one formatted for graphing with gnuplot and one with relevant information in human readable format. Also included is a gnuplot script for creating stacked histograms with the data.
client_analysis - This script calculates the number of successful jobs finished by each client computer, for each day in a given time period. Use it to monitor which clients are successfully completing the most work.

Running the scripts
------------------
Before running the script, make sure to enter the correct name, username, and password for *your* BOINC mySQL database.

For questions & more information:
-----------------------------
tancredi.holly@gmail.com

https://sites.google.com/site/emiliogallicchiolab/research/research-blog/calculatingboincthroughputdata
