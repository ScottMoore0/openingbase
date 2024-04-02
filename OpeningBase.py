import chess
import csv
import time


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
    positions = {}

    if current_ply >= max_ply:
        return positions

    for move in board.legal_moves:
        board.push(move)
        if is_checkmate(board):
            key = custom_fen(board)
            if key not in positions or positions[key][0] > current_ply:
                if board.turn == chess.WHITE:
                    positions[key] = (current_ply, '#', 'W')
                else:
                    positions[key] = (current_ply, '#', 'B')
        else:
            positions.update(find_checkmate_positions(board, max_ply, current_ply + 1))
        board.pop()

    return positions


def find_mate_positions(board, max_ply, current_ply=0):
    positions = {}

    if current_ply >= max_ply:
        return positions

    for move in board.legal_moves:
        board.push(move)
        if is_mate_in_n(board, max_ply - current_ply):
            key = custom_fen(board)
            if key not in positions or positions[key][0] > current_ply:
                positions[key] = (current_ply, f'M{max_ply - current_ply}', 'W' if board.turn == chess.WHITE else 'B')
        else:
            positions.update(find_mate_positions(board, max_ply, current_ply + 1))
        board.pop()

    return positions


def find_all_positions(board, max_ply, current_ply=0, visited=set()):
    positions = {}

    if current_ply > max_ply:
        return positions

    key = custom_fen(board)
    if key not in visited:
        visited.add(key)
        positions[key] = (current_ply, '', 'W' if board.turn == chess.WHITE else 'B')

        if current_ply == max_ply:
            return positions

        for move in board.legal_moves:
            board.push(move)
            positions.update(find_all_positions(board, max_ply, current_ply + 1, visited))
            board.pop()

    return positions


def custom_fen(board):
    return ' '.join(board.fen().split(' ')[:4])


def main():
    starting_position = chess.Board()
    max_ply = int(input("Enter the maximum ply to search: "))

    start_time = time.time()

    checkmate_positions = find_checkmate_positions(starting_position, max_ply)
    mate_positions = find_mate_positions(starting_position, max_ply)
    all_positions = find_all_positions(starting_position, max_ply)

    filename = f'openingbase (ply {max_ply}).csv'

    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['ply number', 'mate status', 'to move', 'FEN string'])
        positions = {}
        positions.update(checkmate_positions)
        positions.update(mate_positions)
        positions.update(all_positions)
        unique_positions = {}
        for key, value in sorted(positions.items()):
            if key not in unique_positions or value[0] < unique_positions[key][0]:
                unique_positions[key] = value
        for key, value in sorted(unique_positions.items()):
            ply, status, to_move = value
            writer.writerow([ply, status, to_move, key])

    end_time = time.time()

    print(
        f"{len(unique_positions)} unique positions found up to ply {max_ply}. Saved to '{filename}'."
        f"\nTime taken: {end_time - start_time:.2f} seconds.")


if __name__ == "__main__":
    main()
