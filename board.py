from tkinter import *
from functools import partial
import time

class Board:

    def __init__(self, menu_window, num_of_players):
        self.menu_window = menu_window
        self.num_of_players = num_of_players
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

        if self.num_of_players == 2:
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
        if self.num_of_players == 1:
            self.computer_move(tuple)
        else:
            self.other_player_move(tuple)

    def other_player_move(self, tuple):
        row, col = tuple
        if self.curr_turn % 2 == 0:
            self.board[row, col].config(bg='blue', state='disabled')
        else:
            self.board[row, col].config(bg='red', state='disabled')

        self.result[row, col] = self.curr_turn

        if self.is_there_win():
            winning_window = self.create_winning_window('Player ' + str(self.curr_turn) + ' is the winner')
            self.board_window.withdraw()
            winning_window.mainloop()

        if self.find_empty_square() is None:  # If the board is full
            self.handle_tie()
            return

        self.curr_turn = 1 - self.curr_turn

        self.player_turn_label.config(text='Player ' + str(self.curr_turn) + ' Turn')

    def computer_move(self, tuple):
        row, col = tuple
        self.board[row, col].config(bg='blue', state='disabled')
        self.result[row, col] = 0

        # Check if the Player is the winner
        if self.is_there_win():
            winning_window = self.create_winning_window("You are the Winner")
            self.board_window.withdraw()
            winning_window.mainloop()

        # First, check if there is a chance the player can win, if yes then block it
        if self.find_blocking_square() is not None:
            self.board[self.find_blocking_square()].config(bg='red', state='disabled')
            self.result[self.find_blocking_square()] = 1
        # Block the middle square
        elif self.result[1, 1] is None:
            self.board[1, 1].config(bg='red', state='disabled')
            self.result[1, 1] = 1
        # Choose an empty square
        else:
            if self.find_empty_square() is None:  # If the board is full
                self.handle_tie()
                return
            self.board[self.find_empty_square()].config(bg='red', state='disabled')
            self.result[self.find_empty_square()] = 1

        # Check if the Computer is the winner
        if self.is_there_win():
            winning_window = self.create_winning_window("The Computer is the Winner")
            self.board_window.withdraw()
            winning_window.mainloop()

    def find_blocking_square(self):

        # Check if there is a row that has 2 squares that marked as player 0
        for row in range(3):
            if len([0 for col in range(3) if self.result[row,col]==0]) == 2:
                for col in range(3):
                    if self.result[row,col] is None:
                        return row, col
        # Check if there is a column that has 2 squares that marked as player 0
        for col in range(3):
            if len([0 for row in range(3) if self.result[row,col]==0]) == 2:
                for row in range(3):
                    if self.result[row, col] is None:
                        return row, col
        # Check if there is a diagonal that has 2 squares that marked as player 0
        if len([0 for i in range(3) if self.result[i,i] == 0]) == 2:
            for i in range(3):
                if self.result[i,i] is None:
                    return i, i
        if len(list(filter(lambda x: x == 0, [self.result[0,2], self.result[1,1], self.result[2,0]]))) == 2:
            if self.result[0,2] is None:
                return 0, 2
            if self.result[1,1] is None:
                return 1, 1
            if self.result[2,0] is None:
                return 2, 2
        return None

    def find_empty_square(self):
        for row in range(3):
            for col in range(3):
                if self.result[row, col] is None:
                    return row, col

    def create_winning_window(self, winning_msg):
        winning_window = Toplevel(self.board_window)
        label = Label(winning_window, text=winning_msg)
        quit_button = Button(winning_window, text='Back to menu',
                             command=partial(self.on_quit_click, winning_window))
        label.pack()
        quit_button.pack()
        return winning_window

    def handle_tie(self):
        tie_window = self.create_winning_window('This is a Tie')
        self.board_window.withdraw()
        tie_window.mainloop()

    def on_quit_click(self, winning_window):
        winning_window.destroy()
        self.board_window.destroy()
        self.menu_window.deiconify()

    def start(self):
        self.board_window.mainloop()
