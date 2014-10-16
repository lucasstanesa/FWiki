from flask import Flask, render_template, redirect, g, url_for
from markupsafe import Markup, escape
import sqlite3 as sqlite
import bbcode
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
		markdown_init()
		return render_template('article.html', title=title, content=escape(article['content']))
	else:
		return render_template('article.html', title=title, content="There is currently no text on this page")

@app.route('/<title>/edit')
def route_edit(title):
	title = title.replace("_", " ")

	if not db_init():
		return error('Internal Error', 'An unexpected error occurred'), 503
	
	db_query("SELECT * FROM articles WHERE title=?", [title])
	article = db_fetchone()
	if article != None:
		return render_template('edit.html', article=article)
	else:
		return redirect('/')

@app.route('/do/edit', methods=["POST"])
def route_do_edit():
	article_id = request.form['article_id']
	content = require.form['content']
	

@app.route('/random')
def route_random():
	db_init()
	db_query("SELECT title FROM articles WHERE title!='Main Page' ORDER BY RANDOM() LIMIT 1")
	title = db_fetchone()['title']
	db_close()

	if title:
		return redirect('/' + title.replace(" ", "_"))
	else:
		return redirect('/')


def error(error, message):
	return render_template('error.html', error=error, message=message)

def markdown_init():
	g.parser = markdown.Markdown(safe_mode='')

def bbcode_article(tag_name, value, options, parent, context):
	url = url_for('route_article', title=value)
	return '<a href="%s">%s</a>' % (url, value)

def bbcode_section(tag_name, value, options, parent, context):
	utitle = value.replace(" ", "_").lower()
	url = '#' + utitle
	return '<a title="%s" name="%s" class="section">%s</a>' % (utitle, utitle, value)
