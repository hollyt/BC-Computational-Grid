#! usr/bin/python

# properties class - creates a new table "properties" for .dms files
# and stores/retrieves relevant information (temperature, lambda, etc.) there.

import sqlite3
import sys

class properties:
	def __init__(self, filename, property, value):
		self._filename = filename
		self._property = str(property)
		self._value = value
		if type(value) is int:
			self._type = 'INTEGER'
		elif type(value) is float:
			self._type = 'REAL'
		else:
			self._type = 'TEXT'

	def connect(self):
		try:
			self._connection = sqlite3.connect(self._filename)
			self._cursor = self._connection.cursor()
		except sqlite3.DatabaseError as e:
			print type(e)
			print 'Could not connect to .dms file.'
			sys.exit(-1)
		
	def add_properties(self):
		self._cursor.execute('CREATE TABLE IF NOT EXISTS properties (id INTEGER PRIMARY KEY)')
		self._cursor.execute('INSERT OR IGNORE INTO properties(id) values(1)')
		try:
			self._cursor.execute('UPDATE properties SET {}={} WHERE id=1'.format(self._property, self._value,))
		except sqlite3.OperationalError as e:
			try:
				self._cursor.execute('ALTER TABLE properties ADD COLUMN {}'.format(self._property))
				self._cursor.execute('UPDATE properties SET {}={} WHERE id=1'.format(self._property, self._value,))
			except sqlite3.DatabaseError:
				return False
		finally:
			self._connection.commit()
		return True
			
	@staticmethod
	def get_properties(filename):
		try:	
			connection = sqlite3.connect(filename)
			connection.row_factory = sqlite3.Row
			cursor = connection.cursor()
			cursor.execute('SELECT * from properties')
			# Returns a dictionary of all query results
			row = cursor.fetchone()
			return row

		except sqlite3.DatabaseError as e:
			print type(e)
			print 'Could not connect to .dms file.'
			sys.exit(-1)

	def __exit__(self):
		self._connection.close()
