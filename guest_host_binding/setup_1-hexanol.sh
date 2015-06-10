#!/bin/bash

# This script creates and sets up 1-hexanol files for the BOINC server

for ((i = 1; i <= 100; i++))
do
	mkdir r$i
	cd r$i
	cp ~/1-hexanol2/1-hexanol_$i.dms 1-hexanol_rcpt.dms
	cp ~/1-hexanol2/bcd_$i.dms 1-hexanol_lig.dms
	cp ~/1-hexanol2/bcd-1-hexanol-work.inp 1-hexanol_0.inp
	cp ~/1-hexanol2/bcd-1-hexanol_cmrestraint.dat 1-hexanol_cmrestraint.dat
	echo "~" >1-hexanol_restdist.dat
	echo "~" >1-hexanol_resttor.dat
	echo "~" >1-hexanol_0.rst
	echo "~" >agbnp2.param
	echo "~" >paramstd.dat
	cd ..
done
