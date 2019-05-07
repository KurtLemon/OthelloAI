import copy
import threading
import random
import sys


class Othello:

    # ******************************************************************************************************************
    # INITIALIZATION AND BOARD STATE GENERATION
    # ******************************************************************************************************************

    # Initialize the board and backup board data structures, populating them to be totally empty.
    def __init__(self):
        self.theta = [.25, .25, .25, .25]
        self.board = [['*' for _ in range(8)] for _ in range(8)]
        self.backup_board = copy.deepcopy(self.board)

    # Populate the board with the initial configuration of pieces. * = available space, B = black occupied space,
    #   W = white occupied space. The mode indicates which configuration to use between
    #       WB         BW
    #       BW   and   WB
    def generate_start(self, mode):
        if mode == 1:
            self.board[3][3] = 'W'
            self.board[3][4] = 'B'
            self.board[4][3] = 'B'
            self.board[4][4] = 'W'
        elif mode == 2:
            self.board[3][3] = 'B'
            self.board[3][4] = 'W'
            self.board[4][3] = 'W'
            self.board[4][4] = 'B'
        self.backup_board = copy.deepcopy(self.board)

    # Prints out the state of the board that is currently in play.
    def print_board(self):
        print("   _A__B__C__D__E__F__G__H_")
        for i in range(len(self.board)):
            print(i + 1, '|', end='')
            for piece in self.board[i]:
                print(' ', end='')
                print(piece, end=' ')
            print()

    # Prints out the state of the back-up board.
    def print_backup_board(self):
        print("   _A__B__C__D__E__F__G__H_")
        for i in range(len(self.backup_board)):
            print(i + 1, '|', end='')
            for piece in self.backup_board[i]:
                print(' ', end='')
                print(piece, end=' ')
            print()

    # Prints out the state of a board that is passed in as an argument.
    def print_board_from_board_state(self, board_state):
        print("   _A__B__C__D__E__F__G__H_")
        for i in range(len(board_state)):
            print(i + 1, '|', end='')
            for piece in board_state[i]:
                print(' ', end='')
                print(piece, end=' ')
            print()

    # Prints out the saved board states as well as the backup board state side-by-side.
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

    # Prints the scores of each player at any point.
    def print_scores(self):
        print("Black Score: ", self.get_score('B'))
        print("White Score: ", self.get_score('W'))

    # Prints out information about who won the game.
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

    # ******************************************************************************************************************
    # GAME PLAYING LOGIC
    # ******************************************************************************************************************

    # The main game-playing logic for following through turns between players.
    def game(self):
        ai_player_token = self.get_ai_player()
        print("Welcome to Othello, Black goes first")
        moves_left = self.spaces_available()
        while moves_left:
            if self.valid_moves_exist('B', 'W'):
                print()
                should_have_turn = True
                while should_have_turn:
                    print("Black's Turn")
                    self.print_scores()
                    timer = threading.Timer(10, self.time_out)
                    if ai_player_token == 'b':
                        timer.start()
                        # AI TAKES TURN
                        self.ai_turn('B', 'W')
                        timer.cancel()
                    else:
                        self.turn('B', 'W')
                    should_have_turn = not self.confirm_move()
            else:
                print("No valid moves for Black available")
            if self.valid_moves_exist('W', 'B'):
                print()
                should_have_turn = True
                while should_have_turn:
                    print("White's Turn")
                    self.print_scores()
                    timer = threading.Timer(10, self.time_out)
                    if ai_player_token == 'w':
                        timer.start()
                        # AI TAKES TURN
                        self.ai_turn('W', 'B')
                        timer.cancel()
                    else:
                        self.turn('W', 'B')
                    should_have_turn = not self.confirm_move()
            else:
                print("No valid moves for White available")
            moves_left = self.spaces_available() and \
                (self.valid_moves_exist('B', 'W') or self.valid_moves_exist('W', 'B'))
        self.end_game_win()

    # ******************************************************************************************************************
    # TIMING AND AI THREADING CONTROL
    # ******************************************************************************************************************

    # Callback function for the timer. Quits the game if too much time has elapsed and displays scores.
    def time_out(self):
        print("10s has elapsed for AI player. AI loses.")
        self.print_scores()
        quit()

    # ******************************************************************************************************************
    # GETTING INFORMATION FROM THE USER
    # ******************************************************************************************************************

    # Gets the identity of the AI player from the user.
    def get_ai_player(self):
        player_input = input("Which Color should the AI have? (b, w)")
        while player_input != 'b' and player_input != 'B' and player_input != 'w' and player_input != 'W':
            player_input = input("Invalid input. Which Color should the AI have? (b, w)")
        return player_input.lower()

    # After a user or AI moves, presents the user with the old and new board configurations and asks for confirmation.
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

    # ******************************************************************************************************************
    # MOVE AND GAME VALIDATION
    # ******************************************************************************************************************

    # Determines if there are any open spaces on the board.
    def spaces_available(self):
        for row in self.board:
            if '*' in row:
                return True
        return False

    # Determines if there are any open spaces on a given board state.
    def spaces_available_for_board_state(self, board_state):
        for row in board_state:
            if '*' in row:
                return True
        return False

    # Gets the score from the in-play board from a given player.
    def get_score(self, piece):
        total = 0
        for row in self.board:
            for space in row:
                if space == piece:
                    total += 1
        return total

    # Gets the score from a given player in the specified board state.
    def get_score_from_board_state(self, piece, board_state):
        total = 0
        for row in board_state:
            for space in row:
                if space == piece:
                    total += 1
        return total

    # Determines if there are valid moves available for the given player on the current board.
    def valid_moves_exist(self, piece, opponent):
        directions = ['up', 'down', 'left', 'right', 'up-left', 'up-right', 'down-left', 'down-right']
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                if self.board[y][x] == '*':
                    for direction in directions:
                        if self.check_for_pieces(piece, opponent, x, y, direction):
                            return True
        return False

    # Determines if there are valid moves available for the given player on a specified board state.
    def valid_moves_exist_for_board_state(self, piece, opponent, board_state):
        directions = ['up', 'down', 'left', 'right', 'up-left', 'up-right', 'down-left', 'down-right']
        for y in range(len(board_state)):
            for x in range(len(board_state[y])):
                if board_state[y][x] == '*':
                    for direction in directions:
                        if self.check_for_pieces_for_board_state(piece, opponent, x, y, direction, board_state):
                            return True
        return False

    # ******************************************************************************************************************
    # AI TURN LOGIC
    # ******************************************************************************************************************

    # The turn logic for the AI player. Works off the current saved board state.
    def ai_turn(self, piece, opponent):
        max_value = -sys.maxsize - 1
        max_x = 0
        max_y = 0
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                valid_move, message = self.validate_move(x, y, piece, opponent)
                if valid_move:
                    print()
                    test_value = self.h_x(x, y, piece, opponent)
                    print("h(x) at (", x, y, ")", test_value)
                    if test_value >= max_value:
                        max_value = test_value
                        max_x = x
                        max_y = y
        self.place_piece(max_x, max_y, piece)
        self.flip_pieces(max_x, max_y, piece, opponent)

    # ******************************************************************************************************************
    # HEURISTICS
    # ******************************************************************************************************************

    # The full heuristic considering all components.
    def h_x(self, x, y, piece, opponent):
        return self.theta[0] * self.heuristic_parity(x, y, piece, opponent) + \
               self.theta[1] * self.heuristic_mobility(x, y, piece, opponent) + \
               self.theta[2] * self.heuristic_corners(x, y, piece, opponent) + \
               self.theta[3] * self.heuristic_stability(x, y, piece, opponent)

    # The full heuristic considering all components for a given board state.
    def h_x_for_board_state(self, x, y, piece, opponent, board_state):
        return self.theta[0] * self.heuristic_parity_for_board_state(x, y, piece, opponent, board_state) + \
               self.theta[1] * self.heuristic_mobility_for_board_state(x, y, piece, opponent, board_state) + \
               self.theta[2] * self.heuristic_corners_for_board_state(x, y, piece, opponent, board_state) + \
               self.theta[3] * self.heuristic_stability_for_board_state(x, y, piece, opponent, board_state)

    # A heuristic analysing the value of a move on the current board by the number of pieces it wil flip.
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

    # A heuristic analysing the value of a move on a given board state by the number of pieces it wil flip.
    def heuristic_parity_for_board_state(self, x, y, piece, opponent, board_state):
        self.place_piece_on_board_state(x, y, piece, board_state)
        self.flip_pieces_on_board_state(x, y, piece, opponent, board_state)
        piece_score = self.get_score_from_board_state(piece, board_state)
        opponent_score = self.get_score_from_board_state(opponent, board_state)
        value = 0
        if piece_score + opponent_score != 0:
            value = 100 * (piece_score - opponent_score) / (piece_score + opponent_score)
        return value

    # A heuristic for analyzing the value of a move on the current board by the number of moves it opens up for the
    #   current player and the number of moves it blocks for the opponent player.
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

    # A heuristic for analyzing the value of a move on a given board state by the number of moves it opens up for the
    #   current player and the number of moves it blocks for the opponent player.
    def heuristic_mobility_for_board_state(self, x, y, piece, opponent, board_state):
        self.place_piece_on_board_state(x, y, piece, board_state)
        self.flip_pieces_on_board_state(x, y, piece, opponent, board_state)
        piece_move_count = 0
        opponent_move_count = 0
        for y in range(len(board_state)):
            for x in range(len(board_state[y])):
                valid_move, message = self.validate_move_for_board_state(x, y, piece, opponent, board_state)
                if valid_move:
                    piece_move_count += 1
                valid_move, message = self.validate_move_for_board_state(x, y, opponent, piece, board_state)
                if valid_move:
                    opponent_move_count += 1
        value = 0
        if piece_move_count + opponent_move_count != 0:
            value = 100 * (piece_move_count - opponent_move_count) / (piece_move_count + opponent_move_count)
        return value
