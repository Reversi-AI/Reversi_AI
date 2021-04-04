import tkinter as tk
import time

from reversi import ReversiGame, Player, RandomPlayer, _index_to_algebraic, GUIPlayer
from constants import BLACK, WHITE, DEFAULT_FPS
from typing import Optional


class ReversiGUI:
    """
    GUI class for the Reversi Game
    This class is responsible for starting a game board, handling game click events, and processing
    and updating current board.
    """

    def __init__(self, parent, size) -> None:
        """initialize gui"""
        # setting up
        self.root = parent
        self.root.title('Reversi')
        self.frame = tk.Frame(parent)

        status_bar = tk.Frame(self.root, bg='blue')
        status_bar.pack()

        self.piece_count_dis = tk.Label(status_bar, text='Black: 2, White:2', width=20, anchor='w',
                                        font=('Helvetica', 16))
        self.piece_count_dis.grid(row=0, column=0)
        self.current_player_dis = tk.Label(status_bar, text='Current Player: Black', width=20,
                                           anchor='center', font=('Helvetica', 16))
        self.current_player_dis.grid(row=0, column=1)
        self.previous_move_dis = tk.Label(status_bar, text='', width=20, anchor='e',
                                          font=('Helvetica', 16))
        self.previous_move_dis.grid(row=0, column=2)

        self.board = tk.Canvas(self.frame, height=500, width=500, bg='black', bd=-2)
        self.board.pack(pady=10)
        self.frame.pack()
        self.click_wanted = tk.BooleanVar()
        self.board.bind('<Button-1>', self.click)
        self.click_move = ''

        # initialize game
        self.game = ReversiGame(size)
        self.draw_game_state()

    def run_game(self, black, white, fps: int = DEFAULT_FPS) -> None:
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
                self.draw_game_state(previous_move)
                time.sleep(1 / fps)
                self.root.update()
            else:
                previous_move = self.gui_move()

            if current_player is black:
                current_player = white
            else:
                current_player = black

        # update status bar
        if self.game.get_winner() == BLACK:
            self.current_player_dis.config(text='Black wins!')
        elif self.game.get_winner() == WHITE:
            self.current_player_dis.config(text='White wins!')
        else:
            self.current_player_dis.config(text='Draw')
        self.win_msg()

        print(self.game.get_winner())

    def gui_move(self) -> str:
        """Makes a move for the gui player"""
        if all(len(m) != 2 for m in self.game.get_valid_moves()):
            return 'pass'
        else:
            self.click_wanted.set(True)
            self.root.wait_variable(self.click_wanted)
            return self.click_move

    def draw_game_state(self, previous_move: Optional[str] = None,
                        h: int = 500, w: int = 500) -> None:
        """Visualize the game by drawing in the window"""
        # update status bar
        num_piece = self.game.get_num_pieces()
        self.piece_count_dis.config(text=f'Black: {num_piece[BLACK]}, White: {num_piece[WHITE]}')
        active_player = self.game.get_current_player()
        if active_player == BLACK:
            self.current_player_dis.config(text='Current player: Black')
            if previous_move is not None:
                self.previous_move_dis.config(text=f'White moved {previous_move}')
        else:
            self.current_player_dis.config(text='Current player: White')
            if previous_move is not None:
                self.previous_move_dis.config(text=f'Black moved {previous_move}')

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
        """Called when mouse is clicked on the given canvas
        Finds the relative position of the click and executes a move"""
        if self.click_wanted.get():
            xcor = event.x // (self.board.winfo_width() / 8)
            ycor = event.y // (self.board.winfo_height() / 8)

            pos = (ycor, xcor)
            move = _index_to_algebraic(pos)
            print(move)
            if move in self.game.get_valid_moves():
                self.game.make_move(move)
                self.click_move = move
                self.draw_game_state()
                self.root.update()
                self.click_wanted.set(False)
                return

    def win_msg(self) -> None:
        """popup window for game ending. Contains winner information."""
        popup = tk.Tk()
        popup.wm_title("Game Over")
        if self.game.get_winner() == WHITE:
            msg = "White wins"
        elif self.game.get_winner() == BLACK:
            msg = "Black wins"
        else:
            msg = "It's a draw"
        label = tk.Label(popup, text=msg)
        label.pack(side="top", fill="x", pady=20)
        b1 = tk.Button(popup, text="Okay", command=popup.destroy)
        b1.pack()
        popup.mainloop()


if __name__ == '__main__':
    root = tk.Tk()
    gui = ReversiGUI(root, 8)
    # gui.run_game(RandomPlayer(), RandomPlayer())
    # gui.run_game(GUIPlayer(), RandomPlayer())
    root.mainloop()
