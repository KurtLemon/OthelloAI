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
            print(i, '|', end='')
            for piece in self.board[i]:
                print(' ', end='')
                print(piece, end=' ')
            print()


def main():
    othello = Othello()
    othello.generate_start()
    othello.print_board()


if __name__ == '__main__':
    main()