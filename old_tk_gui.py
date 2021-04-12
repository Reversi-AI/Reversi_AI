import tkinter as tk
import time

from mcts import MCTSTimeSavingPlayer
from minimax import MobilityPlayer, PositionalPlayer
from reversi import ReversiGame, Player, RandomPlayer, GUIPlayer
from constants import BLACK, WHITE, DEFAULT_FPS, index_to_algebraic
from typing import Optional


class ReversiGUI:
    """
    GUI class for the Reversi Game
    This class is responsible for starting a game board, handling game click events, and processing
    and updating current board.
    """

    def __init__(self, parent: tk.Tk, size: int) -> None:
        """initialize gui

        Preconditions:
            - size == 8 or size == 6

        :param parent: tkinter root object
        :param size: size of the game, which is either 8 or 6
        """
        # setting up
        self.root = parent
        self.root.title('Reversi')
        self.frame = tk.Frame(parent)
        self.status_bar = None

        self.status_bar = tk.Frame(self.root, bg='blue')
        self.status_bar.pack()

        self.piece_count_dis = tk.Label(self.status_bar, text='Black: 2, White:2', width=20,
                                        anchor='w',
                                        font=('Helvetica', 16))
        self.piece_count_dis.grid(row=0, column=0)
        self.current_player_dis = tk.Label(self.status_bar, text='Current Player: Black', width=20,
                                           anchor='center', font=('Helvetica', 16))
        self.current_player_dis.grid(row=0, column=1)
        self.previous_move_dis = tk.Label(self.status_bar, text='', width=20, anchor='e',
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

    def run_game(self, black: Player, white: Player, fps: int = DEFAULT_FPS) -> None:
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
            xcor = event.x // (self.board.winfo_width() / self.game.get_size())
            ycor = event.y // (self.board.winfo_height() / self.game.get_size())

            pos = (ycor, xcor)
            move = index_to_algebraic(pos)
            print(move)
            if move in self.game.get_valid_moves():
                self.game.make_move(move)
                self.click_move = move
                self.draw_game_state()
                self.root.update()
                self.click_wanted.set(False)
                return

    def quit(self) -> None:
        """quit the entire game"""
        self.root.destroy()
        exit()

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
        b1 = tk.Button(popup, text="quit game", command=lambda: [popup.destroy(), self.quit()])
        b2 = tk.Button(popup, text="return to menu",
                       command=lambda: [popup.destroy(), self.restart()])
        b1.pack()
        b2.pack()
        popup.mainloop()

    def start_page(self) -> None:
        """this method allows the root to call on the game's frame --> basically allowing screen
        switching"""
        self.frame.pack()

    def restart(self) -> None:
        """return to GameStartScreen"""
        self.frame.pack_forget()
        self.status_bar.pack_forget()
        page_1 = GameStartScreen(self.root)
        page_1.main_page()

class GameStartScreen:
    """
    starting screen of the game
    """

    def __init__(self, root=None) -> None:
        """initializes the main menu of the game"""
        self.root = root
        self.frame = tk.Frame(self.root)
        self.frame.pack()
        player_choices = ['Mobility Player', 'Positional Player', 'Random Player',
                          'MCTS Player']
        board_choices = ['6', '8']
        variable_player = tk.StringVar(root)
        variable_player.set('MCTS Player')
        variable_board = tk.StringVar(root)
        variable_board.set('8')
        tk.Label(self.frame, text='Reversi').pack()
        tk.Button(self.frame, text='start game', command=self.start_game).pack()
        tk.Button(self.frame, text='quit game', command=self.quit_game).pack()
        tk.OptionMenu(self.frame, variable_player, *player_choices,
                      command=self.set_player).pack()
        tk.OptionMenu(self.frame, variable_board, *board_choices, command=self.set_board).pack()
        self.page_1 = None
        self.player = None
        self.boardsize = None

    def main_page(self) -> None:
        """allows this frame to be packed and called at another time"""
        self.frame.pack()

    def start_game(self) -> None:
        """start game button clicked. starts the reversi gaame with the selected parameters"""
        if self.player is not None and self.boardsize is not None:
            self.frame.pack_forget()
            self.page_1 = ReversiGUI(self.root, size=self.boardsize)
            self.page_1.start_page()
            self.page_1.run_game(GUIPlayer(), self.player, self.boardsize)
        else:
            # print('please select a player and/or a board size')
            self.frame.pack_forget()
            self.page_1 = ReversiGUI(self.root, size=8)
            self.page_1.start_page()
            self.page_1.run_game(GUIPlayer(), MCTSTimeSavingPlayer(100, 8), 8)

    def set_player(self, value) -> None:
        """drop down menu selecting AI player"""
        if value == 'Mobility Player':
            self.player = MobilityPlayer(3)
        elif value == 'Positional Player':
            self.player = PositionalPlayer(3)
        elif value == 'Random Player':
            self.player = RandomPlayer()
        else:
            self.player = MCTSTimeSavingPlayer(500, 15)

    def set_board(self, value) -> None:
        """drop down menu selecting board size"""
        if value == '8':
            self.boardsize = 8
        else:
            self.boardsize = 6

    def quit_game(self) -> None:
        """quit the entire game"""
        self.root.destroy()
        exit()


if __name__ == '__main__':
    root = tk.Tk()
    app = GameStartScreen(root)
    root.mainloop()
