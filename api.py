# -*- coding: utf-8 -*-
"""
    Flaskr
    ~~~~~~

    A microblog example application written as Flask tutorial with
    Flask and sqlite3.

    :copyright: (c) 2010 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
"""
from __future__ import with_statement
from sqlite3 import dbapi2 as sqlite3
from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, send_from_directory, send_file, Response, make_response
import csv

# configuration
DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'
FOLDER = '/home/msi/Projects/flask/mitsuhiko-flask-b209cd9/examples/flaskr'
# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


def connect_db():
    """Returns a new connection to the database."""
    return sqlite3.connect(app.config['DATABASE'])


def init_db():
    """Creates the database tables."""
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.before_request
def before_request():
    """Make sure we are connected to the database each request."""
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    """Closes the database again at the end of the request."""
    g.db.close()


@app.route('/')
def show_entries():
    cur = g.db.execute('select title, text from entries order by id desc')
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into entries (title, text) values (?, ?)',
                 [request.form['title'], request.form['text']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

@app.route('/data/<q>')
def data(q):
  print q
  return render_template('login.html')
  
@app.route('/test', methods=['GET', 'POST'])
def test():
  query=''
  if request.method == 'POST':
    query = request.form['data']+"&"+request.form['year']
    print query
    #print url_for('test',data=request.form['data'],period=request.form['year'])
    #cur = g.db.execute('select title, text from entries where id=1')
    #for row in cur.fetchall():
      #entries = [row[0],row[1]]
   
    #writer = csv.writer(open('temp.csv','wb'), delimiter=' ',quotechar='|', quoting=csv.QUOTE_MINIMAL)
    #writer.writerow(entries)
    #send_file('README')
    #f = send_from_directory(app.config['FOLDER'],'temp.csv',as_attachment=True)
    #f
    #print "f is", f
    #Response((send_from_directory(app.config['FOLDER'],'temp.csv',as_attachment=True)), mimetype='application/octet-stream')
    #print query
    
  #print "Called data"
    return redirect(url_for('data', q=query))
  else:
    return render_template('test.html')


  
if __name__ == '__main__':
    app.run()
