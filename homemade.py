"""
Some example classes for people who want to create a homemade bot.

With these classes, bot makers will not have to implement the UCI or XBoard interfaces themselves.
"""
import chess
from chess.engine import PlayResult, Limit
import random
from lib.engine_wrapper import MinimalEngine
from lib.lichess_types import MOVE, HOMEMADE_ARGS_TYPE
import logging
import time

from piece_square_tables import (
    PIECE_SQUARE_TABLES,
    KING_MIDDLE_TABLE,
    KING_END_TABLE
)


# Use this logger variable to print messages to the console or log files.
# logger.info("message") will always print "message" to the console or log file.
# logger.debug("message") will only print "message" if verbose logging is enabled.
logger = logging.getLogger(__name__)


class ExampleEngine(MinimalEngine):
    """An example engine that all homemade engines inherit."""


# Bot names and ideas from tom7's excellent eloWorld video

class RandomMove(ExampleEngine):
    """Get a random move."""

    def search(self, board: chess.Board, *args: HOMEMADE_ARGS_TYPE) -> PlayResult:  # noqa: ARG002
        """Choose a random move."""
        return PlayResult(random.choice(list(board.legal_moves)), None)


class Alphabetical(ExampleEngine):
    """Get the first move when sorted by san representation."""

    def search(self, board: chess.Board, *args: HOMEMADE_ARGS_TYPE) -> PlayResult:  # noqa: ARG002
        """Choose the first move alphabetically."""
        moves = list(board.legal_moves)
        moves.sort(key=board.san)
        return PlayResult(moves[0], None)


class FirstMove(ExampleEngine):
    """Get the first move when sorted by uci representation."""

    def search(self, board: chess.Board, *args: HOMEMADE_ARGS_TYPE) -> PlayResult:  # noqa: ARG002
        """Choose the first move alphabetically in uci representation."""
        moves = list(board.legal_moves)
        moves.sort(key=str)
        return PlayResult(moves[0], None)


class ComboEngine(ExampleEngine):
    """
    Get a move using multiple different methods.

    This engine demonstrates how one can use `time_limit`, `draw_offered`, and `root_moves`.
    """

    def search(self,
               board: chess.Board,
               time_limit: Limit,
               ponder: bool,  # noqa: ARG002
               draw_offered: bool,
               root_moves: MOVE) -> PlayResult:
        """
        Choose a move using multiple different methods.

        :param board: The current position.
        :param time_limit: Conditions for how long the engine can search (e.g. we have 10 seconds and search up to depth 10).
        :param ponder: Whether the engine can ponder after playing a move.
        :param draw_offered: Whether the bot was offered a draw.
        :param root_moves: If it is a list, the engine should only play a move that is in `root_moves`.
        :return: The move to play.
        """
        if isinstance(time_limit.time, int):
            my_time = time_limit.time
            my_inc = 0
        elif board.turn == chess.WHITE:
            my_time = time_limit.white_clock if isinstance(time_limit.white_clock, int) else 0
            my_inc = time_limit.white_inc if isinstance(time_limit.white_inc, int) else 0
        else:
            my_time = time_limit.black_clock if isinstance(time_limit.black_clock, int) else 0
            my_inc = time_limit.black_inc if isinstance(time_limit.black_inc, int) else 0

        possible_moves = root_moves if isinstance(root_moves, list) else list(board.legal_moves)

        if my_time / 60 + my_inc > 10:
            # Choose a random move.
            move = random.choice(possible_moves)
        else:
            # Choose the first move alphabetically in uci representation.
            possible_moves.sort(key=str)
            move = possible_moves[0]
        return PlayResult(move, None, draw_offered=draw_offered)

#---


class MattysBot(ExampleEngine):
    def search(self,
               board: chess.Board,
               time_limit: Limit,
               ponder: bool,
               draw_offered: bool,
               root_moves: MOVE) -> PlayResult:

        start_time = time.time()
        time_cutoff = 0.3  # seconds

        depth = 2
        best_move = None

        if board.turn == chess.WHITE:
            maximizing_player = True
            best_eval = -float('inf')
        else:
            maximizing_player = False
            best_eval = float('inf')

        moves = root_moves if isinstance(root_moves, list) else list(board.legal_moves)

        for move in moves:
            # Time cutoff check
            if time.time() - start_time > time_cutoff:
                break

            board.push(move)
            eval = minimax(board, depth-1, -float('inf'), float('inf'),
                           not maximizing_player, start_time, time_cutoff)
            board.pop()

            if maximizing_player and eval > best_eval:
                best_eval = eval
                best_move = move
            elif not maximizing_player and eval < best_eval:
                best_eval = eval
                best_move = move

        if best_move is None:
            best_move = random.choice(list(board.legal_moves))

        # Draw acceptance logic
        if draw_offered and abs(best_eval) < 50:
            return PlayResult(None, None, draw_offered=True)

        return PlayResult(best_move, None)

        


# Determine if we are in an endgame
def is_endgame(board):
    pieces = list(board.piece_map().values())

    # Condition A: no queens on the board
    if not any(p.piece_type == chess.QUEEN for p in pieces):
        return True

    # Condition B: no rooks and at most two minor pieces total
    minor_count = sum(p.piece_type in (chess.BISHOP, chess.KNIGHT) for p in pieces)
    rook_count = sum(p.piece_type == chess.ROOK for p in pieces)

    if rook_count == 0 and minor_count <= 2:
        return True

    return False


# Material evaluation function with piece-square tables
def material_evaluation(board):
    endgame = is_endgame(board)
    score = 0

    piece_values = {
        chess.PAWN: 100,
        chess.KNIGHT: 320,
        chess.BISHOP: 330,
        chess.ROOK: 500,
        chess.QUEEN: 900,
        chess.KING: 20000
    }

    # Loop through every occupied square on the board
    for square, piece in board.piece_map().items():
        # Store the material value of the piece in "base value"
        base_value = piece_values[piece.piece_type]

        # Select correct PST
        if piece.piece_type == chess.KING:
            pst = KING_END_TABLE if endgame else KING_MIDDLE_TABLE
        else:
            pst = PIECE_SQUARE_TABLES[piece.piece_type]

        # Apply PST value to base material value
        if piece.color == chess.WHITE:
            pst_value = pst[square]
            score += base_value + pst_value
        # Mirror for black
        else:
            mirrored = chess.square_mirror(square)
            pst_value = pst[mirrored]
            score -= base_value + pst_value

    # Score will be positive if white is better, and negative if black is better
    return score

def minimax(board, depth, alpha, beta, maximizing_player, start_time, time_cutoff):
    # Base case: depth reached or game over
    if depth == 0 or board.is_game_over():
        return material_evaluation(board)

    # Time cutoff
    if time.time() - start_time > time_cutoff:
        return material_evaluation(board)

    if maximizing_player:
        value = -float('inf')
        for move in board.legal_moves:
            board.push(move)
            value = max(
                value,
                minimax(board, depth - 1, alpha, beta, False, start_time, time_cutoff)
            )
            board.pop()

            alpha = max(alpha, value)
            if alpha >= beta:
                break  # Beta cutoff
        return value

    else:
        value = float('inf')
        for move in board.legal_moves:
            board.push(move)
            value = min(
                value,
                minimax(board, depth - 1, alpha, beta, True, start_time, time_cutoff)
            )
            board.pop()

            beta = min(beta, value)
            if beta <= alpha:
                break  # Alpha cutoff
        return value
