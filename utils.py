def remove_piece(board, row: int, col: int):
    board[row][col] = 0

def is_on_board(board_size ,row: int, col: int) -> bool:
    return 0 <= row < board_size and 0 <= col < board_size
