import tkinter as tk
import time

from reversi import ReversiGame, Player, RandomPlayer, _index_to_algebraic
from constants import BLACK, WHITE
from typing import Optional


class ReversiGUI:
    """"""

    def __init__(self, parent, size) -> None:
        """initialize gui"""
        # setting up
        self.root = parent
        self.root.title('Reversi')
        self.frame = tk.Frame(parent)
        self.board = tk.Canvas(height=500, width=500, bg='black')
        self.frame.pack()
        self.clicked = tk.BooleanVar()
        self.board.bind('<Button-1>', self.click)

        # initialize game
        self.game = ReversiGame(size)
        # self.player1 = player1
        # self.player2 = player2
        self.draw_game_state()

        # run game
        # self.run_game(self.player1, self.player2)

    def run_game(self, black, white) -> None:
        """Run a Reversi game between the two given players.

        Return the winner and list of moves made in the game.
        """
        previous_move = None
        current_player = black
        self.draw_game_state()

        while self.game.get_winner() is None:
            previous_move = current_player.make_move(self.game, previous_move)
            if previous_move != 'mouse_pos':
                self.game.make_move(previous_move)
                self.draw_game_state()
                time.sleep(1)
                root.update()
            else:
                # self.game.make_move(self.mouse_input_move())
                root.wait_variable(self.clicked)
                self.clicked.set(not self.clicked.get())

            if current_player is black:
                current_player = white
            else:
                current_player = black

    def run_game_human(self, black, white) -> None:
        """Run a Reversi game between the two given players.

        Return the winner and list of moves made in the game.
        """
        previous_move = None
        current_player = black
        self.draw_game_state()

        while self.game.get_winner() is None:

            # previous_move = current_player.make_move(self.game, previous_move)
            root.wait_variable(self.clicked)

            # self.draw_game_state()
            # time.sleep(1)
            # root.update()

            if current_player is black:
                current_player = white
            else:
                current_player = black

    # def mouse_input_move(self) -> None:
    #     """Return a move based on where the user clicks on the UI"""
    #     root.wait_variable(self.click_move)
    #     return self.click_move

    def draw_game_state(self, h=500, w=500) -> None:
        """Visualize the game by drawing on the Canvas"""

        lst = self.game.get_game_board()

        x = w / self.game.get_size()
        y = h / self.game.get_size()

        inset = x / 5

        colours = {WHITE: 'white', BLACK: 'black'}

        for r in range(0, self.game.get_board_size()):
            for c in range(0, self.game.get_board_size()):
                self.board.create_rectangle(c * x, r * y, (c + 1) * x, (r + 1) * y,
                                            fill='green4', outline='dark green', width=5)

                if lst[r][c] in {WHITE, BLACK}:
                    colour = colours[lst[r][c]]

                    self.board.create_oval(c * x + inset, r * y + inset, (c + 1) * x - inset,
                                           (r + 1) * y - inset, fill=colour, outline='black',
                                           width=0)

        self.board.pack()

    def click(self, event) -> None:
        """Called when mouse is clicked on the given canvas"""
        xcor = event.x // (self.board.winfo_width() / 8)
        ycor = event.y // (self.board.winfo_height() / 8)

        pos = (ycor, xcor)
        move = _index_to_algebraic(pos)
        print(move)
        if move in self.game.get_valid_moves():
            self.game.make_move(move)
            self.draw_game_state()
            root.update()
            self.clicked.set(not self.clicked.get())
            return


from reversi import GUIPlayer
if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('500x500')
    gui = ReversiGUI(root, 8)
    # gui.run_game(RandomPlayer(), RandomPlayer())
    # gui.run_game_human(RandomPlayer(), RandomPlayer())
    gui.run_game(RandomPlayer(), GUIPlayer())
    root.deiconify()
    root.mainloop()
