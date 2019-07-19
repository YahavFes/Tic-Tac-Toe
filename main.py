from tkinter import *
from functools import partial

class Board:

    def __init__(self):
        self.master_board = Tk()
        self.curr_turn = 0
        self.board = {}  # Matrix that includes the 9 different squares of the game
        self.result = {}
        for i in range(3):
            for j in range(3):
                self.board[i,j] = Button(self.master_board, height=10, width=15,
                                         command=partial(self.on_square_click,(i,j)))
                self.board[i,j].grid(row=i,column=j)
                self.result[i,j] = None

    def is_there_win(self):

        # Check if there is a winner in one of the rows
        for i in range(3):
            if self.result[i,0] == self.result[i,1] == self.result[i,2] and self.result[i,0] is not None:
                return True

        # Check if there is a winner in one of the columns
        for j in range(3):
            if self.result[0,j] == self.result[1,j] == self.result[2,j] and self.result[0,j] is not None:
                return True

        # Check if there is a winner in one of the diagonals
        if (self.result[0,0] == self.result[1,1] == self.result[2,2] or
            self.result[0,2] == self.result[1,1] == self.result[2,0]) and (self.result[1,1] is not None):
            return True

        return False

    def on_square_click(self, tuple):
        row, col = tuple
        if self.curr_turn % 2 == 0:
            self.board[row,col].config(bg='blue', state='disabled')
        else:
            self.board[row,col].config(bg='red', state='disabled')

        self.result[row,col] = self.curr_turn

        if self.is_there_win():
            winning_window = Toplevel(self.master_board)
            label = Label(winning_window, text='Player ' + str(self.curr_turn) + ' is the winner')
            label.pack()
            self.master_board.withdraw()
            winning_window.mainloop()

        self.curr_turn = 1 - self.curr_turn

    def start(self):
        self.master_board.mainloop()


if __name__ == '__main__':
    b = Board()
    b.start()
