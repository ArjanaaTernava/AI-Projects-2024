import chess
import math

def static_evaluation(board):
    material_values = {
        chess.PAWN: 1, chess.KNIGHT: 3, chess.BISHOP: 3, chess.ROOK: 5, chess.QUEEN: 9, chess.KING: 0
    }
    score = 0
    for piece_type, value in material_values.items():
        score += len(board.pieces(piece_type, chess.WHITE)) * value
        score -= len(board.pieces(piece_type, chess.BLACK)) * value
    return score

def minimax(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or board.is_game_over():
        return static_evaluation(board)

    if maximizing_player:
        max_eval = -math.inf
        for move in board.legal_moves:
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
        for move in board.legal_moves:
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

    for move in board.legal_moves:
        board.push(move)
        board_value = minimax(board, depth - 1, -math.inf, math.inf, not board.turn)
        board.pop()

        if (board.turn == chess.WHITE and board_value > best_value) or \
           (board.turn == chess.BLACK and board_value < best_value):
            best_value = board_value
            best_move = move

    return best_move

def print_board_with_labels(board):
    print("\n   a b c d e f g h")
    print("  -----------------")
    board_string = str(board).split("\n")
    for idx, row in enumerate(board_string):
        row_formatted = " ".join(row)  
        print(f"{8 - idx} | {row_formatted} | {8 - idx}")
    print("  -----------------")
    print("   a b c d e f g h\n")

# Main function
if __name__ == "__main__":
    fen = "r2r2k1/bpq3p1/1pn1p2p/2p4p/P1P1B3/2P1PN1P/2Q2PP1/R2R2K1 w - - 0 1"
    board = chess.Board(fen)

    print("Custom Initial Board:")
    print_board_with_labels(board)

    while True:
        try:
            depth = int(input("Enter search depth (e.g., 3-5): "))
            if depth > 0:
                break
            print("Depth must be a positive integer.")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

    best_move = find_best_move(board, depth)

    # Display results
    if best_move:
        print(f"\nBest Move: {best_move}")
        board.push(best_move)
        print("\nBoard After Best Move:")
        print_board_with_labels(board)
    else:
        print("\nNo valid moves found.")

