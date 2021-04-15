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
from typing import List, Optional

from PIL import Image, ImageTk

from mcts import MCTSTimeSavingPlayer
from reversi import ReversiGame, Player, RandomPlayer, GUIPlayer
from minimax_tree import MobilityTreePlayer, PositionalTreePlayer, GreedyTreePlayer
from constants import BLACK, WHITE, DEFAULT_FPS, index_to_algebraic


class TransparentButton:
    """
    Represents a button on a tkinter Canvas, modified to allow the button image to be transparent on
    a tkinter Canvas

     Instance Attributes:
        - pos: The position of the button, relative to the canvas
        - image: What the button looks like
        - action: An action representing what the button should do when pressed
    """
    pos: tuple[int, int]
    image: ImageTk.PhotoImage
    action: str

    def __init__(self, canvas: tk.Canvas, pos: tuple[int, int],
                 image: ImageTk.PhotoImage, action: str, text: str = '',
                 anchor: str = tk.NW) -> None:
        """Initialize the button on the canvas"""
        self.image = image
        self.pos = pos
        self.action = action
        canvas.create_image(pos, anchor=anchor, image=image)
        canvas.pack()

        if text != '':
            mid = (self.pos[0] + self.image.width() / 2,
                   self.pos[1] + self.image.height() / 2)

            font = ('Times', str(self.image.height() // 2), 'bold italic')
            canvas.create_text(mid, text=text, fill='white', font=font, activefill='red')

    def in_bounds(self, cords: tuple[int, int]) -> bool:
        """Returns whether the given coordinates are within the button bounds
        The bounds are based on the image size.
        """

        in_x = self.pos[0] < cords[0] < self.pos[0] + self.image.width()
        in_y = self.pos[1] < cords[1] < self.pos[1] + self.image.height()
        if in_x and in_y:
            return True
        else:
            return False


class VisualReversi:
    """
    An application that takes user input and visualizes a game of Reversi between selected
    algorithms

    Instance Attributes:
     - root: The root of the application
     - current_frame:  The window that the application is currently in
    """
    tk_root: tk.Tk
    current_frame: tk.Frame

    def __init__(self, tk_root: tk.Tk) -> None:
        """Initializes a the VisualReversi window, setting the current state to StartScreen"""
        tk_root.frame = StartScreen(self)
        self.tk_root = tk_root
        self.current_frame = tk_root.frame
        self.tk_root.title('Reversi')

    def frame_swap(self, frame: tk.Frame) -> None:
        """Change the current frame to the provided frame"""
        self.current_frame.destroy()
        self.current_frame = frame
        self.tk_root.frame = self.current_frame
        self.current_frame.pack()


class StartScreen(tk.Frame):
    """Represents a window state in which AI or Human Players are selected to play

      Instance Attributes:
         - _background_img: The background image of this window state
         - window: The window that is currently displaying this window state
         - _buttons: A list representing all the TransparentButton objects in the window
         - _background_img: The background image of the window

         Note: PhotoImage instances are stored as Instance Attributes because they are deleted
         otherwise, they may not be used outside of initialization.
     """
    window: VisualReversi
    _buttons: List[TransparentButton]
    _background_img: ImageTk.PhotoImage

    def __init__(self, window: VisualReversi) -> None:
        """initializes the main menu of the game"""
        tk.Frame.__init__(self)
        self.pack()
        self.window = window
        self._buttons = []

        # Create the background menu
        self._background_img = ImageTk.PhotoImage(Image.open("assets/main_menu.png"))
        canvas = tk.Canvas(self, width=self._background_img.width(),
                           height=self._background_img.height())
        canvas.create_image((0, 0), anchor=tk.NW, image=self._background_img)

        start = TransparentButton(canvas, (250, 320),
                                  ImageTk.PhotoImage(file="assets/blank_button.png"), 'start',
                                  'Start Game')
        quit_button = TransparentButton(canvas, (250, 380),
                                        ImageTk.PhotoImage(file="assets/blank_button.png"), 'quit',
                                        'Quit')
        self._buttons.append(start)
        self._buttons.append(quit_button)

        canvas.pack()
        canvas.bind('<Button-1>', self.menu_click)

    def menu_click(self, event: tk.EventType.Button) -> None:
        """Handles click events on Transparent buttons for the start menu
        """
        for button in self._buttons:
            if button.in_bounds((event.x, event.y)):
                if button.action == 'start':
                    self.window.frame_swap(AISelectScreen(self.window))
                else:
                    self.window.tk_root.destroy()
                    exit()


class AISelectScreen(tk.Frame):
    """Represents a window state in which AI or Human Players are selected to play

     Instance Attributes:
        - _background_img: The background image of this window state
        - _player_chosen: Whether the first AI has been selected
        - window: The window that is currently displaying this window state
        - _buttons: A list representing all the TransparentButton objects in the window
        - _player1: The first player chosen for a reversi game
        - _player2: The second player chosen for a reversi
        - _button_image: An image of a blank button
        - _text: Text representing user instructions
        - _background_img: The background image of the window

        Note: PhotoImage instances are stored as Instance Attributes because they are deleted
        otherwise, they may not be used outside of initialization.
    """
    window: VisualReversi
    _background_img: ImageTk.PhotoImage
    _buttons: List[TransparentButton]
    _player1: Optional[Player]
    _player2: Optional[Player]
    _text: tk.StringVar
    _player_chosen: False

    def __init__(self, window: VisualReversi) -> None:
        """initializes the main menu of the game"""
        tk.Frame.__init__(self)
        self.pack()
        self.window = window
        self._buttons = []
        self._player_chosen = False
        self._player1 = None
        self._player2 = None

        # Sets font sizes and title text
        title_font = ('Times', '50', 'bold italic')
        subtitle_font = ('Times', '15', 'bold italic')
        self._text = tk.StringVar(self, value='Select Black')
        label = tk.Label(self, textvariable=self._text, font=title_font)

        # Set the background image
        self._background_img = ImageTk.PhotoImage(Image.open("assets/unfocused_board.png"))
        canvas = tk.Canvas(self, width=self._background_img.width(),
                           height=self._background_img.height() - 100)
        canvas.create_image((0, 0), anchor=tk.NW, image=self._background_img)

        players = ['Human Player', 'Greedy Player', 'Mobility Player', 'Positional Player',
                   'Random Player', 'MCTS Player']

        increment = (self._background_img.height() - 200) / (len(players) + 1)
        mid = self._background_img.width() // 2
        canvas.create_text((mid, 40),
                           text='The Human Player is controlled with the mouse, '
                                'click a valid square on your turn to place a disc there.',
                           width=500, fill='white', font=subtitle_font, justify=tk.CENTER)
        start_y = 100
        for i in range(0, len(players)):
            button_pos = (250, start_y + i * increment)
            button = TransparentButton(canvas, button_pos,
                                       ImageTk.PhotoImage(file="assets/blank_button.png"),
                                       players[i], text=players[i])
            self._buttons.append(button)

            if i == len(players) - 1:
                _ = TransparentButton(canvas, (250, start_y + (i + 1) * increment),
                                      ImageTk.PhotoImage(file="assets/blank_button.png"),
                                      'Quit to Menu', text='Quit to Menu')
                self._buttons.append(_)
        label.pack(side=tk.TOP)
        canvas.pack(side=tk.BOTTOM)

        canvas.bind('<Button-1>', self.ai_select_trees)

    def set_player(self, first: bool, player: Player) -> None:
        """Set the games player, set the first player if first is true
        set the second player otherwise
        """
        if first:
            self._player1 = player
        else:
            self._player2 = player

    def ai_select_trees(self, event: tk.EventType.Button) -> None:
        """Selects an ai tree player when a Transparent button is clicked
        """

        for button in self._buttons:
            if button.in_bounds((event.x, event.y)):
                self._player_chosen = not self._player_chosen
                self._text.set('Select White')
                if button.action == 'Mobility Player':
                    self.set_player(self._player_chosen, MobilityTreePlayer(3))
                elif button.action == 'Positional Player':
                    self.set_player(self._player_chosen, PositionalTreePlayer(3))
                elif button.action == 'Greedy Player':
                    self.set_player(self._player_chosen, GreedyTreePlayer(3))
                elif button.action == 'Random Player':
                    self.set_player(self._player_chosen, RandomPlayer())
                elif button.action == 'MCTS Player':
                    self.set_player(self._player_chosen, MCTSTimeSavingPlayer(100, 8))
                elif button.action == 'Human Player':
                    self.set_player(self._player_chosen, GUIPlayer())
                elif button.action == 'Quit to Menu':
                    self.window.frame_swap(StartScreen(self.window))

                # Runs if the second player was just selected
                if not self._player_chosen and button.action != 'Quit to Menu':
                    self.window.frame_swap(
                        BoardSelectScreen(self.window, self._player1, self._player2))


class BoardSelectScreen(tk.Frame):
    """Represents a window state in which a board size is selected

     Instance Attributes:
        - _background_img: The background image of this window state

        - window: The window that is currently displaying this window state
        - _buttons: A list representing all the TransparentButton objects in the window
        - _player1: The first player of the game
        - _player2: The second player of the game
        - _button_img: An image of a blank button

        Note: PhotoImage instances are stored as Instance Attributes because they are deleted
        otherwise, they may not be used outside of initialization.
    """
    window: VisualReversi
    _buttons: List[TransparentButton]
    _player1: Player
    _player2: Player
    _button_img: ImageTk.PhotoImage
    _background_img: ImageTk.PhotoImage

    def __init__(self, window: VisualReversi, player1: Player, player2: Player) -> None:
        """initializes the main menu of the game"""
        tk.Frame.__init__(self)
        self.pack()
        self.window = window
        self._buttons = []
        self._player1 = player1
        self._player2 = player2

        # Create the background menu
        self._background_img = ImageTk.PhotoImage(Image.open("assets/unfocused_board.png"))
        canvas = tk.Canvas(self, width=self._background_img.width(),
                           height=self._background_img.height())
        canvas.create_image((0, 0), anchor=tk.NW, image=self._background_img)

        mid = (self._background_img.width() // 2, 100)

        font = ('Times', '50', 'bold italic')
        canvas.create_text(mid, text='Select a Board Size', width=500, fill='white', font=font,
                           justify=tk.CENTER)

        select_6 = Image.open('assets/othello_board6x6.png').resize((300, 300))
        select_8 = Image.open('assets/othello_board8x8.png').resize((300, 300))

        six = TransparentButton(canvas, (75, 200),
                                ImageTk.PhotoImage(select_6), '6')
        eight = TransparentButton(canvas, (self._background_img.width() - 75 - 300, 200),
                                  ImageTk.PhotoImage(select_8), '8')

        self._button_img = ImageTk.PhotoImage(Image.open('assets/blank_button.png'))
        button_6_pos = (six.pos[0] + six.image.width() // 2 - self._button_img.width() // 2,
                        six.pos[1] + six.image.height() + 20)

        button_8_pos = (eight.pos[0] + eight.image.width() // 2 - self._button_img.width() // 2,
                        eight.pos[1] + eight.image.height() + 20)

        button_6 = TransparentButton(canvas, button_6_pos, self._button_img, action='6', text='6x6')
        button_8 = TransparentButton(canvas, button_8_pos, self._button_img, action='8', text='8x8')

        self._buttons.append(six)
        self._buttons.append(eight)

        self._buttons.append(button_6)
        self._buttons.append(button_8)

        canvas.pack()
        canvas.bind('<Button-1>', self.board_select)

    def board_select(self, event: tk.EventType.Button) -> None:
        """Handles click events on Transparent buttons for the start menu
        """
        for button in self._buttons:
            if button.in_bounds((event.x, event.y)):
                if button.action == '8':
                    new_screen = GameScreen(self.window, 8)
                    self.window.frame_swap(new_screen)
                    new_screen.run_game(self._player1, self._player2)
                elif button.action == '6':
                    new_screen = GameScreen(self.window, 6)
                    self.window.frame_swap(new_screen)
                    new_screen.run_game(self._player1, self._player2)


class UIScreen(tk.Frame):
    """An abstract window that uses user input in a reversi game

    Instance Attributes:
        - _previous_move_dis: A string representing the previous move, used in the progress bar
        - _board_pixel_size: The size of the reversi board, in pixels, excluding the border
        - _board_pos: The top left corner of the reversi board, excluding the border
        - _click_move: The move made by the cursor, only relevant if a Human Player is playing
        - window: The window that is currently displaying this window state
        - _board_pixel_size: The size of an edge of the Reversi board, in pixels
        - previous_move_dis: A string to display the players previous move
        - _click_wanted: Represents if the window is waiting for player input
        - game: The ReversiGame being played

        Note: PhotoImage instances are stored as Instance Attributes because they are deleted
        otherwise, they may not be used outside of initialization.
    """
    _board_pos: tuple[int, int]
    _click_move: str
    window: VisualReversi
    _board_pixel_size: int
    previous_move_dis: str
    _click_wanted: tk.BooleanVar
    game: ReversiGame

    def __init__(self, window: VisualReversi, size: int) -> None:
        tk.Frame.__init__(self)
        self.window = window
        self._board_pos = (84, 120)
        self._board_pixel_size = 637
        self.previous_move_dis = ''

        self._click_wanted = tk.BooleanVar()

        # initialize game
        self.game = ReversiGame(size)


class GameScreen(UIScreen):
    """Represents the window state that shows the Reversi board

    Instance Attributes:
        - _background_img: The background image of this window state
        - _white_disk: A scaled image a white reversi disk
        - _black_disk: A scaled image a black reversi disk
        - _canvas: A tkinter Canvas on which game elements are drawn

        Note: PhotoImage instances are stored as Instance Attributes because they are deleted
        otherwise, they may not be used outside of initialization.
    """

    _background_img: ImageTk.PhotoImage
    _white_disk: ImageTk.PhotoImage
    _black_disk: ImageTk.PhotoImage
    _canvas: tk.Canvas

    def __init__(self, window: VisualReversi, size: int) -> None:
        """initialize gui

        Preconditions:
            - size == 8 or size == 6
        """
        # setting up
        super().__init__(window, size)

        # Open a scale disc images to fit the window
        w = Image.open('assets/chess/white8.png')
        b = Image.open('assets/chess/black8.png')
        width = int(self._board_pixel_size / size * 0.65)
        w = w.resize((width, width))
        b = b.resize((width, width))

        self._white_disk = ImageTk.PhotoImage(w)
        self._black_disk = ImageTk.PhotoImage(b)

        if size == 8:
            self._background_img = ImageTk.PhotoImage(Image.open('assets/othello_board8X8.png'))
        else:
            self._background_img = ImageTk.PhotoImage(Image.open('assets/othello_board6X6.png'))

        self._canvas = tk.Canvas(self, width=self._background_img.width(),
                                 height=self._background_img.height())
        self._canvas.create_image((0, 0), anchor=tk.NW, image=self._background_img)

        self._canvas.bind('<Button-1>', self.click)
        self._click_move = ''

        self._canvas.pack()

    def _update_progress_bar(self) -> None:
        """ Draws text onto the Canvas with information about the game"""

        # bar_y is the height of the progress bar
        bar_y = 20
        mid_x = self._background_img.width() // 2
        font = ('Times', '15', 'bold italic')

        # Display the score of both players:
        score_text = 'Black: ' + str(self.game.get_num_pieces()[BLACK]) + "  " + 'White: ' + str(
            self.game.get_num_pieces()[WHITE])
        self._canvas.create_text((15, bar_y), text=score_text, fill='white', font=font,
                                 anchor=tk.W)

        # Display who's turn it is
        if self.game.get_current_player() == BLACK:
            self._canvas.create_text((mid_x, bar_y), text='Black\'s turn', fill='white', font=font)
        else:
            self._canvas.create_text((mid_x, bar_y), text='White\'s turn', fill='white', font=font)

        # Display the previous move
        end = self._background_img.width() - 15
        self._canvas.create_text((end, bar_y), text=self.previous_move_dis,
                                 fill='white', font=font, anchor=tk.E)

    def run_game(self, black: Player, white: Player, fps: int = DEFAULT_FPS) -> None:
        """Run a Reversi game between the two given players.

        Return the winner and list of moves made in the game.
        """
        previous_move = None
        current_player = black
        self._draw_game_state()
        self._update_progress_bar()

        while self.game.get_winner() is None:
            previous_move = current_player.make_move(self.game, previous_move)

            if previous_move != 'mouse_pos':
                self.game.make_move(previous_move)
                self._draw_game_state()
                time.sleep(1 / fps)
                self.window.tk_root.update()
            else:
                previous_move = self._gui_move()

            if current_player is black:
                self.previous_move_dis = 'Black moved: ' + previous_move
                current_player = white
            else:
                self.previous_move_dis = 'White moved: ' + previous_move
                current_player = black

            self._update_progress_bar()

        self.win_msg()
        print(self.game.get_winner())

    def _gui_move(self) -> str:
        """Makes a move for the gui player"""
        if self.game.get_valid_moves() == ['pass']:
            return 'pass'
        else:
            self._click_wanted.set(True)
            self.window.tk_root.wait_variable(self._click_wanted)
            return self._click_move

    def _draw_game_state(self) -> None:
        """Visualize the board on the windows canvas"""
        lst = self.game.get_game_board()

        board_pos = (84, 120)

        x = self._board_pixel_size / self.game.get_size()
        y = self._board_pixel_size / self.game.get_size()

        inset = x / 2

        # colours = {WHITE: 'white', BLACK: 'black'}

        images = {WHITE: self._white_disk, BLACK: self._black_disk}

        self._canvas.create_image((0, 0), anchor=tk.NW, image=self._background_img)

        for r in range(0, self.game.get_board_size()):
            for c in range(0, self.game.get_board_size()):

                if lst[r][c] in {WHITE, BLACK}:
                    # colour = colours[lst[r][c]]

                    top = (c * x + inset + board_pos[0], r * y + inset + board_pos[1])
                    self._canvas.create_image(top, image=images[lst[r][c]])

    def click(self, event: tk.EventType.Button) -> None:
        """Called when mouse is clicked on the given canvas
        Finds the relative position of the click and executes a move"""

        if self._click_wanted.get():
            xcor = (event.x - self._board_pos[0]) // (self._board_pixel_size / self.game.get_size())
            ycor = (event.y - self._board_pos[1]) // (self._board_pixel_size / self.game.get_size())

            if 0 <= xcor <= self.game.get_size() and 0 <= ycor <= self.game.get_size():
                pos = (ycor, xcor)
                move = index_to_algebraic(pos)
                if move in self.game.get_valid_moves():
                    self.game.make_move(move)
                    self._click_move = move
                    self._draw_game_state()
                    self.window.tk_root.update()
                    self._click_wanted.set(False)
                    return

    def quit(self) -> None:
        """quit the entire game"""
        self.window.tk_root.destroy()
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

    def restart(self) -> None:
        """return to GameStartScreen"""
        self.window.frame_swap(StartScreen(self.window))


def run_app() -> None:
    """Creates the tk root and runs the Reversi application"""
    root = tk.Tk()
    VisualReversi(root)
    root.mainloop()


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['tkinter', 'time', 'PIL', 'mcts', 'reversi', 'minimax_tree', 'constants'],
        # the names (strs) of imported modules
        'allowed-io': ['run_game'],  # the names (strs) of functions that call print/open/input
        'max-line-length': 100,
        'disable': ['E1136', 'R0913']
    })
