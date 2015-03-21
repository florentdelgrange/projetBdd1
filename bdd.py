import sqlite3

class Bdd(object):
	def __init__(self, bdd = None):
		self.bdd = bdd
		self.df = []
