#!/usr/bin/python

# This is a test program to make sure my algorithm for plotting
# random points on a sphere is correct.

from __future__ import print_function
import math
import random
import sqlite3

def plot_point():
	# radius
	r = 1
	lat_angle = random.uniform(0,360)
	# Epsilon = cos(x)
	cosx = random.uniform(-1,1)
	z = r*cosx
	
	# sin(x) = +- sqrt(1 - cos^2(x))
	sinx = math.sqrt(1 - cosx**2)
	# Randomly choose -1 or 1 for the +- part of previous equation
	seq = [-1,1]
	sign = random.choice(seq)
	sinx = sign * sinx

	y = r * sinx * math.sin(lat_angle)
	x = r * sinx * math.cos(lat_angle)

	return(x,y,z)

def main():
	with open('sphere_plot.dat','a') as outfile:
		for x in range(1000):
			points = plot_point()
			print('{}\t{}\t{}'.format(points[0],points[1],points[2]), file=outfile)

if __name__ == '__main__':
	main()
