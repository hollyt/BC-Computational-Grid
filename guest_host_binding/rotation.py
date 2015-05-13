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
		x_total += atoms.get(atom)[0]
		y_total += atoms.get(atom)[1]
		z_total += atoms.get(atom)[2]
		atom_count += 1
	return ((x_total/atom_count),(y_total/atom_count),(z_total/atom_count))
	
def pick_points():
	# radius
	r = 1
	# Latitude angle is random # between 0 - 360
	lat_angle = random.uniform(0,math.pi)
	# epsilon = cos(x)
	cosx = random.uniform(-1,1)
	# z coordinate
	z = r*cosx
	
	# sin(x) = +/- sqrt(1 - cos^2(x))
	sinx = math.sqrt(1 - cosx**2)
	# Randomly choose -1 or 1 for the +/- part of previous equation
	seq = [-1,1]
	sign = random.choice(seq)
	sinx = sign * sinx

	# formulas for x & y coordinates
	y = r * sinx * math.sin(lat_angle)
	x = r * sinx * math.cos(lat_angle)

	return(x,y,z)

# x is the angle
def rotate(atoms,center_mass_lig):
	ux, uy, uz = pick_points()
	# x is theta
	x = random.uniform(0,2*math.pi)
	# rotation matrix
	R = [[(math.cos(x) + (ux**2 * (1 - math.cos(x)))), (ux*uy * (1 - math.cos(x)) - (uz * math.sin(x))), ((ux*uz * (1 - math.cos(x))) + uy*math.sin(x))],
	     [((uy*ux * (1 - math.cos(x))) + uz*math.sin(x)), (math.cos(x) + ((uy**2) * (1 - math.cos(x)))), ((uy*uz * (1 - math.cos(x))) - (ux * math.sin(x)))],
	     [((uz*ux * (1 - math.cos(x))) - (uy * math.sin(x))), ((uz*uy * (1 - math.cos(x))) + (ux * math.sin(x))), (math.cos(x) + (uz**2 * (1 - math.cos(x))))]]	

	# subtract center of mass from every atom
	for atom in atoms:
		atoms.get(atom)[0] -= center_mass_lig[0]
		atoms.get(atom)[1] -= center_mass_lig[1]
		atoms.get(atom)[2] -= center_mass_lig[2]
	
	# multiply Rotation matrix by every atom
	atom_prime = []

	for atom in atoms:
		atom_prime.append(multiply(R,atoms.get(atom)))

	return atom_prime

def multiply(rotation_matrix,coordinates):
	atom_prime = [0,0,0]
	atom_prime[0] = (rotation_matrix[0][0] * coordinates[0]) + (rotation_matrix[0][1] * coordinates[1]) + (rotation_matrix[0][2] * coordinates[2])
	atom_prime[1] = (rotation_matrix[1][0] * coordinates[0]) + (rotation_matrix[1][1] * coordinates[1]) + (rotation_matrix[1][2] * coordinates[2])
	atom_prime[2] = (rotation_matrix[2][0] * coordinates[0]) + (rotation_matrix[2][1] * coordinates[1]) + (rotation_matrix[2][2] * coordinates[2])
	return (atom_prime[0],atom_prime[1],atom_prime[2])

def add(translate_coordinates,coordinates):
	atom_prime = [0,0,0]
	atom_prime[0] = translate_coordinates[0] + coordinates[0]
	atom_prime[1] = translate_coordinates[1] + coordinates[1]
	atom_prime[2] = translate_coordinates[2] + coordinates[2]
	return (atom_prime[0],atom_prime[1],atom_prime[2])
				
def translate(atoms):
	# start with (0,0,0) to test this
	# radius in Angstroms
	r = 8.0
	neg_r = -1.0 * 8
	# create a cube around the receptor
	#cube = [(0,0,0), (1,0,0), (1,1,0), (0,1,0), (0,0,1), (1,0,1), (1,1,1), (0,1,1)]

	# Generate a random point within the cube and check if it's in the sphere
	# http://stackoverflow.com/questions/5531827/random-point-on-a-given-sphere
	# http://www.gamedev.net/topic/95637-random-point-within-a-sphere/
	while True:
		x = random.uniform(neg_r,r)
		y = random.uniform(neg_r,r)
		z = random.uniform(neg_r,r)
		if (x**2 + y**2 + z**2 > r**2):
			break
	atom_prime = []

	for atom in atoms:
		atom_prime.append(add((x,y,z),atoms.get(atom)))

	return atom_prime	
def main():
	# key = atom id; value = list of (x,y,z) coordinates
	# list rather than tuple becuase we need to subtract the center of mass
	# from every atom later
	lig_atoms = {}
	rcpt_atoms = {}
	
	# stuff you need to do to connect to the sqlite database ~>
	rcpt_conn = sqlite3.connect('''path/to/your/rcpt.dms''')
	lig_conn = sqlite3.connect('''path/to/your/lig.dms''')
	c_rcpt = rcpt_conn.cursor()
	c_lig = lig_conn.cursor()

	# get the atoms in tuples of 3
	c_lig.execute('SELECT i_i_internal_atom_index, x, y, z FROM particle')
 	lig = c_lig.fetchall()
	c_rcpt.execute('SELECT i_i_internal_atom_index, x, y, z FROM particle')
	rcpt = c_rcpt.fetchall()
	
	# Create a dictionary atom id - tuple of coordinates so the correct coordinates
	# can be updated later
	for atom in lig:
		lig_atoms[atom[0]] = [atom[1],atom[2],atom[3]]
	for atom in rcpt:
		rcpt_atoms[atom[0]] = [atom[1],atom[2],atom[3]]

	# TESTING
	# print lig atoms before rotation to compare after rotation
	print('LIG ATOMS BEFORE ROTATION')
	for entry in lig_atoms:
		print('{}:{}'.format(entry,lig_atoms.get(entry)))
	#print('RCPT ATOMS:')	
	#for entry in rcpt_atoms:
		#print('{}:{}'.format(entry,rcpt_atoms.get(entry)))


	# find the centers of mass
	center_mass_lig = center_of_mass(lig_atoms)
	center_mass_rcpt = center_of_mass(rcpt_atoms)
	
	# Rotate the ligand randomly
	rotated = rotate(lig_atoms, center_mass_lig)
	new = translate(lig_atoms)
	# TO DO: translate ligand to a random place
		
	# Update the coordinate values
	count = 1
	for atom in new:
		c_lig.execute('UPDATE particle SET x = {}, y = {}, z = {} WHERE i_i_internal_atom_index = {}'.format(atom[0],atom[1],atom[2],count))
		count += 1
	lig_conn.commit()

	# Print lig atoms after rotation - did it work?
	c_lig.execute('SELECT i_i_internal_atom_index, x, y, z FROM particle')
	new_atoms = c_lig.fetchall()

	# just testing
	temp = {}
	for atom in new_atoms:
		temp[atom[0]] = (atom[1],atom[2],atom[3])
	print('\nLIG ATOMS AFTER ROTATION')
	for entry in temp:
		print('{}:{}'.format(entry,temp.get(entry)))

	lig_conn.close()
	rcpt_conn.close()

if __name__ == '__main__':
	main()
