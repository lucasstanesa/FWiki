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
    title = title.replace('_', ' ')
    
    if not database.init():
        return error(app.config['db_err_title'], app.config['db_err_msg']), 503

    article =  database.fetch('SELECT * FROM articles WHERE title = ? AND revision = 0', [title])
    database.close()
    if article != None:
        return render_template('article.html', title=title, content=article['content'])
    else:
        return render_template('article.html', title=title, content='There is currently no text on this page')

@app.route('/<title>/revisions', defaults={ 'rev' : "list" })
@app.route('/<title>/revisions/<rev>')
def route_revisions(title, rev):
    title = title.replace('_', ' ')
    
    if not database.init():
        return error(app.config['db_err_title'], app.config['db_err_msg']), 503

    if not database.fetch('SELECT 1 from articles WHERE title = ?', [title]):
        return redirect('/%s' % title)

    if rev == "list":
       revisions = database.fetch_all('SELECT * FROM articles WHERE title = ?', [title])
       return render_template('revision.html', rev="list", title=title, revisions=revisions)
    elif rev != 0:
       article = database.fetch('SELECT * FROM articles WHERE title = ? AND revision = ?', [title, rev])
       return render_template('revision.html', rev=rev, title=title, content=article['content'])
    else:
       return redirect('/%s' % title)
        

@app.route('/edit', defaults={ 'title' : None })
@app.route('/edit/<title>')
def route_edit(title):
    if title == None:
        return redirect('/')
    title = title.replace('_', ' ')

    if not database.init():
        return error(app.config['s_db_title'], app.config['s_db_msg']), 503
    
    article = database.fetch('SELECT * FROM articles WHERE title = ?', [escape(title)])
    database.close()

    if article != None:
        return render_template('edit.html', title=article['title'], id=article['id'], content=article['content'])
    else:
        return render_template('edit.html', title=title, id=0, content='')

@app.route('/do/edit', methods=['POST'])
def route_do_edit():
    title = form('title')
    id = int(form('id'))
    content = form('content')
    hpot = form('email')

    if title is None or id is None or content is None or hpot is not "":
        return 'Error'

    if app.config['locked']:
        if form('pass') != app.config['pass']:
            return redirect('/')

    if not database.init():
        return error(app.config['db_err_title'], app.config['db_err_msg']), 503

    if id == 0:
        database.query('INSERT INTO articles VALUES(NULL, ?, ?, 0)', [escape(title), escape(content)])
    else:
        database.query("UPDATE articles SET revision = 1 WHERE title=?", [title])
        database.query("INSERT INTO articles VALUES(NULL, ?, ?, 0)", [escape(title), escape(content)])

    database.close()

    return redirect(url_for('route_article', title=title))

@app.route('/random')
def route_random():
    database.init()
    row = database.fetch("SELECT title FROM articles WHERE title!='Main Page' ORDER BY RANDOM() LIMIT 1")
    database.close()

    if row != None:
        title = row['title'].replace(' ', '_')
        return redirect('/' + title)
    else:
        return redirect('/')

def form(name):
    if not name in request.form:
        return None

    return request.form[name]

def error(error, message):
    return render_template('error.html', error=error, message=message)

def static_url(file):
    return url_for('static', filename=file)

@app.context_processor
def util_processor():
    return dict(markdown_parse=markdown.markdown, static_url=static_url)


