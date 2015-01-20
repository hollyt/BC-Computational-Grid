#! /bin/bash

# This script runs the script add-lambda-temp.py for every replica directory

echo "Starting..."
for ((i = 1; i <= 143; i++))
do
	./add-properties.py r$i
done
