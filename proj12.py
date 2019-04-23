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
    pass

class Board:
    # Board
    # - the board has a game state
    # - each piece of the board can be B, W, or unoccupied
    # - each piece of the board has an associated coordinate.

    # function ideas:
    # this will initialize the board at the beginning of the game
    def __init__(self):
        pass

    # this will display the board pieces in their current state
    def display_board(self):
        pass
    
    pass

class BoardPiece:
    # Board Piece
    # - state: B, W, or unoccupied
    # - location: coordinate in the row (row, col)
    pass

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

    pass

class AIPlayer:
    # AI Player
    # - determines the available moves
    # - determines which move to make
    pass

class Scoreboard:
    # Scoreboard
    # - The scoreboard displays the number of black and number
    # of white pieces on the board.

    # initialize the scoreboard to a beginning game state
    def __init__(self):
        pass
    def update_scores(self):
        pass
    
    def display_scores(self):
        pass
    pass

# Specifications for Interaction
# P = Player
# AI = Player
# S = System that keeps track of things

# The board is an 8 x 8 matrix with initial config:
# WB
# BW

# your game allows the initial configuration to be changed to:
# BW
# WB
