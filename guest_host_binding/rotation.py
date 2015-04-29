#!/usr/bin/python

from __future__ import print_function
import math
import random
import sqlite3

def center_of_mass(atoms):
	x_total = 0
	y_total = 0
	z_total = 0
	atom_count = 0
	for atom in atoms:
		x_total += atom[0]
		y_total += atom[1]
		z_total += atom[2]
		atom_count += 1
	return ((x_total/atom_count),(y_total/atom_count),(z_total/atom_count))

def pick_points():
	# radius
	r = 1
	# Latitude angle is random # between 0 - 360
	lat_angle = random.uniform(0,360)
	# epsilon = cos(x)
	cosx = random.uniform(-1,1)
	# z coordinate
	z = r*cosx
	
	# sin(x) = +/- sqrt(1 - cos^2(x))
	sinx = math.sqrt(1 - cosx**2)
	# Randomly choose -1 or 1 for the +/- part of previous equation
	seq = [-1,1]
	sign = random.choice(req)
	sinx = sign * sinx

	# formulas for x & y coordinates
	y = r * sinx * math.sin(lat_angle)
	x = r * sinx * math.cos(lat_angle)

	return(x,y,z)

# x is the angle
def rotate(atoms):
	ux, uy, uz = pick_points()
	# x is theta
	x = random.uniform(0,360)
	# rotation matrix
	R = [[((math.cos(x) + ux**2) * (1 - math.cos(x))), (ux*uy * (1 - math.cos(x)) - uz * math.sin(x)), (ux*uz * (1 - math.cos(x)) + uy*math.sin(x))], [(uy*ux * (1 - math.cos(x)) + uz*math.sin(x)), (math.cos(x) + (uy**2) * (1 - math.cos(x))), (uy*uz * (1 - math.cos(x)) - ux * math.sin(x))], [(uz*ux * (1 - math.cos(x)) - uy * math.sin(x)), (uz*uy * (1 - math.cos(x)) + ux * math.sin(x)), (math.cos(x) + uz**2 * (1 - math.cos(x)))]]	

	# Perform affinity transformation - multiply Rotation matrix by every atom
	atom_prime = []
	
	# TO DO: This part...
	
	return atom_prime
						

def main():

	# stuff you need to do to connect to the sqlite database ~>
	rcpt_conn = sqlite3.connect("""path/to/rcpt/file.dms""")
	lig_conn = sqlite3.connect("""path/to/lig/file.dms""")
	c_rcpt = rcpt_conn.cursor()
	c_lig = lig_conn.cursor()

	# get the atoms
	c_lig.execute('SELECT x, y, z FROM particle')
 	lig_atoms = c_lig.fetchall()
			
	# The atoms are in tuples of 3

	# Rotate the ligand randomly
	rotate(lig_atoms)

	# Find the center of mass of the ligand
	center_mass_lig = center_of_mass(lig_atoms)
 	print(center_mass_lig)
	

if __name__ == '__main__':
	main()
