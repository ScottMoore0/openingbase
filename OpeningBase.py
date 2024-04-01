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
    positions = []

    if current_ply >= max_ply:
        return positions

    for move in board.legal_moves:
        board.push(move)
        if is_checkmate(board):
            if board.turn == chess.WHITE:
                positions.append((board.fen(), current_ply, '#W'))
            else:
                positions.append((board.fen(), current_ply, '#B'))
        else:
            positions.extend(find_checkmate_positions(board, max_ply, current_ply + 1))
        board.pop()

    return positions


def find_mate_positions(board, max_ply, current_ply=0):
    positions = []

    if current_ply >= max_ply:
        return positions

    for move in board.legal_moves:
        board.push(move)
        if is_mate_in_n(board, max_ply - current_ply):
            positions.append((board.fen(), current_ply, f'M{max_ply - current_ply}', board.turn))
        else:
            positions.extend(find_mate_positions(board, max_ply, current_ply + 1))
        board.pop()

    return positions


def find_all_positions(board, max_ply, current_ply=0):
    positions = []

    if current_ply > max_ply:
        return positions

    positions.append((board.fen(), current_ply, board.turn))

    if current_ply == max_ply:
        return positions

    for move in board.legal_moves:
        board.push(move)
        positions.extend(find_all_positions(board, max_ply, current_ply + 1))
        board.pop()

    return positions


def main():
    starting_position = chess.Board()
    max_ply = int(input("Enter the maximum ply to search: "))

    checkmate_positions = find_checkmate_positions(starting_position, max_ply)
    mate_positions = find_mate_positions(starting_position, max_ply)
    all_positions = find_all_positions(starting_position, max_ply)

    filename = f'openingbase (ply {max_ply}).txt'

    with open(filename, 'w') as f:
        for fen, ply, status in checkmate_positions:
            f.write(f"P{ply} {status} {fen}\n")
        for fen, ply, status, player in mate_positions:
            f.write(f"P{ply} {status}{'W' if player == chess.WHITE else 'B'} {fen}\n")
        for fen, ply, player in all_positions:
            f.write(f"P{ply}{'W' if player == chess.WHITE else 'B'} {fen}\n")

    print(
        f"{len(checkmate_positions) + len(mate_positions) + len(all_positions)} positions found up to ply {max_ply}. Saved to '{filename}'.")


if __name__ == "__main__":
    main()
