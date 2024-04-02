import chess
import csv
import time

def generate_custom_fen(board):
    piece_placement = board.board_fen().split()[0]
    active_color = 'w' if board.turn == chess.WHITE else 'b'
    castling_rights = ''.join([
        'K' if board.has_kingside_castling_rights(chess.WHITE) else '',
        'Q' if board.has_queenside_castling_rights(chess.WHITE) else '',
        'k' if board.has_kingside_castling_rights(chess.BLACK) else '',
        'q' if board.has_queenside_castling_rights(chess.BLACK) else ''
    ]) or '-'
    ep_square = board.ep_square
    en_passant = chess.SQUARE_NAMES[ep_square] if ep_square is not None else '-'
    custom_fen = f"{piece_placement} {active_color} {castling_rights} {en_passant}"
    return custom_fen

def count_checkmates(board, depth, max_depth, positions, search_mate_in_1, unique_checkmates, unique_mate_in_2, unique_mate_in_3, unique_mate_in_4):
    if depth == 0:
        if board.is_checkmate():
            custom_fen = generate_custom_fen(board)
            if custom_fen not in positions or (custom_fen in positions and positions[custom_fen][0] > max_depth - depth + 1):
                positions[custom_fen] = (max_depth - depth + 1, 'M1')
                unique_checkmates.add(custom_fen)
        return board.is_checkmate(), 0, 0, 0, 0

    checkmate_count = 0
    mate_in_1_count = 0
    mate_in_2_count = 0
    mate_in_3_count = 0
    mate_in_4_count = 0
    legal_moves = board.legal_moves
    unique_positions = set()
    for move in legal_moves:
        if depth <= max_depth:
            board.push(move)
            if board.is_checkmate():
                checkmate_count += 1
                custom_fen = generate_custom_fen(board)
                if custom_fen not in unique_positions:
                    unique_positions.add(custom_fen)
                    if custom_fen not in positions or (custom_fen in positions and positions[custom_fen][0] > max_depth - depth + 1):
                        positions[custom_fen] = (max_depth - depth + 1, '#')
                        unique_checkmates.add(custom_fen)
            elif search_mate_in_1 and board.is_check():
                mate_in_1_count += 1
                custom_fen = generate_custom_fen(board)
                if custom_fen not in unique_positions:
                    unique_positions.add(custom_fen)
                    if custom_fen not in positions or (custom_fen in positions and positions[custom_fen][0] > max_depth - depth + 1):
                        positions[custom_fen] = (max_depth - depth, 'M1')
            else:
                sub_checkmate_count, sub_mate_in_1_count, sub_mate_in_2_count, sub_mate_in_3_count, sub_mate_in_4_count = count_checkmates(board, depth - 1, max_depth, positions, search_mate_in_1, unique_checkmates, unique_mate_in_2, unique_mate_in_3, unique_mate_in_4)
                checkmate_count += sub_checkmate_count
                mate_in_1_count += sub_mate_in_1_count
                mate_in_2_count += sub_mate_in_2_count
                mate_in_3_count += sub_mate_in_3_count
                mate_in_4_count += sub_mate_in_4_count
            board.pop()
    if depth == max_depth - 1:
        unique_checkmates.update(unique_positions)
    elif depth == max_depth - 2:
        unique_mate_in_2.update(unique_positions)
    elif depth == max_depth - 3:
        unique_mate_in_3.update(unique_positions)
    elif depth == max_depth - 4:
        unique_mate_in_4.update(unique_positions)
    return len(unique_positions), mate_in_1_count, mate_in_2_count, mate_in_3_count, mate_in_4_count

def main():
    max_depth = int(input("Enter the maximum depth (number of plies): "))
    starting_position = chess.Board()
    total_checkmates = 0
    unique_positions = 0
    prev_unique_positions = 0

    start_time = time.time()

    positions = {}
    unique_checkmates = set()
    unique_mate_in_2 = set()
    unique_mate_in_3 = set()
    unique_mate_in_4 = set()
    for depth in range(1, max_depth + 1):
        if depth == max_depth:
            search_mate_in_1 = False
        else:
            search_mate_in_1 = True
        unique_positions, mate_in_1_count, mate_in_2_count, mate_in_3_count, mate_in_4_count = count_checkmates(starting_position.copy(), depth, max_depth, positions, search_mate_in_1, unique_checkmates, unique_mate_in_2, unique_mate_in_3, unique_mate_in_4)
        print(f"Number of unique checkmate positions at {depth} plies: {len(unique_checkmates) - prev_unique_positions}")
        print(f"Number of unique mate-in-1 positions at {depth} plies: {mate_in_1_count}")
        if depth < max_depth - 1:
            print(f"Number of unique mate-in-2 positions at {depth} plies: {mate_in_2_count}")
        if depth < max_depth - 2:
            print(f"Number of unique mate-in-3 positions at {depth} plies: {mate_in_3_count}")
        if depth < max_depth - 3:
            print(f"Number of unique mate-in-4 positions at {depth} plies: {mate_in_4_count}")
        prev_unique_positions = len(unique_checkmates)

    filename = f"checkmate_positions_ply_{max_depth}.csv"
    with open(filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Ply', 'Mate', 'FEN'])
        for custom_fen, (ply, mate) in positions.items():
            csv_writer.writerow([ply, mate, custom_fen])
        for custom_fen in unique_mate_in_2:
            csv_writer.writerow([max_depth - 2, 'M2', custom_fen])
        for custom_fen in unique_mate_in_3:
            csv_writer.writerow([max_depth - 3, 'M3', custom_fen])
        for custom_fen in unique_mate_in_4:
            csv_writer.writerow([max_depth - 4, 'M4', custom_fen])

    end_time = time.time()

    print(f"Total number of checkmate positions found: {len(unique_checkmates)}")
    print(f"CSV file '{filename}' generated successfully.")

    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time:.2f} seconds")

if __name__ == "__main__":
    main()
