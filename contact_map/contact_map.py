#! /usr/bin/python

from __future__ import print_function
from itertools import izip
from math import sqrt
import sqlite3
import sys

# Function to calculate the distance between receptor and ligand atoms in 3d space
def are_neighbors(rcpt_atoms, lig_atoms):
	for rcpt_atom in rcpt_atoms:
		for lig_atom in lig_atoms:
			xd = rcpt_atom[3] - lig_atom[3]
			yd = rcpt_atom[4] - lig_atom[4]
			zd = rcpt_atom[5] - lig_atom[5]
			distance = sqrt(xd*xd + yd*yd + zd*zd)
			if (distance < 4.0):
				return True
	return False

# Get all recptor filenames and ligand filenames
with open("*rcpt file path*") as rcpt, open("*lig file path*") as lig:
	# Must strip the newline character from each line so it's not included in filename!
	rcpt_files = [line.rstrip('\n') for line in rcpt]
	lig_files = [line.rstrip('\n') for line in lig]

# Get initial information
rcpt_conn = sqlite3.connect('*rcpt file path*')
lig_conn = sqlite3.connect('*lig file path*')

c_rcpt = rcpt_conn.cursor()
c_lig = lig_conn.cursor()

c_rcpt.execute('SELECT DISTINCT resid from particle')
_rcpt_resids = c_rcpt.fetchall()

# Convert from list of tuples to list of ints because it will be easier for later
# This is ugly but it works for now
rcpt_resids = range(len(_rcpt_resids))
for x in range(len(rcpt_resids)):
	rcpt_resids[x] = (_rcpt_resids[x])[0]
c_lig.execute('SELECT DISTINCT resid from particle')
_lig_resids = c_lig.fetchall()
lig_resids = range(len(_lig_resids))
for x in range(len(lig_resids)):
	lig_resids[x] = (_lig_resids[x])[0]

# Create dictionaries of resid and resname
rcpt_dict = {}
lig_dict = {}
for rcpt in rcpt_resids:
	c_rcpt.execute('SELECT resname from particle where resid = {}'.format(rcpt))
	rresname = c_rcpt.fetchone()
	rcpt_dict[rcpt] = str(rresname[0])

for lig in lig_resids:
	c_lig.execute('SELECT resname from particle where resid = {}'.format(lig))
	lresname = c_lig.fetchone()
	lig_dict[lig] = str(lresname[0])

# Create matrix of 0s
neighbors = [[0.0 for _ in range(len(rcpt_resids))] for _ in range(len(lig_resids))]

structures = 0
for rcpt, lig in izip(rcpt_files, lig_files):

	try:
		# Create a Connection object that represents the database
		rcpt_conn = sqlite3.connect(rcpt)
		lig_conn = sqlite3.connect(lig)

		# Create a cursor object and call its execute() method to perform SQL commands
		c_rcpt = rcpt_conn.cursor()
		c_lig = lig_conn.cursor()

		# Print output to a new text file instead of the console
		log = open('*your logfile path*', 'a')

		for i in range(len(rcpt_resids)):
			c_rcpt.execute("SELECT resid, resname, name, x, y, z FROM particle where resid = '{}'".format(rcpt_resids[i]))
			rcpt_residue_atoms = c_rcpt.fetchall()
			for j in range(len(lig_resids)):
				c_lig.execute("SELECT resid, resname, name, x, y, z FROM particle where resid = '{}'".format(lig_resids[j]))
				lig_residue_atoms = c_lig.fetchall()
				if (are_neighbors(rcpt_residue_atoms, lig_residue_atoms)):
					neighbors[j][i] += 1
		
		structures += 1
	# Catch the exception and continue if we're missing the .dms file
	except sqlite3.OperationalError as e:
		print('Could not open {}'.format(rcpt))


# Get probability of contacts
for i in range(len(neighbors)):
	for j in range(len(neighbors[i])):
		neighbors[i][j] /= structures

# print to file
for i in range(len(neighbors)):
	for j in range(len(neighbors[i])):
		c_rcpt.execute("SELECT resid, resname, name, x, y, z FROM particle where resid = '{}'".format(rcpt_resids[i]))
		print('{}{}-{}{}\t{:.2f}'.format(rcpt_dict.get(rcpt_resids[j]),rcpt_resids[j],lig_dict.get(lig_resids[i]),lig_resids[i],neighbors[i][j]*100),file=log)

# Close the connection
rcpt_conn.close()
lig_conn.close()
