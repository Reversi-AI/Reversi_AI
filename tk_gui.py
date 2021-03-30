import tkinter as tk
import time

from reversi import ReversiGame, Player, RandomPlayer
from constants import BLACK, WHITE



class ReversiGUI:
    """"""
    def __init__(self, parent, size, player1, player2) -> None:
        """initialize gui"""
        # setting up
        self.root = parent
        self.root.title('Reversi')
        self.frame = tk.Frame(parent)
        self.board = tk.Canvas(height=500, width=500, bg='black')
        self.frame.pack()

        # initialize game
        self.game = ReversiGame(size)
        self.player1 = player1
        self.player2 = player2
        self.draw_game_state()

        # run game
        self.run_game(self.player1, self.player2)

    def run_game(self, black, white) -> None:
        """Run a Reversi game between the two given players.

        Return the winner and list of moves made in the game.
        """
        previous_move = None
        current_player = black
        self.draw_game_state()

        while self.game.get_winner() is None:
            previous_move = current_player.make_move(self.game, previous_move)
            self.game.make_move(previous_move)
            self.draw_game_state()
            time.sleep(1)
            root.update()

            if current_player is black:
                current_player = white
            else:
                current_player = black

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


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('500x500')
    gui = ReversiGUI(root, 8, RandomPlayer(), RandomPlayer())
    root.deiconify()
    root.mainloop()
