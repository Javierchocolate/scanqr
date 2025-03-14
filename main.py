from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS scans (id INTEGER PRIMARY KEY, url TEXT)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    data = request.json.get('url', '')
    if data:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("INSERT INTO scans (url) VALUES (?)", (data,))
        conn.commit()
        conn.close()
        return jsonify({'message': 'URL guardada', 'url': data})
    return jsonify({'error': 'No se recibió ninguna URL'})

@app.route('/latest')
def latest():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT url FROM scans ORDER BY id DESC LIMIT 1")
    row = c.fetchone()
    conn.close()
    return jsonify({'url': row[0] if row else ''})

if __name__ == '__main__':
    app.run(debug=True)

