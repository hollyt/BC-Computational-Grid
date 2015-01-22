=== Add and Retrieve Properties to DESRES Molecular System (.dms) Files ===

Usage
------
./add_properties.py <directory>
./get_properties.py <directory>

To use the properties class in your own python script: import properties

What is it?
------------
properties.py is a python class that adds properties of a molecular system to a new table (properties)
in .dms files. The class supports creating custom columns in the properties table. Our example script
uses Temperature and Lambda. The method get_properties() retrieves all information from the properties
table and returns it as a dictionary.

add_properties.py and get_properties.py are example scripts that use the properties class to build and
retrieve information from the properties table.

Running the scripts
------------------
You can run add_properties.py and get_properties.py with the included sample directory, r1. add_properties.py
uses regular expressions to get temperature and lambda values from output files and create a properties
table with these values in the corresponding .dms files. get_properties.py retrieves the properties infromation
from the .dms file and prints it to standard output.

To run: ./add_properties.py r1
	./get_properties.py r1

For questions & more information:
-----------------------------
tancredi.holly@gmail.com

https://sites.google.com/site/emiliogallicchiolab/research/research-blog/
