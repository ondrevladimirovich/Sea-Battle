from flask import Flask, render_template, request, jsonify
import os
import sqlite3
import hashlib
import time

# function to connect with sqlite db
def get_db_connection():
    conn = sqlite3.connect('db/sb.db')
    conn.row_factory = sqlite3.Row
    return conn

# generates unique (I hope so) game id
def generate_link():
    hash = hashlib.sha1()
    hash.update(str(time.time()).encode('utf-8'))
    return hash.hexdigest()[:10]

# flask route starts here
app = Flask(__name__)

# main page
@app.route('/')
def main_page():
    #conn = get_db_connection()
    #battles = conn.execute('SELECT * FROM Battles').fetchall()
    #conn.close()
    #return render_template('index.html', battles=battles)
    return render_template('index.html')

# click on new game button
@app.route('/create_new_game')
@app.route('/create_new_game/')
def create_new_game():
    id = generate_link()
    
    # creating db record of new game
    conn = get_db_connection()
    conn.execute("INSERT INTO Battles (Id, Field1, Field2) VALUES ('" + id + "', '0', '0')")
    conn.commit()
    conn.close()

    return jsonify(id)

# game page
@app.route('/game/<id>')
def game_page(id):
    # load game state from db
    conn = get_db_connection()
    game = conn.execute("SELECT Id, Field1, Field2 FROM Battles WHERE Id = '" + id + "'").fetchone()
    conn.close()

    return render_template('game.html', game=game)

# server settings
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.run(host='127.0.0.1', port=port)