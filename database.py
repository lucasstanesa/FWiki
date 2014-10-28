import sqlite3 as sqlite
from flask import g

def init():
	try:
		g.dbh = sqlite.connect("wiki.db")
		g.dbh.row_factory = sqlite.Row
		g.cursor = g.dbh.cursor()
	except Exception:
		return False
	finally:
		return True

def close():
	if g.dbh:
		g.dbh.commit()
		g.dbh.close()
		g.dbh = g.cursor = None

def query(query, binds=[]):
	return g.cursor.execute(query, binds)

def query_many(query, binds=[]):
	return g.cursor.executemany(query, binds)

def fetchall():
	return g.cursor.fetchall()

def fetchone():
	return g.cursor.fetchone()
