class Othello:
    def __init__(self):
        self.board = [['*' for _ in range(8)] for _ in range(8)]

    def generate_start(self):
        self.board[3][3] = 'B'
        self.board[3][4] = 'W'
        self.board[4][3] = 'W'
        self.board[4][4] = 'B'

    def print_board(self):
        print("   _A__B__C__D__E__F__G__H_")
        for i in range(len(self.board)):
            print(i + 1, '|', end='')
            for piece in self.board[i]:
                print(' ', end='')
                print(piece, end=' ')
            print()

    def game(self):
        print("Welcome to Othello, Black goes first")
        # Create function to see if there are any moves left
        moves_left = self.spaces_available()
        while moves_left:
            self.turn('B')
            self.turn('W')
            moves_left = self.spaces_available()

    def spaces_available(self):
        for row in self.board:
            if '*' in row:
                return True
        return False

    def turn(self, piece):
        # Display Board state for the player
        self.print_board()

        # Take in user input
        x = input("X [A, H]: ")
        y = input("Y (1, 8): ")

        # Convert user input to proper indexing values
        x = self.char_to_int_index(x)
        y = int(y) - 1

        # Validate move
        valid_move, message = self.validate_move(x, y)
        while not valid_move:
            print(message, "enter another move.")

            # Take in user input
            x = input("X [A, H]: ")
            y = input("Y (1, 8): ")

            # Convert user input to proper indexing values
            x = self.char_to_int_index(x)
            y = int(y) - 1
            valid_move, message = self.validate_move(x, y)

        self.place_piece(x, y, piece)

        # TODO: Create function to fill in pieces where appropriate
        # Fill pieces as necessary
        pass

    def place_piece(self, x, y, piece):
        self.board[y][x] = piece

    def validate_move(self, x, y):
        # Check location is open
        if x < 0 or x > 7 or y < 0 or y > 7:
            return False, "Invalid move"
        if not self.board[y][x] == '*':
            return False, "Location is taken"

        # TODO: Check if conditions are met for the move
        return True, "Move is good"

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
