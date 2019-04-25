import copy


class Othello:
    def __init__(self):
        self.board = [['*' for _ in range(8)] for _ in range(8)]
        self.backup_board = copy.deepcopy(self.board)

    def generate_start(self):
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
        print("Welcome to Othello, Black goes first")
        # Create function to see if there are any moves left
        moves_left = self.spaces_available()
        while moves_left:
            if self.valid_moves_exist('B', 'W'):
                print()
                should_have_turn = True
                while should_have_turn:
                    print("Black's Turn")
                    self.print_scores()
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
                    self.turn('W', 'B')
                    should_have_turn = not self.confirm_move()
            else:
                print("No valid moves for White available")
            moves_left = self.spaces_available() and \
                (self.valid_moves_exist('B', 'W') or self.valid_moves_exist('W', 'B'))

    def confirm_move(self):
        print("Confirm Move:")
        self.print_both_boards()
        acc_input = input("Accept New Board? (y, n)")
        while acc_input != 'y' and acc_input != 'Y' and acc_input != 'n' and acc_input != 'N':
            acc_input = input("Accept New Board? (y, n)")
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

    def turn(self, piece, opponent):
        # Display Board state for the player
        self.print_board()

        # Take in user input
        x = input("X [A, H]: ")
        y = input("Y (1, 8): ")

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

        # TODO: Create function to fill in pieces where appropriate
        self.flip_pieces(x, y, piece, opponent)
        pass

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
    othello = Othello()
    othello.generate_start()
    othello.game()
    othello.print_board()


if __name__ == '__main__':
    main()
