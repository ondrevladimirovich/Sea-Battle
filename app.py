from flask import Flask, render_template, request, jsonify
import os
import sqlite3
import hashlib
import time

# there are few states of cells:
#   - unknown
# * - miss
# x - wounded
# X - killed
# 1,2,3,4 - alive parts of ship

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

def make_empty_field():
    return ' '*100

# flask route starts here
app = Flask(__name__)

# main page
@app.route('/')
def main_page():
    return render_template('index.html')

# click on new game button
@app.route('/create_new_game')
@app.route('/create_new_game/')
def create_new_game():
    id = generate_link()
    
    # creating db record of new game
    conn = get_db_connection()
    conn.execute("INSERT INTO Battles (Id, Field1, Steps1, Field2, Steps2) VALUES ('" + id + "', '" + make_empty_field() + "', '" + make_empty_field() + "', '" + make_empty_field() + "', '" + make_empty_field() + "')")
    conn.commit()
    conn.close()

    return jsonify(id)

# game page
@app.route('/game/<id>')
def game_page(id):
    # load game state from db
    conn = get_db_connection()
    game = conn.execute("SELECT Id, Field1, Steps1, Field2, Steps2 FROM Battles WHERE Id = '" + id + "'").fetchone()
    conn.close()

    return render_template('game.html', game=game)

@app.route('/fire', methods=['POST'])
@app.route('/fire/', methods=['POST'])
def fire():
    game_id = request.form['game_id']
    # TODO: multiplayer
    game_type = request.form['game_type']
    position = int(request.form['position'])

    conn = get_db_connection()
    game = conn.execute("SELECT Id, Field1, Steps1, Field2, Steps2 FROM Battles WHERE Id = '" + game_id + "'").fetchone()
    enemy_field = game[3]
    user_steps = game[2]

    cahnged_cells = dict()

    new_mark = ''

    #mark empty cell
    if enemy_field[position] == ' ':
        new_mark = '*'

        # prevent repeated steps
        if(new_mark == enemy_field[position]):
            return

        enemy_field = enemy_field[:position] + new_mark + enemy_field[position+1:]
        user_steps = user_steps[:position] + new_mark + user_steps[position+1:]

        conn.execute("UPDATE Battles SET Field2 = '" + enemy_field + "' WHERE Id = '" + game_id + "'")
        conn.commit()
        conn.execute("UPDATE Battles SET Steps1 = '" + user_steps + "' WHERE Id = '" + game_id + "'")
        conn.commit()

        #cahnged_cells[position] = new_mark
    # TODO: else if 1-4 mark cell as wounded or
    # mark bunch of cells if whole ship is killed

    # full enemy field redrawing after every step
    for i in range(100):
        cahnged_cells[i] = user_steps[i]

    return jsonify(cahnged_cells)

# server settings
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.run(host='127.0.0.1', port=port)