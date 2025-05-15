from flask import Flask, render_template, jsonify, request
import sqlite3
import random

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('/home/choupimalo/Soutenus/mots.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_random_mot():
    conn = get_db_connection()
    mot = conn.execute('SELECT * FROM mots ORDER BY RANDOM() LIMIT 1').fetchone()
    conn.close()
    return mot

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/mot')
def mot():
    mot = get_random_mot()
    return jsonify({
        'mot': mot['mot'],
        'definition': mot['definition'] if 'definition' in mot else None
    })

@app.route('/add_word', methods=['POST'])
def add_word():
    data = request.get_json()
    mot = data['mot']
    definition = data.get('definition', '')

    conn = get_db_connection()
    try:
        conn.execute('INSERT INTO mots (mot, definition) VALUES (?, ?)', (mot, definition))
        conn.commit()
        return jsonify({'status': 'success'}), 201
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400
    finally:
        conn.close()

if __name__ == '__main__':
    app.run()
