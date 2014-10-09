from flask import Flask, render_template, redirect, g, url_for
import sqlite3 as sqlite

app = Flask(__name__)

@app.route('/')
def route_index():
	return route_article('Main_Page')

@app.route('/<title>')
def route_article(title):
	title = title.replace("_", " ")
	db_init()
	g.cursor.execute("SELECT * FROM articles WHERE title=?", [title])
	article = g.cursor.fetchone()
	if article != None:
		return render_template('article.html', title=title, content=article['content'])
	else:
		return redirect('/')

@app.route('/random')
def route_random():
	redirect('/')

def db_init():
	g.dbh = sqlite.connect("wiki.db")
	g.dbh.row_factory = sqlite.Row
	g.cursor = g.dbh.cursor()

def db_close():
	g.dbh.commit()
	g.dbh.close()

