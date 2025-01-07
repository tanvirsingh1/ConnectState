import numpy as np
from copy import deepcopy
from meta import GameMeta

class ConnectState:
    def __init__(self):
        """
        Initializes the ConnectState with an empty board, sets the current player,
        initializes column heights, and tracks the last move made.
        """
        self.board = [[0 for _ in range(GameMeta.COLS)] for _ in range(GameMeta.ROWS)]
        self.current_player = GameMeta.PLAYERS['one']
        self.column_heights = [GameMeta.ROWS - 1 for _ in range(GameMeta.COLS)]
        self.last_move = None

    def get_board(self):
        """
        Returns a deep copy of the current board state.
        """
        return deepcopy(self.board)

    def make_move(self, col):
        """
        Makes a move in the specified column, updates the board, tracks the last move,
        adjusts column heights, and switches to the other player.
        """
        row = self.column_heights[col]
        self.board[row][col] = self.current_player
        self.last_move = (row, col)
        self.column_heights[col] -= 1
        self.current_player = GameMeta.PLAYERS['two'] if self.current_player == GameMeta.PLAYERS['one'] else GameMeta.PLAYERS['one']

    def available_moves(self):
        """
        Returns a list of columns that are not full and can accept a new move.
        """
        return [col for col in range(GameMeta.COLS) if self.board[0][col] == 0]

    def check_victory(self):
        """
        Checks if the last move resulted in a victory for the player who made the move.
        """
        if self.last_move and self.is_winning_move(self.last_move[0], self.last_move[1]):
            return self.board[self.last_move[0]][self.last_move[1]]
        return 0

    def is_winning_move(self, row, col):
        """
        Determines if the move at (row, col) resulted in a win by checking all possible
        directions: horizontal, vertical, and both diagonals.
        """
        player = self.board[row][col]

        # Horizontal check
        consecutive_count = 1
        for d in [-1, 1]:
            r, c = row, col
            while 0 <= c + d < GameMeta.COLS and self.board[r][c + d] == player:
                consecutive_count += 1
                c += d
        if consecutive_count >= 4:
            return True

        # Vertical check
        consecutive_count = 1
        for d in [-1, 1]:
            r, c = row, col
            while 0 <= r + d < GameMeta.ROWS and self.board[r + d][c] == player:
                consecutive_count += 1
                r += d
        if consecutive_count >= 4:
            return True

        # Diagonal checks
        for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            consecutive_count = 1
            r, c = row, col
            while 0 <= r + dr < GameMeta.ROWS and 0 <= c + dc < GameMeta.COLS and self.board[r + dr][c + dc] == player:
                consecutive_count += 1
                r += dr
                c += dc
            if consecutive_count >= 4:
                return True

        return False

    def is_game_over(self):
        """
        Checks if the game is over either by a win or a draw.
        """
        return self.check_victory() or not self.available_moves()

    def get_winner(self):
        """
        Returns the outcome of the game. If the game is a draw, it returns 'draw',
        otherwise it returns the winner ('one' or 'two').
        """
        if not self.available_moves() and self.check_victory() == 0:
            return GameMeta.OUTCOMES['draw']
        return GameMeta.OUTCOMES['one'] if self.check_victory() == GameMeta.PLAYERS['one'] else GameMeta.OUTCOMES['two']

    def display(self):
        """
        Displays the current board state in a formatted manner.
        """
        print('==============================')
        for row in range(GameMeta.ROWS):
            for col in range(GameMeta.COLS):
                token = 'X' if self.board[row][col] == GameMeta.PLAYERS['one'] else 'O' if self.board[row][col] == GameMeta.PLAYERS['two'] else ' '
                print(f'| {token} ', end='')
            print('|')
        print('==============================')
