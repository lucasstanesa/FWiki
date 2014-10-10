from flask import Flask, render_template, redirect, g, url_for
import sqlite3 as sqlite
import bbcode


app = Flask(__name__)

@app.route('/')
def route_index():
	return route_article('Main_Page')

@app.route('/<title>')
def route_article(title):
	title = title.replace("_", " ")
	
	if not db_init():
		return redier_template('error.html', error='Internal Error', message='An unexpected error occurred'), 503

	g.cursor.execute("SELECT * FROM articles WHERE title=?", [title])
	article = g.cursor.fetchone()
	if article != None:
		g.parser = bbcode.Parser()
		g.parser.add_simple_formatter('wiki', url_for('route_article', title="%(value)s"))
		return render_template('article.html', title=title, content=article['content'])
	else:
		return render_template('error.html', error='404', message='The requested page was not found'), 404

@app.route('/random')
def route_random():
	db_init()
	g.cursor.execute("SELECT title FROM articles WHERE title != 'Main Page' ORDER BY RANDOM( ) LIMIT 1")
	title = g.cursor.fetchone()['title']

	if title:
		return redirect('/' + title.replace(" ", "_"))
	else:
		return redirect('/')


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
	g.dbh.commit()
	g.dbh.close()

