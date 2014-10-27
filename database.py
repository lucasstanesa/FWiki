import sqlite3 as sqlite
from flask import g

def db_init():
	try:
		g.dbh = sqlite.connect("wiki.db")
		g.dbh.row_factory = sqlite.Row
		g.cursor = g.dbh.cursor()
	except Exception:
		return False
	finally:
		return True

def db_close():
	if g.dbh:
		g.dbh.commit()
		g.dbh.close()

def db_query(query, binds=[]):
	return g.cursor.execute(query, binds)

def db_fetchone():
	return g.cursor.fetchone()