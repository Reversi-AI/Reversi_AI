"""Reversi Game GUI implementation

Module Description
===============================

This module contains a collection of classes and functions which implements the GUI
the Reversi Game with Tkinter.

Copyright and Usage Information
===============================

Authors:
    - Haoze Deng
    - Peifeng Zhang
    - Man Chon Ho
    - Alexander Nicholas Conway

This file is Copyright (c) 2021.
"""
import tkinter as tk
import time
from PIL import Image, ImageTk

from mcts import MCTSTimeSavingPlayer
from minimax import MobilityPlayer, PositionalPlayer
from reversi import ReversiGame, Player, RandomPlayer, _index_to_algebraic, GUIPlayer
from constants import BLACK, WHITE, DEFAULT_FPS
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
            move = _index_to_algebraic(pos)
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
        page_1 = GameStartScreen(root)
        page_1.main_page()


class TransparentButton:
    """
    A class represents a class on a tkinter Canvas, so that
    it supports transparency.
    """
    pos: tuple[int, int]
    image: ImageTk.PhotoImage
    action: str

    def __init__(self, canvas: tk.Canvas, pos: tuple[int, int],
                 image: ImageTk.PhotoImage, action: callable, anchor=tk.NW):
        """initalize the button on the canvas"""
        self.image = image
        self.pos = pos
        self.action = action
        canvas.create_image(pos, anchor=anchor, image=image)
        canvas.pack()

    def in_bounds(self, cords: tuple[int, int]) -> bool:
        """Returns whether the given coordinates are within the button bounds
        """

        in_x = self.pos[0] < cords[0] < self.pos[0] + self.image.width()
        in_y = self.pos[1] < cords[1] < self.pos[1] + self.image.height()
        if in_x and in_y:
            return True
        else:
            return False


class VisualReversi:
    """
    Another starting screen
    """
    player1: Optional[Player]
    player2: Optional[Player]

    def __init__(self, root: tk.Tk) -> None:
        """initializes the main menu of the game"""
        root.frame = StartScreen(self)
        self.player1 = None
        self.player2 = None
        # root.frame.destroy()
        # root.frame = AISelectScreen(self)
        self.root = root
        self.current_frame = root.frame
        # self.frame.pack()
        # self.frame.destroy()
        # self.frame.pack_forget()
        # self.frame = AISelectScreen(self)

    def frame_swap(self, frame: tk.Frame) -> None:
        """Change the current frame to the provided frame"""
        self.current_frame.destroy()
        self.current_frame = frame
        self.root.frame = self.current_frame
        self.current_frame.pack()

    def set_player(self, first: bool, player: Player) -> None:
        """Set the games player, set the first player if first is true
        set the second player otherwise
        """
        if first:
            self.player1 = player
        else:
            self.player2 = player


class StartScreen(tk.Frame):
    """The starting menu of the game"""

    def __init__(self, window: VisualReversi) -> None:
        """initializes the main menu of the game"""
        tk.Frame.__init__(self)
        self.pack()
        self.window = window
        self.buttons = []

        # Create the background menu
        self.background_img = ImageTk.PhotoImage(Image.open("assets/main_menu.png"))
        canvas = tk.Canvas(self, width=self.background_img.width(),
                           height=self.background_img.height())
        canvas.create_image((0, 0), anchor=tk.NW, image=self.background_img)

        start = TransparentButton(canvas, (250, 320),
                                  ImageTk.PhotoImage(file="assets/start_button.png"), 'start')
        quit = TransparentButton(canvas, (250, 380),
                                 ImageTk.PhotoImage(file="assets/quit_button.png"), 'quit')
        self.buttons.append(start)
        self.buttons.append(quit)

        canvas.pack()
        canvas.bind('<Button-1>', self.menu_click)

    def menu_click(self, event) -> None:
        """Handles click events on Transparent buttons for the start menu
        """
        for button in self.buttons:
            if button.in_bounds((event.x, event.y)):
                if button.action == 'start':
                    print('starting')
                    self.window.frame_swap(AISelectScreen(self.window))
                else:
                    print('quiting')


class AISelectScreen(tk.Frame):
    """Window where AI players are selected"""

    def __init__(self, window: VisualReversi) -> None:
        """initializes the main menu of the game"""
        tk.Frame.__init__(self)
        self.pack()
        self.window = window
        self.buttons = []
        self.player_chosen = False

        # Create the background menu
        self.background_img = ImageTk.PhotoImage(Image.open("assets/main_menu.png"))
        canvas = tk.Canvas(self, width=self.background_img.width(),
                           height=self.background_img.height())
        canvas.create_image((0, 0), anchor=tk.NW, image=self.background_img)

        players = ['Mobility Player', 'Positional Player', 'Random Player', 'MCTS Player',
                   'AI Simulation']

        increment = 100
        for i in range(0, len(players)):
            _ = TransparentButton(canvas, (250, 150 + i * increment),
                                  ImageTk.PhotoImage(file="assets/ai_button.png"), players[i])
            self.buttons.append(_)

            if i == len(players) - 1:
                _ = TransparentButton(canvas, (250, 150 + (i + 1) * increment),
                                      ImageTk.PhotoImage(file="assets/ai_button.png"),
                                      'quit to menu')
                self.buttons.append(_)

        canvas.pack()
        canvas.bind('<Button-1>', self.ai_select)

    def ai_select(self, event) -> None:
        """Handles click events on Transparent buttons for the start menu
        """
        for button in self.buttons:
            if button.in_bounds((event.x, event.y)):
                self.player_chosen = not self.player_chosen
                if button.action == 'Mobility Player':
                    self.window.set_player(self.player_chosen, MobilityPlayer(3))
                elif button.action == 'Positional Player':
                    self.window.set_player(self.player_chosen, PositionalPlayer(3))
                elif button.action == 'Random Player':
                    self.window.set_player(self.player_chosen, RandomPlayer())
                elif button.action == 'MCTS Player':
                    self.window.set_player(self.player_chosen, MCTSTimeSavingPlayer(500, 15))

                # Runs if the second player was just selected
                if not self.player_chosen:
                    self.window.frame_swap(BoardSelectScreen(self.window))


class BoardSelectScreen(tk.Frame):
    """Window where AI players are selected"""

    def __init__(self, window: VisualReversi) -> None:
        """initializes the main menu of the game"""
        tk.Frame.__init__(self)
        self.pack()
        self.window = window
        self.buttons = []

        # Create the background menu
        self.background_img = ImageTk.PhotoImage(Image.open("assets/main_menu.png"))
        canvas = tk.Canvas(self, width=self.background_img.width(),
                           height=self.background_img.height())
        canvas.create_image((0, 0), anchor=tk.NW, image=self.background_img)

        start = TransparentButton(canvas, (250, 320),
                                  ImageTk.PhotoImage(file="assets/ai_button.png"), '8')
        quit = TransparentButton(canvas, (250, 380),
                                 ImageTk.PhotoImage(file="assets/ai_button.png"), '6')
        self.buttons.append(start)
        self.buttons.append(quit)

        canvas.pack()
        canvas.bind('<Button-1>', self.ai_select)

    def ai_select(self, event) -> None:
        """Handles click events on Transparent buttons for the start menu
        """
        for button in self.buttons:
            if button.in_bounds((event.x, event.y)):
                if button.action == '8':
                    new_screen = GameScreen(self.window, 8, self.window.player1,
                                            self.window.player2)
                    self.window.frame_swap(new_screen)
                    new_screen.run_game(self.window.player1, self.window.player2)
                elif button.action == '6':
                    new_screen = GameScreen(self.window, 6, self.window.player1,
                                            self.window.player2)
                    self.window.frame_swap(new_screen)
                    new_screen.run_game(self.window.player1, self.window.player2)


class GameScreen(tk.Frame):

    def __init__(self, window: VisualReversi, size: int, player1: Player, player2: Player) -> None:
        """initialize gui

        Preconditions:
            - size == 8 or size == 6

        :param parent: tkinter root object
        :param size: size of the game, which is either 8 or 6
        """
        # setting up
        # self.root = parent
        tk.Frame.__init__(self)
        self.window = window
        self.root = window.root
        self.board_pos = (84, 120)
        self.board_pixel_size = 637

        w = Image.open('assets/chess/white8.png')
        b = Image.open('assets/chess/black8.png')
        width = int(self.board_pixel_size / size * 0.65)
        w = w.resize((width, width))
        b = b.resize((width, width))

        self.white_disk = ImageTk.PhotoImage(w)
        self.black_disk = ImageTk.PhotoImage(b)


        # self.root.title('Reversi')
        # self.frame = tk.Frame(parent)
        # self.status_bar = None
        #
        # self.status_bar = tk.Frame(self.window.root, bg='blue')
        # self.status_bar.pack()
        #
        # self.piece_count_dis = tk.Label(self.status_bar, text='Black: 2, White:2', width=20,
        #                                 anchor='w',
        #                                 font=('Helvetica', 16))
        # self.piece_count_dis.grid(row=0, column=0)
        # self.current_player_dis = tk.Label(self.status_bar, text='Current Player: Black', width=20,
        #                                    anchor='center', font=('Helvetica', 16))
        # self.current_player_dis.grid(row=0, column=1)
        # self.previous_move_dis = tk.Label(self.status_bar, text='', width=20, anchor='e',
        #                                   font=('Helvetica', 16))
        # self.previous_move_dis.grid(row=0, column=2)

        if size == 8:
            self.background_img = ImageTk.PhotoImage(Image.open('assets/othello_board8X8.png'))
        else:
            self.background_img = ImageTk.PhotoImage(Image.open('assets/othello_board6X6.png'))

        self.canvas = tk.Canvas(self, width=self.background_img.width(),
                                height=self.background_img.height())
        self.canvas.create_image((0, 0), anchor=tk.NW, image=self.background_img)

        # self.board = tk.Canvas(self, height=500, width=500, bg='black', bd=-2)
        # self.board.pack(pady=10)
        # self.pack()
        self.click_wanted = tk.BooleanVar()
        self.canvas.bind('<Button-1>', self.click)
        self.click_move = ''

        self.canvas.pack()

        # initialize game
        self.game = ReversiGame(size)
        # self.draw_game_state()
        # self.run_game(player1, player2)

    def run_game(self, black: Player, white: Player, fps: int = DEFAULT_FPS) -> None:
        """Run a Reversi game between the two given players.

        Return the winner and list of moves made in the game.
        """
        previous_move = None
        current_player = black
        self.draw_game_state()

        while self.game.get_winner() is None:
            previous_move = current_player.make_move(self.game, previous_move)
            print(previous_move)
            if previous_move != 'mouse_pos':
                self.game.make_move(previous_move)
                self.draw_game_state(previous_move)
                time.sleep(1 / fps)
                self.window.root.update()
            else:
                previous_move = self.gui_move()

            if current_player is black:
                current_player = white
            else:
                current_player = black

        # update status bar
        # if self.game.get_winner() == BLACK:
        #     self.current_player_dis.config(text='Black wins!')
        # elif self.game.get_winner() == WHITE:
        #     self.current_player_dis.config(text='White wins!')
        # else:
        #     self.current_player_dis.config(text='Draw')
        # self.win_msg()
        #
        # print(self.game.get_winner())

    def gui_move(self) -> str:
        """Makes a move for the gui player"""
        if all(len(m) != 2 for m in self.game.get_valid_moves()):
            return 'pass'
        else:
            self.click_wanted.set(True)
            self.window.root.wait_variable(self.click_wanted)
            return self.click_move

    def draw_game_state(self, previous_move: Optional[str] = None) -> None:
        """Visualize the game by drawing in the window"""
        # update status bar
        num_piece = self.game.get_num_pieces()
        # self.piece_count_dis.config(text=f'Black: {num_piece[BLACK]}, White: {num_piece[WHITE]}')
        active_player = self.game.get_current_player()
        # if active_player == BLACK:
        #     self.current_player_dis.config(text='Current player: Black')
        #     if previous_move is not None:
        #         self.previous_move_dis.config(text=f'White moved {previous_move}')
        # else:
        #     self.current_player_dis.config(text='Current player: White')
        #     if previous_move is not None:
        #         self.previous_move_dis.config(text=f'Black moved {previous_move}')

        lst = self.game.get_game_board()

        board_pos = (84, 120)

        x = self.board_pixel_size / self.game.get_size()
        y = self.board_pixel_size / self.game.get_size()

        inset = x / 2

        colours = {WHITE: 'white', BLACK: 'black'}


        images = {WHITE: self.white_disk, BLACK: self.black_disk}

        self.canvas.create_image((0, 0), anchor=tk.NW, image=self.background_img)

        for r in range(0, self.game.get_board_size()):
            for c in range(0, self.game.get_board_size()):
                # self.board.create_rectangle(c * x, r * y, (c + 1) * x, (r + 1) * y,
                #                             fill='green4', outline='dark green', width=5)

                if lst[r][c] in {WHITE, BLACK}:
                    colour = colours[lst[r][c]]

                    top = (c * x + inset + board_pos[0], r * y + inset + board_pos[1])
                    # bottom = (
                    # (c + 1) * x - inset + board_pos[0], (r + 1) * y - inset + board_pos[1])
                    # self.canvas.create_oval(top[0], top[1], bottom[0],
                    #                         bottom[1], fill=colour, outline='black', width=0)
                    self.canvas.create_image(top, image =images[lst[r][c]])

        # self.board.pack()

    def click(self, event) -> None:
        """Called when mouse is clicked on the given canvas
        Finds the relative position of the click and executes a move"""

        if self.click_wanted.get():
            xcor = (event.x - self.board_pos[0]) // (self.board_pixel_size / self.game.get_size())
            ycor = (event.y - self.board_pos[1]) // (self.board_pixel_size / self.game.get_size())

            if 0 <= xcor <= self.game.get_size() and 0 <= ycor <= self.game.get_size():
                pos = (ycor, xcor)
                move = _index_to_algebraic(pos)
                print(move)
                if move in self.game.get_valid_moves():
                    self.game.make_move(move)
                    self.click_move = move
                    self.draw_game_state()
                    self.window.root.update()
                    self.click_wanted.set(False)
                    return

    def quit(self) -> None:
        """quit the entire game"""
        self.window.root.destroy()
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

    # def start_page(self) -> None:
    #     """this method allows the root to call on the game's frame --> basically allowing screen
    #     switching"""
    #     self.frame.pack()

    def restart(self) -> None:
        """return to GameStartScreen"""
        # self.frame.pack_forget()
        # self.status_bar.pack_forget()
        # page_1 = GameStartScreen(root)
        # page_1.main_page()


class GameStartScreen:
    """
    starting screen of the game
    """

    def __init__(self, root=None) -> None:
        """initializes the main menu of the game"""
        self.root = root
        self.frame = tk.Frame(self.root)
        self.frame.pack()
        player_choices = ['Mobility Player', 'Positional Player', 'Random Player', 'MCTS Player']
        board_choices = ['6', '8']
        variable_player = tk.StringVar(root)
        variable_player.set('MCTS Player')
        variable_board = tk.StringVar(root)
        variable_board.set('8')
        tk.Label(self.frame, text='Reversi').pack()
        tk.Button(self.frame, text='start game', command=self.start_game).pack()
        tk.Button(self.frame, text='quit game', command=self.quit_game).pack()
        tk.OptionMenu(self.frame, variable_player, *player_choices, command=self.set_player).pack()
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
    # root = tk.Tk()
    # gui = ReversiGUI(root, 8)
    # # gui.run_game(RandomPlayer(), RandomPlayer())
    # # gui.run_game(GUIPlayer(), RandomPlayer())
    # root.mainloop()
    root = tk.Tk()
    # app = GameStartScreen(root)
    app = VisualReversi(root)
    root.mainloop()
    # run this file to see the current game starting screen, it's a bit crude right now
