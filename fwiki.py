from flask import Flask, request, render_template, redirect, g, url_for
from markupsafe import Markup, escape
import sqlite3 as sqlite
import markdown

#Local imports
from database import *

app = Flask(__name__)

@app.route('/')
def route_index():
	return route_article('Main_Page')

@app.route('/<title>')
def route_article(title):
	title = title.replace("_", " ")
	
	if not db_init():
		return error('Internal Error', 'An unexpected error occurred'), 503

	db_query("SELECT * FROM articles WHERE title=?", [title])
	article = db_fetchone()
	db_close()	
	if article != None:
		return render_template('article.html', title=title, content=article['content'])
	else:
		return render_template('article.html', title=title, content="There is currently no text on this page")

@app.route('/edit/<title>')
def route_edit(title):
	title = title.replace("_", " ")

	if not db_init():
		return error('Internal Error', 'An unexpected error occurred'), 503
	
	db_query("SELECT * FROM articles WHERE title = ?", [title])
	article = db_fetchone()
	if article != None:
		return render_template('edit.html', title=article['title'], id=article['id'], content=article['content'])
	else:
		return render_template('edit.html', title=escape(title), id=0, content='')

@app.route('/do/edit', methods=['POST'])
def route_do_edit():
	title = request.form['title']
	id = int(request.form['id'])
	content = request.form['content']

	if not db_init():
		return error('Internal Error', 'An unexpected error occurred'), 503

	if id == 0:
		db_query("INSERT INTO articles VALUES(NULL, ?, ?)", [escape(title), escape(content)])
	else:
		db_query("UPDATE articles SET content = ? WHERE id = ?", [escape(content), id])
	
	db_close()
	
	return redirect(url_for('route_article', title=title))

@app.route('/random')
def route_random():
	db_init()
	db_query("SELECT title FROM articles WHERE title!='Main Page' ORDER BY RANDOM() LIMIT 1")
	row = db_fetchone()
	db_close()

	if row != None:
		return redirect('/' + row['title'].replace(" ", "_"))
	else:
		return redirect('/')


def error(error, message):
	return render_template('error.html', error=error, message=message)

def markdown_parse(content):
	return markdown.markdown(content)

@app.context_processor
def util_processor():
    return dict(markdown_parse=markdown_parse)


