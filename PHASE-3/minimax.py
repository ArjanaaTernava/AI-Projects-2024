import chess
import math

PIECE_WEIGHTS = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 0
}

def static_evaluation(board):
    """Evaluate the board state based on material, king safety, and mobility."""
    score = 0
    for piece_type, weight in PIECE_WEIGHTS.items():
        score += len(board.pieces(piece_type, chess.WHITE)) * weight
        score -= len(board.pieces(piece_type, chess.BLACK)) * weight

    if not board.has_kingside_castling_rights(chess.WHITE):
        score -= 1
    if not board.has_kingside_castling_rights(chess.BLACK):
        score += 1

    central_squares = [chess.D4, chess.D5, chess.E4, chess.E5]
    for square in central_squares:
        piece = board.piece_at(square)
        if piece:
            if piece.color == chess.WHITE:
                score += 0.5
            else:
                score -= 0.5

    score += len(list(board.legal_moves)) if board.turn == chess.WHITE else -len(list(board.legal_moves))

    return score


def order_moves(board, moves):
    """Order moves to improve alpha-beta pruning effectiveness."""
    def move_priority(move):
        if board.is_capture(move):
            return 10  
        if board.gives_check(move):
            return 5   
        return 1     

    return sorted(moves, key=move_priority, reverse=True)


def minimax(board, depth, alpha, beta, maximizing_player):
    """Minimax algorithm with alpha-beta pruning."""
    if depth == 0 or board.is_game_over():
        return static_evaluation(board)

    moves = list(board.legal_moves)
    moves = order_moves(board, moves)

    if maximizing_player:
        max_eval = -math.inf
        for move in moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = math.inf
        for move in moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, True)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval


def find_best_move(board, depth):
    best_move = None
    best_value = -math.inf if board.turn == chess.WHITE else math.inf

    moves = list(board.legal_moves)
    moves = order_moves(board, moves)

    for move in moves:
        board.push(move)
        board_value = minimax(board, depth - 1, -math.inf, math.inf, not board.turn)
        board.pop()

        if board.turn == chess.WHITE and board_value > best_value:
            best_value = board_value
            best_move = move
        elif board.turn == chess.BLACK and board_value < best_value:
            best_value = board_value
            best_move = move

    print(f"Evaluated {len(moves)} moves at depth {depth}. Best move: {best_move}, Score: {best_value}")
    return best_move


def print_board_with_labels(board):
    """Print the board with coordinates for clarity."""
    print("\n    a   b   c   d   e   f   g   h")
    print("  ------------------------------------")
    board_string = str(board).split("\n")
    for idx, row in enumerate(board_string):
        row_formatted = " ".join(row)
        print(f"{8 - idx} | {row_formatted} | {8 - idx}")
    print("  ------------------------------------")
    print("    a   b   c   d   e   f   g   h\n")


if __name__ == "__main__":

    fen = "r2qk2r/2pb4/ppn2p1b/3ppnpp/PP6/N1PBPQPN/1B1P1P1P/R4RK1 w - - 0 1"
    try:
        board = chess.Board(fen)
    except ValueError:
        print("Invalid FEN string. Please check the configuration.")
        exit(1)

    print("Custom Initial Board:")
    print_board_with_labels(board)

    while True:
        try:
            depth = int(input("Enter search depth: "))
            if depth > 0:
                break
            print("Depth must be a positive integer.")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

    print("\nStarting Iterative Deepening Search...")
    best_move = None
    for current_depth in range(1, depth + 1):
        print(f"\nSearching at Depth {current_depth}...")
        best_move = find_best_move(board, current_depth)
        print("-" * 40)

    if best_move:
        print(f"\nFinal Best Move at Depth {depth}: {best_move}")
        board.push(best_move)
        print("\nBoard After Best Move:")
        print_board_with_labels(board)
    else:
        print("\nNo valid moves found.")

    if board.is_checkmate():
        print("Game Over: Checkmate!")
    elif board.is_stalemate():
        print("Game Over: Stalemate!")
    elif board.is_insufficient_material():
        print("Game Over: Draw due to insufficient material!")
    elif board.is_seventyfive_moves():
        print("Game Over: Draw due to 75-move rule!")
    elif board.is_fivefold_repetition():
        print("Game Over: Draw due to fivefold repetition!")
    else:
        print("Game is ongoing.")
