from flask import Flask, render_template, request, g
import sqlite3

app = Flask(__name__)
DATABASE = 'knowledge_base.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form['query']
        return search(query)
    return render_template('index.html')

def search(query):
    cur = get_db().cursor()
    cur.execute("SELECT title, content FROM articles WHERE content LIKE ?", ('%' + query + '%',))
    results = cur.fetchall()
    return render_template('search_results.html', query=query, results=results)

if __name__ == '__main__':
    app.run(debug=True)
