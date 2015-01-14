#! usr/bin/python

# properties class - creates a new table "properties" for .dms files
# and stores/retrieves relevant information (temperature (K), lambda) there.

import sqlite3
import sys

class properties:
	def __init__(self, filename, temp, lam):
		self._filename = filename
		self._basename, __, __ = filename.rpartition('.')
		self._temp = temp
		self._lam = lam

	def connect(self):
		try:
			self._connection = sqlite3.connect(self._filename)
			self._cursor = self._connection.cursor()

		except sqlite3.DatabaseError as e:
			print type(e)
			print 'Cannot connect to .dms file.'
			sys.exit(-1)
		
	def add_properties(self):
		create = 'CREATE TABLE properties (Id INT, TempK INT, Lambda REAL)'
		values = (1, int(self._temp), float(self._lam))

		try:
			self._cursor.execute(create)
			self._cursor.execute('INSERT INTO properties VALUES(?,?,?)', values)
			self._connection.commit()
			return True
			
		except sqlite3.DatabaseError as e:
			print type(e)
			print 'Error adding data to properties.'
			self._connection.rollback()
			self._connection.close()
			return False
	
	def get_properties(self):
		self._cursor.execute('SELECT * from properties')
		# Returns a list of all rows of query results (id,temp,lam)
		return self._cursor.fetchall()
	
	def __exit__(self):
		self._connection.close()
