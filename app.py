from flask import Flask, jsonify
import sqlite3
import random

app = Flask(__name__)

def get_random_mot():
    conn = sqlite3.connect('/home/choupimalo/Soutenus/mots.db')
    cursor = conn.cursor()
    cursor.execute('SELECT mot FROM mots')
    mots = cursor.fetchall()
    conn.close()
    return random.choice(mots)[0]

@app.route('/mot', methods=['GET'])
def mot():
    mot = get_random_mot()
    return jsonify({'mot': mot})

@app.route('/')
def index():
    return "Bonjour à toutes et à tous"


if __name__ == '__main__':
    app.run(debug=True)
