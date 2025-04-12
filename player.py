from utils import is_on_board, remove_piece
from hex_board import HexBoard

class Player:
    def __init__(self, player_id: int):
        self.player_id = player_id

    def play(self, board: HexBoard) -> tuple:
        raise NotImplementedError("¡Implementa este método!")


class IAPlayer(Player):

    def __init__(self, player_id: int):
        super().__init__(player_id)
        self.opponent_id = 1 if player_id == 2 else 2

    def play(self, board: HexBoard) -> tuple:

        board_size = board.size
        middle = board_size // 2

        if board.board[middle][middle] == 0:
            return middle, middle
        elif board.board[middle][middle] == self.opponent_id and board.board[middle][middle - 1] == 0:
            return middle, middle - 1

        best_move = None
        best_score = -float('inf')

        def evaluate() -> int:

            def base_heuristic():
                max_score = -float('inf')
                diagonals = [(-1,1),(1,-1)]
                for i in range(board_size):
                    line_score = 0
                    for j in range(board.size):
                            row , col  = (i, j) if self.player_id == 1 else (j, i)
                            if board.board[row][col] == self.player_id:
                                line_score += 5
                            for d_row, d_col in diagonals:
                                if is_on_board(board_size, row + d_row, col + d_col) and board.board[row + d_row][col + d_col] == self.player_id:
                                    line_score += 2
                    max_score = max(max_score, line_score)

                return max_score

            def count_components(player):
                visited = [[False for _ in range(board_size)] for _ in range(board_size)]
                component_count = 0
                directions = [(-1,0), (1, 0), (0,-1), (0,1), (-1,1), (1,-1)]

                for i in range(board_size):
                    for j in range(board_size):
                        if board.board[i][j] == player and not visited[i][j]:
                            component_count += 1
                            stack =[(i,j)]
                            visited[i][j] = True

                            while stack:
                                r,c = stack.pop()
                                for dr, dc in directions:
                                      nr, nc = r + dr,c + dc
                                      if (is_on_board(board_size, nr , nc ) and
                                            not visited[nr][nc] and board.board[nr][nc] == player):
                                        visited[nr][nc] = True
                                        stack.append((nr, nc))
                return component_count

            own_components = count_components(self.player_id)
            opp_components = count_components(self.opponent_id)

            return base_heuristic() + (own_components - opp_components) * 2

        def minimax(depth , is_max=True, alpha=-float('inf'), beta=float('inf')):

            player_wins = board.check_connection(self.player_id)
            rival_win = board.check_connection(self.opponent_id)

            if player_wins:
                return 1000 + depth
            elif rival_win:
                return -1000 - depth
            elif depth == 0:
                return evaluate()

            if is_max:
                max_score = -float('inf')
                for local_move in board.get_possible_moves():
                    l_row, l_col = local_move
                    board.place_piece(l_row, l_col, self.player_id)
                    current_score = minimax(depth - 1, False, alpha, beta)
                    remove_piece(board.board, l_row, l_col)
                    max_score = max(max_score, current_score)
                    alpha = max(alpha, max_score)
                    if beta <= alpha:
                        break
                return max_score
            else:
                min_score = float('inf')
                for local_move in board.get_possible_moves():
                    l_row, l_col = local_move
                    board.place_piece(l_row, l_col, self.opponent_id)
                    current_score = minimax(depth - 1, True, alpha, beta)
                    remove_piece(board.board, l_row, l_col)
                    min_score = min(min_score, current_score)
                    beta = min(beta, min_score)
                    if beta <= alpha:
                        break
                return min_score

        moves = board.get_possible_moves()

        for move in moves:

            row, col = move
            board.place_piece(row, col, self.player_id)

            if len(moves) > 20:
                local_score = minimax(depth=2)
            elif len(moves) > 10:
                local_score = minimax(depth=4)
            else:
                local_score = minimax(depth=6)

            remove_piece(board.board, row, col)

            if local_score > best_score:
                best_score = local_score
                best_move = (row, col)

        return best_move
