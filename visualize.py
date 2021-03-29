import tkinter as tk

from reversi import ReversiGame, Player
from constants import BLACK, WHITE, BOARD_WEIGHT_8, BOARD_WEIGHT_6
import time
import minimax

class TestWindow(tk.Frame):


    def __init__(self, master = None) -> None:
        super().__init__(master)
        self.master = master
        self.pack()


class ReversiApplication(tk.Frame):
    quit: tk.Button
    board: tk.Canvas

    def __init__(self, master=None, ) -> None:
        super().__init__(master)
        self.master = master
        self.pack()
        # self.create_widgets()
        self.board = tk.Canvas(height=500, width=500, bg='black')
        self.board.pack()

    # def create_widgets(self) -> None:
    #     """"""
    #     self.hi_there = tk.Button(self)
    #     self.hi_there["text"] = "Hello World\n(click me)"
    #     self.hi_there["command"] = self.say_hi
    #     self.hi_there.pack(side="top")
    #
    #     self.quit = tk.Button(self, text="QUIT", fg="red",
    #                           command=self.master.destroy)
    #     self.quit.pack(side="bottom")
    #
    # def say_hi(self) -> None:
    #     print("hi there, everyone!")

    def draw_game_state(self, game: ReversiGame, h=500, w=500):
        """Visualize the game by drawing on the Canvas"""
        # self.board = tk.Canvas(height=h, width=w, bg='black')

        lst = game.get_game_board()

        x = w / game.get_size()
        y = h / game.get_size()

        inset = x / 5

        colours = {WHITE: 'white', BLACK: 'black'}

        for r in range(0, game.get_board_size()):
            for c in range(0, game.get_board_size()):
                self.board.create_rectangle(c * x, r * y, (c + 1) * x, (r + 1) * y,
                                            fill='green4', outline='dark green', width=5)

                if lst[r][c] in {WHITE, BLACK}:
                    colour = colours[lst[r][c]]

                    self.board.create_oval(c * x + inset, r * y + inset, (c + 1) * x - inset,
                                           (r + 1) * y - inset, fill=colour, outline='black',
                                           width=0)

        self.board.pack()



def big_move(a: ReversiApplication) -> None:
    while(True):
        print('WOW')
        time.sleep(1)
        a.after(a.mainloop())

def testing_window() -> None:
    root = tk.Tk()
    window = ReversiApplication(master=root)
    game = ReversiGame(8)
    window.draw_game_state(game)
    window.mainloop()
