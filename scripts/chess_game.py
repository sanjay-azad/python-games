import chess
import chess.svg
import chess.engine


board = chess.Board()
chess_board = chess.svg.board(board=board, size=400)


class Game:

    def new_game(self):
        self.board = chess.Board()
        self.move = None
        self.undo_fen = None

    def get_board_state(self):
        return self.board.fen()

    def set_board_state(self, fen):
        # self.undo_fen = self.board.fen()
        self.board = chess.Board(fen)

    def undo_board_state(self, undo_fen):
        self.board = chess.Board(undo_fen)

    def make_user_move(self, move):
        self.undo_fen = self.board.fen()
        self.move = self.board.push_san(move)
        return self.get_board_state(), self.board.is_checkmate()

    def make_engine_move(self, move):
        self.move = chess.Move.from_uci(move)
        self.board.push_uci(move)
        return self.get_board_state(), self.board.is_checkmate()

    def render_board(self):
        return chess.svg.board(board=self.board, size=400, lastmove=self.move)


class GameEngine:
    def __init__(self):
        self.engine = chess.engine.SimpleEngine.popen_uci(
            "stockfish/stockfish_10_x64")
        self.limit = chess.engine.Limit(time=2.0)
