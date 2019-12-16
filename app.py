# Import dependencies
from flask import Flask, render_template, Markup, request, session, jsonify
import chess
import chess.svg
from scripts.chess_game import Game, GameEngine

# Instance of Flask App
app = Flask(__name__)
app.secret_key = 'FluKU8w9^^8O'

game = Game()
engine = GameEngine()

# Define Index Route
@app.route("/")
# Content
def home():
    # return("Home Page")
    return render_template("index.html")

# Define About Route
@app.route("/chess")
# Content
def start_game():
    game.new_game()
    session['board_state'] = game.get_board_state()
    return render_template("chess.html", chess_board=Markup(game.render_board()))

@app.route("/user_move", methods = ['GET', 'POST'])
# Content
def user_move():
    if request.method == 'POST':
        move = request.form['move']
        board_state = session.get('board_state')
        # game.set_board_state(board_state)
        session['board_state'], checkmate_flag = game.make_user_move(move)
        return jsonify(board=Markup(game.render_board()), checkmate=checkmate_flag)

@app.route("/engine_move", methods = ['GET', 'POST'])
# Content
def engine_move():
    if request.method == 'POST':
        board = game.board
        result = engine.engine.play(board, engine.limit)
        print(str(result.move))
        session['board_state'], checkmate_flag = game.make_engine_move(str(result.move))
        return jsonify(board=Markup(game.render_board()), checkmate=checkmate_flag)

@app.route("/undo", methods = ['GET', 'POST'])
# Content
def undo_move():
    if request.method == 'POST':
        undo_fen = game.undo_fen
        game.undo_board_state(undo_fen)
        return Markup(game.render_board())

# Running & Controlling script
if (__name__ == "__main__"):
    app.run(debug=True)
