from flask import Flask, render_template, request, jsonify
import random
import os
import sqlite3

def get_db_connection():
    conn = sqlite3.connect('db/sb.db')
    conn.row_factory = sqlite3.Row
    return conn

app = Flask(__name__)

@app.route('/')
def main_page():
    conn = get_db_connection()
    battles = conn.execute('SELECT * FROM Battles').fetchall()
    conn.close()
    return render_template('index.html', battles=battles)

@app.route('/create_new_game')
@app.route('/create_new_game/')
def create_new_game():
	id = random.randint(1,100)
	return jsonify(id)

@app.route('/game/<id>')
def game_page(id):
    return render_template('game.html', id=id)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.run(host='127.0.0.1', port=port)