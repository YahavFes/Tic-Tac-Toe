from tkinter import *
from functools import partial

class Board:

    def __init__(self, menu_window):
        self.menu_window = menu_window
        self.board_window = Toplevel(self.menu_window)
        self.curr_turn = 0
        self.board = {}  # Matrix that includes the 9 different squares of the game
        self.result = {}

        # Initial the board game with the 9 different buttons
        for i in range(3):
            for j in range(3):
                self.board[i,j] = Button(self.board_window, height=10, width=15,
                                         command=partial(self.on_square_click,(i,j)))
                self.board[i,j].grid(row=i,column=j)
                self.result[i,j] = None

        self.player_turn_label = Label(self.board_window, text='Player 0 Turn')
        self.player_turn_label.grid(row=3)

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
            winning_window = Toplevel(self.board_window)
            label = Label(winning_window, text='Player ' + str(self.curr_turn) + ' is the winner')
            quit_button = Button(winning_window, text='Back to menu', command=partial(self.on_quit_click,winning_window))
            label.pack()
            quit_button.pack()
            self.board_window.withdraw()
            winning_window.mainloop()

        self.curr_turn = 1 - self.curr_turn
        self.player_turn_label.config(text='Player ' + str(self.curr_turn) + ' Turn')

    def on_quit_click(self, winning_window):
        winning_window.destroy()
        self.board_window.destroy()
        self.menu_window.deiconify()

    def start(self):
        self.board_window.mainloop()
