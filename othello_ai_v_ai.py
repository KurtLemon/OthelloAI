import copy
import threading
import random
import sys


class Othello:
    def __init__(self):
        self.theta = [.25, .25, .25, .25]
        self.board = [['*' for _ in range(8)] for _ in range(8)]
        self.backup_board = copy.deepcopy(self.board)

    def generate_start(self):
        self.board[3][3] = 'W'
        self.board[3][4] = 'B'
        self.board[4][3] = 'B'
        self.board[4][4] = 'W'
        self.backup_board = copy.deepcopy(self.board)

    def generate_start_2(self):
        self.board[3][3] = 'B'
        self.board[3][4] = 'W'
        self.board[4][3] = 'W'
        self.board[4][4] = 'B'
        self.backup_board = copy.deepcopy(self.board)

    def print_board(self):
        print("   _A__B__C__D__E__F__G__H_")
        for i in range(len(self.board)):
            print(i + 1, '|', end='')
            for piece in self.board[i]:
                print(' ', end='')
                print(piece, end=' ')
            print()

    def print_backup_board(self):
        print("   _A__B__C__D__E__F__G__H_")
        for i in range(len(self.backup_board)):
            print(i + 1, '|', end='')
            for piece in self.backup_board[i]:
                print(' ', end='')
                print(piece, end=' ')
            print()

    def print_both_boards(self):
        print("  New Board Configuration", "        Old Board Configuration")
        print("   _A__B__C__D__E__F__G__H_", "      _A__B__C__D__E__F__G__H_")
        for i in range(len(self.board)):
            print(i + 1, '|', end='')
            for piece in self.board[i]:
                print(' ', end='')
                print(piece, end=' ')
            print('   ', i + 1, '|', end='')
            for piece in self.backup_board[i]:
                print(' ', end='')
                print(piece, end=' ')
            print()

    def game(self):
        turns = 1
        print("Welcome to Othello, Black goes first")
        # Create function to see if there are any moves left
        moves_left = self.spaces_available()
        while moves_left:
            print("Turn #", turns)
            turns += 1
            self.print_scores()
            self.print_board()
            print()
            if self.valid_moves_exist('B', 'W'):
                print()
                should_have_turn = True
                while should_have_turn:
                    timer = threading.Timer(10, self.time_out)
                    timer.start()
                    # AI TAKES TURN
                    self.ai_turn('B', 'W')
                    timer.cancel()
                    should_have_turn = False
                    self.backup_board = copy.deepcopy(self.board)
            else:
                print("No valid moves for Black available")
            if self.valid_moves_exist('W', 'B'):
                should_have_turn = True
                while should_have_turn:
                    timer = threading.Timer(10, self.time_out)
                    timer.start()
                    # AI TAKES TURN
                    self.ai_turn('W', 'B')
                    timer.cancel()
                    should_have_turn = False
                    self.backup_board = copy.deepcopy(self.board)
            else:
                print("No valid moves for White available")
            moves_left = self.spaces_available() and \
                (self.valid_moves_exist('B', 'W') or self.valid_moves_exist('W', 'B'))
        self.end_game_win()

    def end_game_win(self):
        black_count = 0
        white_count = 0
        for row in self.board:
            for piece in row:
                if piece == 'B':
                    black_count += 1
                elif piece == 'W':
                    white_count += 1
        print("****************************")
        if black_count > white_count:
            print("Black wins!")
        elif white_count > black_count:
            print("White wins!")
        else:
            print("Tie.")
        self.print_scores()

    def time_out(self):
        print("10s has elapsed for AI player. AI loses.")
        self.print_scores()
        quit()

    def get_ai_player(self):
        player_input = input("Which Color should the AI have? (b, w)")
        while player_input != 'b' and player_input != 'B' and player_input != 'w' and player_input != 'W':
            player_input = input("Invalid input. Which Color should the AI have? (b, w)")
        return player_input.lower()

    def confirm_move(self):
        print("Confirm Move:")
        self.print_both_boards()
        acc_input = input("Accept New Board? (y, n)")
        while acc_input != 'y' and acc_input != 'Y' and acc_input != 'n' and acc_input != 'N':
            acc_input = input("Invalid input. Accept New Board? (y, n)")
        if acc_input == 'y' or acc_input == 'Y':
            self.backup_board = copy.deepcopy(self.board)
            return True
        if acc_input == 'n' or acc_input == 'N':
            self.board = copy.deepcopy(self.backup_board)
        return False

    def spaces_available(self):
        for row in self.board:
            if '*' in row:
                return True
        return False

    def print_scores(self):
        print("Black Score: ", self.get_score('B'))
        print("White Score: ", self.get_score('W'))

    def get_score(self, piece):
        total = 0
        for row in self.board:
            for space in row:
                if space == piece:
                    total += 1
        return total

    def valid_moves_exist(self, piece, opponent):
        directions = ['up', 'down', 'left', 'right', 'up-left', 'up-right', 'down-left', 'down-right']
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                if self.board[y][x] == '*':
                    for direction in directions:
                        if self.check_for_pieces(piece, opponent, x, y, direction):
                            return True
        return False

    def ai_turn(self, piece, opponent):
        max_value = -sys.maxsize - 1
        max_x = 0
        max_y = 0
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                valid_move, message = self.validate_move(x, y, piece, opponent)
                if valid_move:
                    test_value = self.h_x(x, y, piece, opponent)
                    if test_value >= max_value:
                        max_value = test_value
                        max_x = x
                        max_y = y
        self.place_piece(max_x, max_y, piece)
        self.flip_pieces(max_x, max_y, piece, opponent)

    def h_x(self, x, y, piece, opponent):
        return self.theta[0] * self.heuristic_parity(x, y, piece, opponent) + \
               self.theta[1] * self.heuristic_mobility(x, y, piece, opponent) + \
               self.theta[2] * self.heuristic_corners(x, y, piece, opponent) + \
               self.theta[3] * self.heuristic_stability(x, y, piece, opponent)

    def ai_turn_random(self, piece, opponent):
        x = random.randint(0, 8)
        y = random.randint(0, 8)
        valid_move, message = self.validate_move(x, y, piece, opponent)
        while not valid_move:
            x = random.randint(0, 8)
            y = random.randint(0, 8)
            valid_move, message = self.validate_move(x, y, piece, opponent)
        self.place_piece(x, y, piece)
        self.flip_pieces(x, y, piece, opponent)

    def heuristic_parity(self, x, y, piece, opponent):
        self.place_piece(x, y, piece)
        self.flip_pieces(x, y, piece, opponent)
        piece_score = self.get_score(piece)
        opponent_score = self.get_score(opponent)
        value = 0
        if piece_score + opponent_score != 0:
            value = 100 * (piece_score - opponent_score) / (piece_score + opponent_score)
        self.board = copy.deepcopy(self.backup_board)
        return value

    def heuristic_mobility(self, x, y, piece, opponent):
        self.place_piece(x, y, piece)
        self.flip_pieces(x, y, piece, opponent)
        piece_move_count = 0
        opponent_move_count = 0
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                valid_move, message = self.validate_move(x, y, piece, opponent)
                if valid_move:
                    piece_move_count += 1
                valid_move, message = self.validate_move(x, y, opponent, piece)
                if valid_move:
                    opponent_move_count += 1
        value = 0
        if piece_move_count + opponent_move_count != 0:
            value = 100 * (piece_move_count - opponent_move_count) / (piece_move_count + opponent_move_count)
        self.board = copy.deepcopy(self.backup_board)
        return value

    def heuristic_corners(self, x, y, piece, opponent):
        self.place_piece(x, y, piece)
        self.flip_pieces(x, y, piece, opponent)
        value = 0
        if x == 0 or x == 7:
            if y == 0 or y == 7:
                value = 100
        self.board = copy.deepcopy(self.backup_board)
        return value

    def heuristic_stability(self, x, y, piece, opponent):
        self.place_piece(x, y, piece)
        self.flip_pieces(x, y, piece, opponent)

        opponent_left = False
        stable_left = True
        opponent_right = False
        stable_right = True
        horizontal_stability = 0
        opponent_up = False
        stable_up = True
        opponent_down = False
        stable_down = True
        vertical_stability = 0
        opponent_up_right = False
        stable_up_right = True
        opponent_down_left = False
        stable_down_left = True
        diagonal_up_stability = 0
        opponent_up_left = False
        stable_up_left = True
        opponent_down_right = False
        stable_down_right = True
        diagonal_down_stability = 0

        # Check up
        for dy in range(y - 1, -1, -1):
            if self.board[dy][x] == opponent:
                opponent_up = True
                stable_up = False
            if  self.board[dy][x] == '*':
                stable_up = False

        # Check down
        for dy in range(y + 1, 8):
            if self.board[dy][x] == opponent:
                opponent_down = True
                stable_down = False
            if self.board[dy][x] == '*':
                stable_down = False

        # Check left
        for dx in range(x - 1, -1, -1):
            if self.board[y][dx] == opponent:
                opponent_left = True
                stable_left = False
            if self.board[y][dx] == '*':
                stable_left = False

        # Check right
        for dx in range(x + 1, 8):
            if self.board[y][dx] == opponent:
                opponent_right = True
                stable_right = False
            if self.board[y][dx] == '*':
                stable_right = False

        # Check up-left
        d = 1
        while x - d >= 0 and y - d >= 0:
            if self.board[y - d][x - d] == opponent:
                opponent_up_left = True
                stable_up_left = False
            if self.board[y - d][x - d] == '*':
                stable_up_left = False
            d += 1

        # Check down-right
        d = 1
        while x + d < 8 and y + d < 8:
            if self.board[y + d][x + d] == opponent:
                opponent_down_right = True
                stable_down_right = False
            if self.board[y - d][x - d] == '*':
                stable_down_right = False
            d += 1

        # Check down-left
        d = 1
        while x - d >= 0 and y + d < 8:
            if self.board[y + d][x - d] == opponent:
                opponent_down_left = True
                stable_down_left = False
            if self.board[y + d][x - d] == '*':
                stable_down_left = False
            d += 1

        # Check up-right
        d = 1
        while x + d < 8 and y - d >= 0:
            if self.board[y - d][x + d] == opponent:
                opponent_right = True
                stable_up_right = False
            if self.board[y - d][x + d] == '*':
                stable_up_right = False
            d += 1

        if stable_down or stable_up:
            vertical_stability = 2
        elif opponent_up and opponent_down:
            vertical_stability = 1

        if stable_left or stable_right:
            horizontal_stability = 2
        elif opponent_left and opponent_right:
            horizontal_stability = 2

        if stable_down_left or stable_up_right:
            diagonal_up_stability = 2
        elif opponent_down_left and opponent_up_right:
            diagonal_up_stability = 1

        if stable_down_right or stable_up_left:
            diagonal_down_stability = 2
        elif opponent_down_right and opponent_up_left:
            diagonal_down_stability = 1

        self.board = copy.deepcopy(self.backup_board)

        return 100 * (vertical_stability + horizontal_stability + diagonal_down_stability + diagonal_up_stability) / 8

    def turn(self, piece, opponent):
        # Display Board state for the player
        self.print_board()

        # Take in user input
        x = input("X [A, H]: ")
        y = input("Y [1, 8]: ")

        # Convert user input to proper indexing values
        x = self.char_to_int_index(x)
        y = int(y) - 1

        # Validate move
        valid_move, message = self.validate_move(x, y, piece, opponent)
        while not valid_move:
            print(message, "enter another move.")

            # Take in user input
            x = input("X [A, H]: ")
            y = input("Y (1, 8): ")

            # Convert user input to proper indexing values
            x = self.char_to_int_index(x)
            y = int(y) - 1
            valid_move, message = self.validate_move(x, y, piece, opponent)

        self.place_piece(x, y, piece)
        self.flip_pieces(x, y, piece, opponent)

    def check_for_pieces(self, piece, opponent, x, y, mode):
        if mode == 'up':
            if y <= 1:
                return False
            if self.board[y - 1][x] != opponent:
                return False
            for dy in range(y - 2, -1, -1):
                if self.board[dy][x] == '*':
                    return False
                if self.board[dy][x] == piece:
                    return True
            return False
        if mode == 'down':
            if y >= 6:
                return False
            if self.board[y + 1][x] != opponent:
                return False
            for dy in range(y + 2, 8):
                if self.board[dy][x] == '*':
                    return False
                if self.board[dy][x] == piece:
                    return True
            return False
        if mode == 'left':
            if x <= 1:
                return False
            if self.board[y][x - 1] != opponent:
                return False
            for dx in range(x - 2, -1, -1):
                if self.board[y][dx] == '*':
                    return False
                if self.board[y][dx] == piece:
                    return True
            return False
        if mode == 'right':
            if x >= 6:
                return False
            if self.board[y][x + 1] != opponent:
                return False
            for dx in range(x + 2, 8):
                if self.board[y][dx] == '*':
                    return False
                if self.board[y][dx] == piece:
                    return True
            return False
        if mode == 'up-left':
            if y <= 1 or x <= 1:
                return False
            if self.board[y - 1][x - 1] != opponent:
                return False
            d = 2
            while x - d >= 0 and y - d >= 0:
                if self.board[y - d][x - d] == '*':
                    return False
                if self.board[y - d][x - d] == piece:
                    return True
                d += 1
            return False
        if mode == 'up-right':
            if y <= 1 or x >= 6:
                return False
            if self.board[y - 1][x + 1] != opponent:
                return False
            d = 2
            while x + d < 8 and y - d >= 0:
                if self.board[y - d][x + d] == '*':
                    return False
                if self.board[y - d][x + d] == piece:
                    return True
                d += 1
            return False
        if mode == 'down-left':
            if y >= 6 or x <= 1:
                return False
            if self.board[y + 1][x - 1] != opponent:
                return False
            d = 2
            while x - d >= 0 and y + d < 8:
                if self.board[y + d][x - d] == '*':
                    return False
                if self.board[y + d][x - d] == piece:
                    return True
                d += 1
            return False
        if mode == 'down-right':
            if y >= 6 or x >= 6:
                return False
            if self.board[y + 1][x + 1] != opponent:
                return False
            d = 2
            while x + d < 8 and y + d < 8:
                if self.board[y + d][x + d] == '*':
                    return False
                if self.board[y + d][x + d] == piece:
                    return True
                d += 1
            return False
        return False

    def place_piece(self, x, y, piece):
        self.board[y][x] = piece

    def flip_pieces(self, x, y, piece, opponent):
        if self.check_for_pieces(piece, opponent, x, y, 'up'):
            dy = y - 1
            while self.board[dy][x] == opponent:
                self.board[dy][x] = piece
                dy -= 1
        if self.check_for_pieces(piece, opponent, x, y, 'down'):
            dy = y + 1
            while self.board[dy][x] == opponent:
                self.board[dy][x] = piece
                dy += 1
        if self.check_for_pieces(piece, opponent, x, y, 'left'):
            dx = x - 1
            while self.board[y][dx] == opponent:
                self.board[y][dx] = piece
                dx -= 1
        if self.check_for_pieces(piece, opponent, x, y, 'right'):
            dx = x + 1
            while self.board[y][dx] == opponent:
                self.board[y][dx] = piece
                dx += 1
        if self.check_for_pieces(piece, opponent, x, y, 'up-left'):
            dy = y - 1
            dx = x - 1
            while self.board[dy][dx] == opponent:
                self.board[dy][dx] = piece
                dy -= 1
                dx -= 1
        if self.check_for_pieces(piece, opponent, x, y, 'up-right'):
            dy = y - 1
            dx = x + 1
            while self.board[dy][dx] == opponent:
                self.board[dy][dx] = piece
                dy -= 1
                dx += 1
        if self.check_for_pieces(piece, opponent, x, y, 'down-left'):
            dy = y + 1
            dx = x - 1
            while self.board[dy][dx] == opponent:
                self.board[dy][dx] = piece
                dy += 1
                dx -= 1
        if self.check_for_pieces(piece, opponent, x, y, 'down-right'):
            dy = y + 1
            dx = x + 1
            while self.board[dy][dx] == opponent:
                self.board[dy][dx] = piece
                dy += 1
                dx += 1

    def validate_move(self, x, y, piece, opponent):
        # Check location is open
        if x < 0 or x > 7 or y < 0 or y > 7:
            return False, "Invalid move"
        if not self.board[y][x] == '*':
            return False, "Location is taken"

        directions = ['up', 'down', 'left', 'right', 'up-left', 'up-right', 'down-left', 'down-right']

        for direction in directions:
            if self.check_for_pieces(piece, opponent, x, y, direction):
                return True, "Move is good in direction " + direction

        return False, "No pieces captured by this move"

    def char_to_int_index(self, c):
        if c == 'A' or c == 'a':
            return 0
        if c == 'B' or c == 'b':
            return 1
        if c == 'C' or c == 'c':
            return 2
        if c == 'D' or c == 'd':
            return 3
        if c == 'E' or c == 'e':
            return 4
        if c == 'F' or c == 'f':
            return 5
        if c == 'G' or c == 'g':
            return 6
        if c == 'H' or c == 'h':
            return 7
        return -1


def main():
    othello = Othello()
    othello.generate_start()
    othello.game()
    othello.print_board()


def get_start_position():
    player_input = input("Which configuration do you want to start with?\n1:  2:\nWB  BW\nBW  WB")
    while player_input != '1' and player_input != '2':
        player_input = input("Invalid input. Which configuration do you want to start with?\n1:  2:\nWB  BW\nBW  WB")
    return player_input


if __name__ == '__main__':
    main()
