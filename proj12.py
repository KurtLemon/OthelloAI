'''
Class: CPSC 427
Team Member 1: Ariana Hibbard
Team Member 2: Kurt Lamon
Submitted By
GU Username 1: ahibbard
GU Username 2: klamon
File Name: proj12.py
Description: Implements the Othello interface.
Usage: python proj12.py

Use python3
'''

class Othello:
    # has a board member that is an 8 x 8 matrix
    # the game driver

    # Game Driver(?)
    # - tracks turns
    # - displays a timer that ticks off seconds starting
    # from 10 when a move is initiated
    # - tracks if the AI fails to move within ten seconds
    # - assigns colors to teams
    # - reads in answers from player
    # -asks player for confirmation to change board configuration

    # starts the othello game
    def othello(self):
        pass
    # Timer called when  a new move is inititated. Forfeit game if time goes above ten seconds.
    def start_timer(self):
        pass
    
    def forfeit_game(self):
        pass
    pass

class Board:
    # Board
    # - the board has a game state
    # - each piece of the board can be B, W, or unoccupied
    # - each piece of the board has an associated coordinate.

    # initial board configuration:
    # * * * * * * * *
    # * * * * * * * *
    # * * * * * * * *
    # * * * B W * * *
    # * * * W B * * *
    # * * * * * * * *
    # * * * * * * * *
    # * * * * * * * *

    # function ideas:
    # this will initialize the board at the beginning of the game
    def __init__(self, dimension):
        # each board piece could be a tuple with: X-coord, y-coord, and state(B,W,*)
        # (3,3) --> B
        # (3,4) --> W
        # (4,3) --> W
        # (4,4) --> B
        # the first value is the row, second is the column, third is the piece
        board_tokens = [(3,3,'B'),
                        (3,4,'W'),
                        (4,3,'W'),
                        (4,4,'B')]
        self.board = [[] for i in range(dimension)]

    def change_initial_configuration(self):
        pass
    # the system must always save the prior board state
    def save_current_board_state(self):
        pass
    
    def get_past_board_state(self):
        pass
    # function to update the state of a particular coordinate on the board
    def update_coordinate_state(self):
        pass

    # update the state of the entire board to reflect new move from user
    def update_board_state(self):
        pass

    # this will display the board pieces in their current state
    def display_board(self):
        for row in range(len(self.board)):
            print(self.board[row])

class Player:
    # Player
    # - has color (black or white)
    # - will take a turn

    # function ideas
    # initialize player to beginning state
    def __init__(self):
        pass

    # assign the player a specific color (black or white) based on user input
    def assign_color(self):
        pass

    # called if the player decides to quit the game
    def player_quit(self):
        pass

    pass

class AIPlayer:
    # AI Player
    # - determines the available moves
    # - determines which move to make

    # the AI will determine if making a move is possible
    def can_make_move(self):
        pass
    pass

class Scoreboard:
    # Scoreboard
    # - The scoreboard displays the number of black and number
    # of white pieces on the board.

    # initialize the scoreboard to a beginning game state
    def __init__(self):
        pass

    def count_black_pieces(self):
        pass
    def count_white_pieces(self):
        pass
    def update_scores(self):
        pass
    def display_player_turn(self):
        pass
    def display_scores(self):
        pass
    pass

def main():
    # initialize board (just to test the function, this will be replaced with othello class)
    gameboard = Board(8)
    gameboard.display_board()


main()
# The board is an 8 x 8 matrix with initial config:
# WB
# BW

# your game allows the initial configuration to be changed to:
# BW
# WB
