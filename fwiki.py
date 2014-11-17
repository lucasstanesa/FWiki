from flask import Flask, request, render_template, redirect, g, url_for
from markupsafe import Markup, escape
import sqlite3 as sqlite
import markdown

import database

app = Flask(__name__)

import config

@app.route('/', defaults={ 'title' : 'Main_Page' })
@app.route('/<title>')
def route_article(title):
	title = title.replace("_", " ")
	
	if not database.init():
		return error(app.config.db_err_title, config.db_err_msg), 503

	article =  database.fetch("SELECT * FROM articles WHERE title=?", [title])
	database.close()	
	if article != None:
		return render_template('article.html', title=title, content=article['content'])
	else:
		return render_template('article.html', title=title, content="There is currently no text on this page")

@app.route('/edit', defaults={ 'title' : None })
@app.route('/edit/<title>')
def route_edit(title):
	if title == None:
		return redirect('/')
	title = title.replace("_", " ")

	if not database.init():
		return error(app.config.db_err_title, config.db_err_msg), 503
	
	article = database.fetch("SELECT * FROM articles WHERE title = ?", [title])
	database.close()

	if article != None:
		return render_template('edit.html', title=article['title'], id=article['id'], content=article['content'])
	else:
		return render_template('edit.html', title=title, id=0, content='')

@app.route('/do/edit', methods=['POST'])
def route_do_edit():
	title = request.form['title']
	id = int(request.form['id'])
	content = request.form['content']

	if app.config.edit_pass != None:
		if request.form['pass'] != app.config.edit_pass:
			return redirect('/')

	if not database.init():
		return error(app.config.db_err_title, config.db_err_msg), 503

	if id == 0:
		database.query("INSERT INTO articles VALUES(NULL, ?, ?)", [escape(title), escape(content)])
	else:
		database.query("UPDATE articles SET content = ? WHERE id = ?", [escape(content), id])
	
	database.close()
	
	return redirect(url_for('route_article', title=title))

@app.route('/random')
def route_random():
	database.init()
	row = database.fetch("SELECT title FROM articles WHERE title!='Main Page' ORDER BY RANDOM() LIMIT 1")
	database.close()

	if row != None:
		title = row['title'].replace(" ", "_")
		return redirect('/' + title)
	else:
		return redirect('/')


def error(error, message):
	return render_template('error.html', error=error, message=message)

def static_url(file):
	return url_for('static', filename=file)

@app.context_processor
def util_processor():
    return dict(markdown_parse=markdown.markdown, static_url=static_url)


