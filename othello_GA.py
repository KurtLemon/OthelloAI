import copy
import threading
import random


class Othello:
    def __init__(self):
        self.board = [['*' for _ in range(8)] for _ in range(8)]
        self.backup_board = copy.deepcopy(self.board)

    def generate_start(self):
        self.board[3][3] = 'W'
        self.board[3][4] = 'B'
        self.board[4][3] = 'B'
        self.board[4][4] = 'W'
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

    def game(self, weights_1, weights_2):
        moves_left = self.spaces_available()
        while moves_left:
            if self.valid_moves_exist('B', 'W'):
                should_have_turn = True
                while should_have_turn:
                    self.ai_turn('B', 'W', weights_1)
                    should_have_turn = False
            if self.valid_moves_exist('W', 'B'):
                should_have_turn = True
                while should_have_turn:
                    self.ai_turn('W', 'B', weights_2)
                    should_have_turn = False
            moves_left = self.spaces_available() and \
                (self.valid_moves_exist('B', 'W') or self.valid_moves_exist('W', 'B'))

    def spaces_available(self):
        for row in self.board:
            if '*' in row:
                return True
        return False

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

    def ai_turn(self, piece, opponent, values):
        max_value = 0
        max_x = 0
        max_y = 0
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                valid_move, message = self.validate_move(x, y, piece, opponent)
                if valid_move:
                    test_value = self.evaluate_move_location(x, y, values)
                    if test_value >= max_value:
                        max_value = test_value
                        max_x = x
                        max_y = y
        self.place_piece(max_x, max_y, piece)
        self.flip_pieces(max_x, max_y, piece, opponent)

    def evaluate_move_location(self, x, y, values):
        return values[y][x]

    def check_for_pieces(self, piece, opponent, x, y, mode):
        if mode == 'up':
            if y == 0:
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
            if y == 7:
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
            if x == 0:
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
            if x == 7:
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
            if y == 0 or x == 0:
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
            if y == 0 or x == 7:
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
            if y == 7 or x == 0:
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
            if y == 7 or x == 7:
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
                return True, "Move is good"

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
    epoch_size = 10000
    good_heuristics = []

    # Generate Initial Population
    for k in range(64):
        othello = Othello()
        othello.generate_start()
        weights = []
        for i in range(2):
            weight = []
            for y in range(len(othello.board)):
                row = []
                for x in range(len(othello.board[y])):
                    row.append(random.randint(0, 1000) / 1000)
                weight.append(row)
            weights.append(weight)

        # Play first round of games and add winners to good pile
        othello.game(weights[0], weights[1])
        if othello.get_score('B') >= othello.get_score('W'):
            if othello.get_score('W') != 0:
                good_heuristics.append((weights[0], othello.get_score('B') / othello.get_score('W')))
            else:
                good_heuristics.append((weights[0], 100))
        elif othello.get_score('W') > othello.get_score('B'):
            if othello.get_score('B') != 0:
                good_heuristics.append((weights[1], othello.get_score('W') / othello.get_score('B')))
            else:
                good_heuristics.append((weights[1], 100))

    for g in range(epoch_size):
        print("Generation", g + 1, "/", epoch_size)
        # Sort the good pile
        for i in range(len(good_heuristics)):
            for j in range(i + 1, len(good_heuristics)):
                if good_heuristics[j][1] > good_heuristics[i][1]:
                    temp = good_heuristics[j]
                    good_heuristics[j] = good_heuristics[i]
                    good_heuristics[i] = temp

        # Mate the good pile and append both children to the new population
        all_heuristics = []
        available_indices = []
        for i in range(64):
            available_indices.append(i)
        for i in range(0, len(good_heuristics) // 2, 1):
            rand = random.randint(0, len(available_indices) - 1)
            index = available_indices[rand]
            available_indices.pop(rand)
            heuristic_1, heuristic_2 = mate(good_heuristics[i][0], good_heuristics[index][0])
            all_heuristics.append(heuristic_1)
            all_heuristics.append(heuristic_2)

        # Fill the rest of the population with random members
        for k in range(32):
            othello = Othello()
            othello.generate_start()
            weights = []
            for i in range(2):
                weight = []
                for y in range(len(othello.board)):
                    row = []
                    for x in range(len(othello.board[y])):
                        row.append(random.randint(0, 1000) / 1000)
                    weight.append(row)
                weights.append(weight)
            all_heuristics.append(weights[0])
            all_heuristics.append(weights[1])

        # Play games to determine new population
        good_heuristics = []
        for i in range(0, len(all_heuristics), 2):
            othello = Othello()
            othello.generate_start()
            othello.game(all_heuristics[i], all_heuristics[i + 1])
            if othello.get_score('B') >= othello.get_score('W'):
                if othello.get_score('W') != 0:
                    good_heuristics.append((weights[0], othello.get_score('B') / othello.get_score('W')))
                else:
                    good_heuristics.append((weights[0], 100))
            elif othello.get_score('W') > othello.get_score('B'):
                if othello.get_score('B') != 0:
                    good_heuristics.append((weights[1], othello.get_score('W') / othello.get_score('B')))
                else:
                    good_heuristics.append((weights[1], 100))

    # Sort the good pile
    for i in range(len(good_heuristics)):
        for j in range(i + 1, len(good_heuristics)):
            if good_heuristics[j][1] > good_heuristics[i][1]:
                temp = good_heuristics[j]
                good_heuristics[j] = good_heuristics[i]
                good_heuristics[i] = temp

    # Print the heuristic Scores and heuristics
    for i in range(len(good_heuristics)):
        print(good_heuristics[i][1],
              "Corners",
              good_heuristics[i][0][0][0] + good_heuristics[i][0][0][0] + good_heuristics[i][0][0][0] +
              good_heuristics[i][0][0][0])
        for row in good_heuristics[i][0]:
            print(row)
        print()



def mate(heuristic_1, heuristic_2):
    for i in range(len(heuristic_1)):
        for j in range(len(heuristic_1[i])):
            if random.randint(0, 1) == 1:
                temp = heuristic_1[i][j]
                heuristic_1[i][j] = heuristic_2[i][j]
                heuristic_2[i][j] = temp
    return heuristic_1, heuristic_2

if __name__ == '__main__':
    main()
