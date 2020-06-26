from flask import Flask, render_template, request, jsonify
import random
import os

app = Flask(__name__)

@app.route('/')
def main_page():
    return render_template('index.html')

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