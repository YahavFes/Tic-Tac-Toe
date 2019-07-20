from tkinter import *
from board import Board

class Menu:

    def __init__(self):

        self.menu_window = Tk()
        openning_label = Label(self.menu_window, text='Tic-Tac-Toe', font=("Courier", 44))
        num_of_players_label = Label(self.menu_window, text='Please select the number of players:')
        player_1_button = Button(self.menu_window, text='1 Players', command=self.on_1_players_click)
        player_2_button = Button(self.menu_window, text='2 Players', command=self.on_2_players_click)
        openning_label.pack()
        num_of_players_label.pack()
        player_1_button.pack()
        player_2_button.pack()

    def on_1_players_click(self):
        board = Board(self.menu_window, 1)
        self.menu_window.withdraw()
        board.start()

    def on_2_players_click(self):
        board = Board(self.menu_window, 2)
        self.menu_window.withdraw()
        board.start()

    def launch(self):
        self.menu_window.mainloop()


if __name__ == '__main__':
    menu = Menu()
    menu.launch()