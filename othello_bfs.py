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
