import copy
import threading
import sys
import math


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

    # ******************************************************************************************************************
    # PRINTING AND DISPLAY
    # ******************************************************************************************************************

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

    # Validates that a given move on the current board works.
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

    # Validates that a given move works on the given board state
    def validate_move_for_board_state(self, x, y, piece, opponent, board_state):
        # Check location is open
        if x < 0 or x > 7 or y < 0 or y > 7:
            return False, "Invalid move"
        if not board_state[y][x] == '*':
            return False, "Location is taken"

        directions = ['up', 'down', 'left', 'right', 'up-left', 'up-right', 'down-left', 'down-right']

        for direction in directions:
            if self.check_for_pieces_on_board_state(piece, opponent, x, y, direction, board_state):
                return True, "Move is good in direction " + direction

        return False, "No pieces captured by this move"

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
                        if self.check_for_pieces_on_board_state(piece, opponent, x, y, direction, board_state):
                            return True
        return False

    # Determines if any pieces will be captured by a specific move on the current board.
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

    # Determines if any pieces will be captured by a specific move on a given board state.
    def check_for_pieces_on_board_state(self, piece, opponent, x, y, mode, board_state):
        if mode == 'up':
            if y <= 1:
                return False
            if board_state[y - 1][x] != opponent:
                return False
            for dy in range(y - 2, -1, -1):
                if board_state[dy][x] == '*':
                    return False
                if board_state[dy][x] == piece:
                    return True
            return False
        if mode == 'down':
            if y >= 6:
                return False
            if board_state[y + 1][x] != opponent:
                return False
            for dy in range(y + 2, 8):
                if board_state[dy][x] == '*':
                    return False
                if board_state[dy][x] == piece:
                    return True
            return False
        if mode == 'left':
            if x <= 1:
                return False
            if board_state[y][x - 1] != opponent:
                return False
            for dx in range(x - 2, -1, -1):
                if board_state[y][dx] == '*':
                    return False
                if board_state[y][dx] == piece:
                    return True
            return False
        if mode == 'right':
            if x >= 6:
                return False
            if board_state[y][x + 1] != opponent:
                return False
            for dx in range(x + 2, 8):
                if board_state[y][dx] == '*':
                    return False
                if board_state[y][dx] == piece:
                    return True
            return False
        if mode == 'up-left':
            if y <= 1 or x <= 1:
                return False
            if board_state[y - 1][x - 1] != opponent:
                return False
            d = 2
            while x - d >= 0 and y - d >= 0:
                if board_state[y - d][x - d] == '*':
                    return False
                if board_state[y - d][x - d] == piece:
                    return True
                d += 1
            return False
        if mode == 'up-right':
            if y <= 1 or x >= 6:
                return False
            if board_state[y - 1][x + 1] != opponent:
                return False
            d = 2
            while x + d < 8 and y - d >= 0:
                if board_state[y - d][x + d] == '*':
                    return False
                if board_state[y - d][x + d] == piece:
                    return True
                d += 1
            return False
        if mode == 'down-left':
            if y >= 6 or x <= 1:
                return False
            if board_state[y + 1][x - 1] != opponent:
                return False
            d = 2
            while x - d >= 0 and y + d < 8:
                if board_state[y + d][x - d] == '*':
                    return False
                if board_state[y + d][x - d] == piece:
                    return True
                d += 1
            return False
        if mode == 'down-right':
            if y >= 6 or x >= 6:
                return False
            if board_state[y + 1][x + 1] != opponent:
                return False
            d = 2
            while x + d < 8 and y + d < 8:
                if board_state[y + d][x + d] == '*':
                    return False
                if board_state[y + d][x + d] == piece:
                    return True
                d += 1
            return False
        return False

    # ******************************************************************************************************************
    # PLAYER TURN LOGIC
    # ******************************************************************************************************************

    # The logic for a single human player turn.
    def turn(self, piece, opponent):
        # Display Board state for the player
        self.print_board()

        # Take in user input
        x = input("X [A, H]: ")
        y = input("Y [1, 8]: ")

        # Convert user input to proper indexing values
        x = self.char_to_int_index(x)
        if y.isdigit():
            y = int(y) - 1
        else:
            y = -1
        while x < 0 or x > 7 or y < 0 or y > 7:
            print("Invalid input")
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

    # ******************************************************************************************************************
    # AI TURN LOGIC
    # ******************************************************************************************************************

    # The turn logic for the AI player. Works off the current saved board state.
    def ai_turn(self, piece, opponent):
        board_state = copy.deepcopy(self.board)
        max_x, max_y = self.alpha_beta_starter(board_state, 3, -math.inf, math.inf, piece, opponent)
        # max_x, max_y, max_value = self.maximize_piece_board_state(piece, opponent, board_state)
        print("AI move:", self.int_index_to_char(max_x), max_y + 1)
        self.place_piece(max_x, max_y, piece)
        self.flip_pieces(max_x, max_y, piece, opponent)

    # ******************************************************************************************************************
    # MINIMAX AND SEARCHING
    # ******************************************************************************************************************

    def alpha_beta_starter(self, board_state, depth, alpha, beta, piece, opponent):
        children = []
        for y in range(len(board_state)):
            for x in range(len(board_state[y])):
                valid_move, message = self.validate_move_for_board_state(x, y, piece, opponent, board_state)
                if valid_move:
                    board_state_copy = copy.deepcopy(board_state)
                    self.place_piece_on_board_state(x, y, piece, board_state_copy)
                    self.flip_pieces_on_board_state(x, y, piece, opponent, board_state_copy)
                    children.append([board_state_copy, x, y])
        max_val = -math.inf
        max_val_location = 0
        for i in range(len(children)):
            child = children[i][0]
            value = -self.alpha_beta_2(child, depth - 1, alpha, beta, False, opponent, piece)
            print("DETERMINED ALPHA-BETA VALUE FOR:")
            self.print_board_from_board_state(child)
            children[i].append(value)
            print("VALUE:", value)
            print()
            if value >= max_val:
                max_val = value
                max_val_location = i
        print("MAXIMUM CHILD")
        self.print_board_from_board_state(children[max_val_location][0])
        print("X, Y:", children[max_val_location][1], children[max_val_location][2])
        print("VALUE:", children[max_val_location][3])
        return children[max_val_location][1], children[max_val_location][2]

    def alpha_beta(self, board_state, depth, alpha, beta, player, piece, opponent):
        if depth == 0:
            return self.h_x_for_board_state(opponent, piece, board_state)
        if player:
            value = -math.inf
            children = []
            for y in range(len(board_state)):
                for x in range(len(board_state[y])):
                    valid_move, message = self.validate_move_for_board_state(x, y, piece, opponent, board_state)
                    if valid_move:
                        board_state_copy = copy.deepcopy(board_state)
                        self.place_piece_on_board_state(x, y, piece, board_state_copy)
                        self.flip_pieces_on_board_state(x, y, piece, opponent, board_state_copy)
                        children.append(board_state_copy)
            for child in children:
                value = max(value, self.alpha_beta(child, depth - 1, alpha, beta, False, opponent, piece))
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value
        else:
            value = math.inf
            children = []
            for y in range(len(board_state)):
                for x in range(len(board_state[y])):
                    valid_move, message = self.validate_move_for_board_state(x, y, piece, opponent, board_state)
                    if valid_move:
                        board_state_copy = copy.deepcopy(board_state)
                        self.place_piece_on_board_state(x, y, piece, board_state_copy)
                        self.flip_pieces_on_board_state(x, y, piece, opponent, board_state_copy)
                        children.append(board_state_copy)
            for child in children:
                value = min(value, -self.alpha_beta(child, depth - 1, alpha, beta, True, opponent, piece))
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return value

    def alpha_beta_2(self, board_state, depth, alpha, beta, player, piece, opponent):
        if depth == 0:
            if player:
                return self.h_x_for_board_state(piece, opponent, board_state)
            else:
                return -self.h_x_for_board_state(opponent, piece, board_state)
        if player:
            value = -math.inf
            children = []
            for y in range(len(board_state)):
                for x in range(len(board_state[y])):
                    valid_move, message = self.validate_move_for_board_state(x, y, piece, opponent, board_state)
                    if valid_move:
                        board_state_copy = copy.deepcopy(board_state)
                        self.place_piece_on_board_state(x, y, piece, board_state_copy)
                        self.flip_pieces_on_board_state(x, y, piece, opponent, board_state_copy)
                        children.append(board_state_copy)
            for child in children:
                value = max(value, self.alpha_beta_2(child, depth - 1, alpha, beta, False, piece, opponent))
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value
        else:
            value = math.inf
            children = []
            for y in range(len(board_state)):
                for x in range(len(board_state[y])):
                    valid_move, message = self.validate_move_for_board_state(x, y, opponent, piece, board_state)
                    if valid_move:
                        board_state_copy = copy.deepcopy(board_state)
                        self.place_piece_on_board_state(x, y, opponent, board_state_copy)
                        self.flip_pieces_on_board_state(x, y, opponent, piece, board_state_copy)
                        children.append(board_state_copy)
            for child in children:
                value = min(value, self.alpha_beta_2(child, depth - 1, alpha, beta, True, piece, opponent))
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return value

    # Given a particular board state the function finds the best possible move for the player and returns its location
    #   as well as heuristic value.
    def maximize_piece_board_state(self, piece, opponent, board_state):
        max_value = -sys.maxsize - 1
        max_x = 0
        max_y = 0
        for y in range(len(board_state)):
            for x in range(len(board_state[y])):
                valid_move, message = self.validate_move_for_board_state(x, y, piece=piece, opponent=opponent,
                                                                         board_state=board_state)
                if valid_move:
                    board_state_copy = copy.deepcopy(board_state)
                    self.place_piece_on_board_state(x, y, piece, board_state_copy)
                    self.flip_pieces_on_board_state(x, y, piece, opponent, board_state_copy)
                    test_value = self.h_x_for_board_state(piece, opponent, board_state_copy)
                    if test_value >= max_value:
                        max_value = test_value
                        max_x = x
                        max_y = y
        return max_x, max_y, max_value

    # Given a particular board state the function finds the best possible move for the opponent and returns its location
    #   and heuristic value.
    def maximize_opponent_board_state(self, piece, opponent, board_state):
        max_value = -sys.maxsize - 1
        max_x = 0
        max_y = 0
        for y in range(len(board_state)):
            for x in range(len(board_state[y])):
                valid_move, message = self.validate_move_for_board_state(x, y, piece=opponent, opponent=piece,
                                                                         board_state=board_state)
                if valid_move:
                    board_state_copy = copy.deepcopy(board_state)
                    self.place_piece_on_board_state(x, y, opponent, board_state_copy)
                    self.flip_pieces_on_board_state(x, y, opponent, piece, board_state_copy)
                    test_value = self.h_x_for_board_state(opponent, piece, board_state_copy)
                    if test_value >= max_value:
                        max_value = test_value
                        max_x = x
                        max_y = y
        return max_x, max_y, max_value

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
    def h_x_for_board_state(self, piece, opponent, board_state):
        print("Searching for", piece)
        self.print_board_from_board_state(board_state)
        parity = self.heuristic_parity_for_board_state(piece, opponent, board_state)
        mobility = self.heuristic_mobility_for_board_state(piece, opponent, board_state)
        corners = self.heuristic_corners_for_board_state(piece, board_state)
        stability = self.heuristic_stability_for_board_state(piece, opponent, board_state)
        total_h_value = self.theta[0] * parity + \
                        self.theta[1] * mobility + \
                        self.theta[2] * corners + \
                        self.theta[3] * stability
        print("Parity:", parity)
        print("Mobility:", mobility)
        print("Corners:", corners)
        print("Stability:", stability)
        print("Total Heuristic Value:", total_h_value)
        print()
        return total_h_value

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
    def heuristic_parity_for_board_state(self, piece, opponent, board_state):
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
    def heuristic_mobility_for_board_state(self, piece, opponent, board_state):
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

    # A heuristic for the value of a move based on the number of corners it captures.
    def heuristic_corners(self, x, y, piece, opponent):
        self.place_piece(x, y, piece)
        self.flip_pieces(x, y, piece, opponent)
        value = 0
        if x == 0 or x == 7:
            if y == 0 or y == 7:
                value = 100
        self.board = copy.deepcopy(self.backup_board)
        return value

    # A heuristic for the value of a move based on the number of corners it captures based odd a given board state.
    def heuristic_corners_for_board_state(self, piece, board_state):
        value = 0
        if board_state[0][0] == piece:
            value += 100
        if board_state[0][7] == piece:
            value += 100
        if board_state[7][0] == piece:
            value += 100
        if board_state[7][7] == piece:
            value += 100
        return value

    # A heuristic for the value of a move based on home many stable pieces it creates on the current board.
    def heuristic_stability(self, xloc, yloc, piece, opponent):
        self.place_piece(xloc, yloc, piece)
        self.flip_pieces(xloc, yloc, piece, opponent)

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

        total_stability = []
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                # Check up
                if self.validate_move(x, y, piece, opponent):
                    for dy in range(y - 1, -1, -1):
                        if self.board[dy][x] == opponent:
                            opponent_up = True
                            stable_up = False
                        if self.board[dy][x] == '*':
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

                    total_stability.append(100 * (vertical_stability + horizontal_stability + diagonal_down_stability +
                                                  diagonal_up_stability) / 8)
        self.board = copy.deepcopy(self.backup_board)
        return sum(total_stability) / len(total_stability)

    # A heuristic for move value based on the number of stable pieces it creates on a given board state.
    def heuristic_stability_for_board_state(self, piece, opponent, board_state):
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

        total_stability = []
        for y in range(len(board_state)):
            for x in range(len(board_state[y])):
                # Check up
                if self.validate_move_for_board_state(x, y, piece, opponent, board_state):
                    for dy in range(y - 1, -1, -1):
                        if board_state[dy][x] == opponent:
                            opponent_up = True
                            stable_up = False
                        if board_state[dy][x] == '*':
                            stable_up = False

                    # Check down
                    for dy in range(y + 1, 8):
                        if board_state[dy][x] == opponent:
                            opponent_down = True
                            stable_down = False
                        if board_state[dy][x] == '*':
                            stable_down = False

                    # Check left
                    for dx in range(x - 1, -1, -1):
                        if board_state[y][dx] == opponent:
                            opponent_left = True
                            stable_left = False
                        if board_state[y][dx] == '*':
                            stable_left = False

                    # Check right
                    for dx in range(x + 1, 8):
                        if board_state[y][dx] == opponent:
                            opponent_right = True
                            stable_right = False
                        if board_state[y][dx] == '*':
                            stable_right = False

                    # Check up-left
                    d = 1
                    while x - d >= 0 and y - d >= 0:
                        if board_state[y - d][x - d] == opponent:
                            opponent_up_left = True
                            stable_up_left = False
                        if board_state[y - d][x - d] == '*':
                            stable_up_left = False
                        d += 1

                    # Check down-right
                    d = 1
                    while x + d < 8 and y + d < 8:
                        if board_state[y + d][x + d] == opponent:
                            opponent_down_right = True
                            stable_down_right = False
                        if board_state[y - d][x - d] == '*':
                            stable_down_right = False
                        d += 1

                    # Check down-left
                    d = 1
                    while x - d >= 0 and y + d < 8:
                        if board_state[y + d][x - d] == opponent:
                            opponent_down_left = True
                            stable_down_left = False
                        if board_state[y + d][x - d] == '*':
                            stable_down_left = False
                        d += 1

                    # Check up-right
                    d = 1
                    while x + d < 8 and y - d >= 0:
                        if board_state[y - d][x + d] == opponent:
                            opponent_right = True
                            stable_up_right = False
                        if board_state[y - d][x + d] == '*':
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

                    total_stability.append(100 * (vertical_stability + horizontal_stability + diagonal_down_stability +
                                                  diagonal_up_stability) / 8)
        return sum(total_stability) / len(total_stability)

    # ******************************************************************************************************************
    # PIECE MOVEMENT
    # ******************************************************************************************************************

    # Places a piece on the current board in the location given.
    def place_piece(self, x, y, piece):
        self.board[y][x] = piece

    # Places a piece on the a given board state in the location given.
    def place_piece_on_board_state(self, x, y, piece, board_state):
        board_state[y][x] = piece

    # Flips the pieces appropriately surrounding a given move on the current board.
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

    # Flips the pieces appropriately surrounding a given move on a given board state.
    def flip_pieces_on_board_state(self, x, y, piece, opponent, board_state):
        if self.check_for_pieces_on_board_state(piece, opponent, x, y, 'up', board_state):
            dy = y - 1
            while board_state[dy][x] == opponent:
                board_state[dy][x] = piece
                dy -= 1
        if self.check_for_pieces_on_board_state(piece, opponent, x, y, 'down', board_state):
            dy = y + 1
            while board_state[dy][x] == opponent:
                board_state[dy][x] = piece
                dy += 1
        if self.check_for_pieces_on_board_state(piece, opponent, x, y, 'left', board_state):
            dx = x - 1
            while board_state[y][dx] == opponent:
                board_state[y][dx] = piece
                dx -= 1
        if self.check_for_pieces_on_board_state(piece, opponent, x, y, 'right', board_state):
            dx = x + 1
            while board_state[y][dx] == opponent:
                board_state[y][dx] = piece
                dx += 1
        if self.check_for_pieces_on_board_state(piece, opponent, x, y, 'up-left', board_state):
            dy = y - 1
            dx = x - 1
            while board_state[dy][dx] == opponent:
                board_state[dy][dx] = piece
                dy -= 1
                dx -= 1
        if self.check_for_pieces_on_board_state(piece, opponent, x, y, 'up-right', board_state):
            dy = y - 1
            dx = x + 1
            while board_state[dy][dx] == opponent:
                board_state[dy][dx] = piece
                dy -= 1
                dx += 1
        if self.check_for_pieces_on_board_state(piece, opponent, x, y, 'down-left', board_state):
            dy = y + 1
            dx = x - 1
            while board_state[dy][dx] == opponent:
                board_state[dy][dx] = piece
                dy += 1
                dx -= 1
        if self.check_for_pieces_on_board_state(piece, opponent, x, y, 'down-right', board_state):
            dy = y + 1
            dx = x + 1
            while board_state[dy][dx] == opponent:
                board_state[dy][dx] = piece
                dy += 1
                dx += 1

    # ******************************************************************************************************************
    # UTILITIES
    # ******************************************************************************************************************

    # Given user input in selecting a coordinate, it provides the useful numeric value.
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

    # Given an index it returns it in expected user input value.
    def int_index_to_char(self, i):
        if i == 0:
            return 'A'
        if i == 1:
            return 'B'
        if i == 2:
            return 'C'
        if i == 3:
            return 'D'
        if i == 4:
            return 'E'
        if i == 5:
            return 'F'
        if i == 6:
            return 'G'
        if i == 7:
            return 'H'
        return '-1'


def main():
    othello = Othello()
    start_position = get_start_position()
    othello.generate_start(int(start_position))
    othello.game()
    othello.print_board()


def get_start_position():
    player_input = input("Which configuration do you want to start with?\n1:  2:\nWB  BW\nBW  WB")
    while player_input != '1' and player_input != '2':
        player_input = input("Invalid input. Which configuration do you want to start with?\n1:  2:\nWB  BW\nBW  WB")
    return player_input


if __name__ == '__main__':
    main()
