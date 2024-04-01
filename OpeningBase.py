import chess


def is_checkmate(board):
    return board.is_checkmate()


def is_mate_in_n(board, n):
    if n <= 0:
        return False
    if n == 1:
        return is_checkmate(board)

    for move in board.legal_moves:
        board.push(move)
        if is_checkmate(board):
            board.pop()
            return True
        if not is_mate_in_n(board, n - 1):
            board.pop()
            return False
        board.pop()
    return False


def find_checkmate_positions(board, max_ply, current_ply=0):
    checkmate_positions = []

    if current_ply >= max_ply:
        return checkmate_positions

    for move in board.legal_moves:
        board.push(move)
        if is_checkmate(board):
            checkmate_positions.append((board.fen(), '#', board.turn))
        else:
            checkmate_positions.extend(find_checkmate_positions(board, max_ply, current_ply + 1))
        board.pop()

    return checkmate_positions


def find_mate_positions(board, max_ply, current_ply=0):
    mate_positions = []

    if current_ply >= max_ply:
        return mate_positions

    for move in board.legal_moves:
        board.push(move)
        if is_mate_in_n(board, max_ply - current_ply):
            mate_positions.append((board.fen(), f'M{max_ply - current_ply}', board.turn))
        else:
            mate_positions.extend(find_mate_positions(board, max_ply, current_ply + 1))
        board.pop()

    return mate_positions


def main():
    starting_position = chess.Board()
    max_ply = int(input("Enter the maximum ply to search: "))

    checkmate_positions = find_checkmate_positions(starting_position, max_ply)
    mate_positions = find_mate_positions(starting_position, max_ply)

    with open('openingbase.txt', 'w') as f:
        for position, status, player in checkmate_positions:
            f.write(f"{status} for {'W' if player == chess.WHITE else 'B'}: {position}\n")
        for position, status, player in mate_positions:
            f.write(f"{status} for {'W' if player == chess.WHITE else 'B'}: {position}\n")

    print(
        f"{len(checkmate_positions) + len(mate_positions)} positions found up to ply {max_ply}. Saved to 'openingbase.txt'.")


if __name__ == "__main__":
    main()