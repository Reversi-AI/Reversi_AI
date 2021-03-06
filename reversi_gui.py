"""Reversi GUI

Module Description
===============================

This module contains all GUI of a reversi game application.

Copyright and Usage Information
===============================

Authors:
    - Haoze Deng
    - Peifeng Zhang
    - Man Chon Ho
    - Alexander Nicholas Conway

This file is Copyright (c) 2021.
"""
from typing import Optional, Union
import pygame

from mcts import MCTSTimeSavingPlayer

from minimax_tree import MobilityTreePlayer, PositionalTreePlayer
from reversi import RandomPlayer, ReversiGame
from constants import BLACK, WHITE, INDEX_TO_COL, INDEX_TO_ROW

DEFAULT_DPI = (800, 800)
DEFAULT_WH_RATIO = 1
BUTTON_SIZE = (280, 55)

BOARD_6 = {'a1': (85, 610), 'a2': (85, 500), 'a3': (85, 385), 'a4': (90, 275), 'a5': (90, 165),
           'a6': (90, 60),
           'b1': (195, 610), 'b2': (195, 500), 'b3': (195, 385), 'b4': (200, 275), 'b5': (200, 165),
           'b6': (200, 60),
           'c1': (300, 610), 'c2': (300, 500), 'c3': (300, 385), 'c4': (305, 275), 'c5': (305, 165),
           'c6': (305, 60),
           'd1': (405, 610), 'd2': (405, 500), 'd3': (405, 385), 'd4': (410, 275), 'd5': (410, 165),
           'd6': (410, 60),
           'e1': (515, 610), 'e2': (515, 500), 'e3': (515, 385), 'e4': (515, 275), 'e5': (519, 165),
           'e6': (519, 60),
           'f1': (625, 610), 'f2': (625, 500), 'f3': (625, 385), 'f4': (625, 275), 'f5': (625, 165),
           'f6': (625, 60)}
SIDE_6 = 102
BOARD_8 = {'a1': (65, 649), 'a2': (66, 563), 'a3': (67, 476), 'a4': (69, 392), 'a5': (70, 303),
           'a6': (71, 220),
           'a7': (72, 135), 'a8': (75, 50),
           'b1': (152, 649), 'b2': (152, 563), 'b3': (153, 476), 'b4': (155, 392), 'b5': (157, 303),
           'b6': (158, 220),
           'b7': (159, 135), 'b8': (159, 50),
           'c1': (238, 649), 'c2': (238, 563), 'c3': (238, 476), 'c4': (238, 392), 'c5': (240, 303),
           'c6': (240, 220),
           'c7': (240, 135), 'c8': (240, 50),
           'd1': (322, 649), 'd2': (322, 563), 'd3': (322, 476), 'd4': (323, 392), 'd5': (324, 303),
           'd6': (324, 220),
           'd7': (324, 135), 'd8': (324, 50),
           'e1': (404, 649), 'e2': (404, 563), 'e3': (405, 476), 'e4': (405, 392), 'e5': (407, 303),
           'e6': (407, 220),
           'e7': (408, 135), 'e8': (408, 50),
           'f1': (488, 649), 'f2': (488, 563), 'f3': (488, 476), 'f4': (488, 392), 'f5': (489, 303),
           'f6': (489, 220),
           'f7': (490, 135), 'f8': (490, 50),
           'g1': (573, 649), 'g2': (573, 563), 'g3': (573, 476), 'g4': (573, 392), 'g5': (574, 303),
           'g6': (574, 220),
           'g7': (574, 135), 'g8': (574, 50),
           'h1': (657, 649), 'h2': (657, 563), 'h3': (657, 476), 'h4': (657, 392), 'h5': (656, 303),
           'h6': (656, 220),
           'h7': (656, 135), 'h8': (656, 50)}
SIDE_8 = 80


def run_reversi_game(dpi: tuple = DEFAULT_DPI) -> None:
    """Call this function directly to start the reversi game window.
    This is the main thread of the game process.

    The default dpi is 800x800
    (please do not change the dpi since dpi adaptation is NOT implemented)
    """
    pygame.init()
    if not pygame.display.get_init():
        print('fail to load display')
        return
    game_surface = pygame.display.set_mode(dpi)
    while True:
        result = _main_menu(game_surface)
        if result == 1:
            while True:
                player = RandomPlayer()
                ai_num = _choose_ai_menu(game_surface)
                if ai_num == 1:
                    player = MobilityTreePlayer(3)
                elif ai_num == 2:
                    player = PositionalTreePlayer(3)
                elif ai_num == 3:
                    player = RandomPlayer()
                elif ai_num == 4:
                    player = MCTSTimeSavingPlayer(100, 8)
                elif ai_num == 5:
                    players = _choose_ai1(game_surface)
                    if players == ():
                        continue
                    else:
                        board_size = _choose_board_menu(game_surface)
                        if board_size == 6:
                            _run_ai_simulation(game_surface, 6, players[0], players[1])
                            break
                        elif board_size == 8:
                            _run_ai_simulation(game_surface, 8, players[0], players[1])
                            break
                        elif board_size == 0:
                            break

                elif ai_num == 0:
                    break
                board_size = _choose_board_menu(game_surface)
                if board_size == 6:
                    _run_ai_game(game_surface, 6, player)
                    break
                elif board_size == 8:
                    _run_ai_game(game_surface, 8, player)
                    break
                elif board_size == 0:
                    break
        else:
            pygame.quit()
            break
    return


def _main_menu(game_surface: pygame.Surface) -> int:
    background = pygame.image.load('assets/main_menu.png')
    game_surface.blit(background, (0, 0))

    start_button = pygame.image.load('assets/start_button.png')
    game_surface.blit(start_button, (250, 320))
    start_button_area = ((255, 250 + BUTTON_SIZE[0] - 5), (325, 320 + BUTTON_SIZE[1] - 5))
    # start_button_rect = pygame.Rect(255, 325, BUTTON_SIZE[0] - 5, BUTTON_SIZE[1] - 5)
    quit_button = pygame.image.load('assets/quit_button.png')
    game_surface.blit(quit_button, (250, 380))
    quit_button_area = ((255, 250 + BUTTON_SIZE[0] - 5), (385, 380 + BUTTON_SIZE[1] - 5))
    # quit_button_rect = pygame.Rect(255, 385, BUTTON_SIZE[0] - 5, BUTTON_SIZE[1] - 5)

    original_surface = game_surface.copy()
    button_down = pygame.image.load('assets/button_down.png')
    pygame.display.flip()

    while True:
        event = pygame.event.wait()
        # The code in this if check has problems yet to be found.
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            if start_button_area[0][0] <= mouse_pos[0] <= start_button_area[0][1] and \
                    start_button_area[1][0] <= mouse_pos[1] <= start_button_area[1][1]:
                game_surface.blit(button_down, (250, 320))
                pygame.display.flip()
                continue
            if quit_button_area[0][0] <= mouse_pos[0] <= quit_button_area[0][1] and \
                    quit_button_area[1][0] <= mouse_pos[1] <= quit_button_area[1][1]:
                game_surface.blit(button_down, (250, 380))
                pygame.display.flip()
                continue
            else:
                game_surface = original_surface
                pygame.display.flip()
                continue
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if start_button_area[0][0] <= mouse_pos[0] <= start_button_area[0][1] and \
                    start_button_area[1][0] <= mouse_pos[1] <= start_button_area[1][1]:
                return 1
            if quit_button_area[0][0] <= mouse_pos[0] <= quit_button_area[0][1] and \
                    quit_button_area[1][0] <= mouse_pos[1] <= quit_button_area[1][1]:
                pygame.quit()
                return -1
            else:
                continue
        elif event.type == pygame.QUIT:
            return -1


def _choose_ai_menu(game_surface: pygame.Surface) -> int:
    background = pygame.image.load('assets/choose_ai_menu.png')
    game_surface.blit(background, (0, 0))
    pygame.display.flip()
    while True:
        event = pygame.event.wait()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if 200 <= mouse_pos[0] <= 606:
                if 179 <= mouse_pos[1] <= 250:
                    return 1
                elif 282 <= mouse_pos[1] <= 345:
                    return 2
                elif 384 <= mouse_pos[1] <= 451:
                    return 3
                elif 490 <= mouse_pos[1] <= 553:
                    return 4
                elif 585 <= mouse_pos[1] <= 652:
                    return 5
                elif 683 <= mouse_pos[1] <= 750:
                    return 0
            else:
                continue
        elif event.type == pygame.QUIT:
            return -1


def _choose_ai_1and2(number: int, game_surface: pygame.Surface) -> int:
    if number == 1:
        file = 'assets/choose_ai_1.png'
    elif number == 2:
        file = 'assets/choose_ai_2.png'
    else:
        raise ValueError
    background = pygame.image.load(file)
    game_surface.blit(background, (0, 0))
    pygame.display.flip()
    while True:
        event = pygame.event.wait()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if 200 <= mouse_pos[0] <= 606:
                if 179 <= mouse_pos[1] <= 250:
                    return 1
                elif 282 <= mouse_pos[1] <= 345:
                    return 2
                elif 384 <= mouse_pos[1] <= 451:
                    return 3
                elif 490 <= mouse_pos[1] <= 553:
                    return 4
                elif 683 <= mouse_pos[1] <= 750:
                    return 0
            else:
                continue
        elif event.type == pygame.QUIT:
            return -1


def _choose_ai1(game_surface: pygame.surface) -> tuple:
    while True:
        player1 = RandomPlayer()
        ai_1 = _choose_ai_1and2(1, game_surface)
        if ai_1 == 0:
            return ()
        elif ai_1 == 1:
            player1 = MobilityTreePlayer(3)
        elif ai_1 == 2:
            player1 = PositionalTreePlayer(3)
        elif ai_1 == 3:
            player1 = RandomPlayer()
        elif ai_1 == 4:
            player1 = MCTSTimeSavingPlayer(100, 8)
        player2 = _choose_ai2(game_surface)
        if player2 is None:
            continue
        return (player1, player2)


def _choose_ai2(game_surface: pygame.surface) -> Optional[Union[MobilityTreePlayer,
                                                                PositionalTreePlayer, RandomPlayer,
                                                                ReversiGame, MCTSTimeSavingPlayer]]:
    while True:
        ai_2 = _choose_ai_1and2(2, game_surface)
        if ai_2 == 0:
            return None
        elif ai_2 == 1:
            return MobilityTreePlayer(3)
        elif ai_2 == 2:
            return PositionalTreePlayer(3)
        elif ai_2 == 3:
            return RandomPlayer()
        elif ai_2 == 4:
            return MCTSTimeSavingPlayer(100, 8)


def _choose_board_menu(game_surface: pygame.Surface) -> int:
    background = pygame.image.load('assets/choose_board_menu.png')
    game_surface.blit(background, (0, 0))
    pygame.display.flip()
    while True:
        event = pygame.event.wait()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if 200 <= mouse_pos[0] <= 606:
                if 188 <= mouse_pos[1] <= 255:
                    return 6
                elif 310 <= mouse_pos[1] <= 377:
                    return 8
                elif 435 <= mouse_pos[1] <= 500:
                    return 0
            else:
                continue
        elif event.type == pygame.QUIT:
            return -1


def _run_ai_game(game_surface: pygame.Surface, size: int,
                 ai_player: Union[MobilityTreePlayer, PositionalTreePlayer, RandomPlayer,
                                  ReversiGame, MCTSTimeSavingPlayer],
                 user_side: str = BLACK) -> None:
    if size == 8:
        background = pygame.image.load('assets/gameboard8.png')
    elif size == 6:
        background = pygame.image.load('assets/gameboard6.png')
    else:
        raise ValueError("invalid size.")
    game_surface.blit(background, (0, 0))
    pygame.display.flip()
    game = ReversiGame(size)
    previous_move = '*'
    if user_side == BLACK:
        ai_side: str = WHITE
    else:
        ai_side: str = BLACK
    board = game.get_game_board()
    _draw_game_state(game_surface, background, size, board)

    pass_move = pygame.image.load('assets/pass.png')

    while game.get_winner() is None:
        if (previous_move == '*' and user_side == WHITE) or game.get_current_player() == user_side:
            if game.get_valid_moves() == ['pass']:
                game.make_move('pass')
                previous_move = 'pass'

                surface = game_surface
                game_surface.blit(pass_move, (300, 300))
                pygame.display.flip()
                pygame.time.wait(1000)
                game_surface.blit(surface, (0, 0))
                pygame.display.flip()

                continue
            while True:
                event = pygame.event.wait()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if 585 <= mouse_pos[0] <= 795 and 10 <= mouse_pos[1] <= 41:
                        return
                    else:
                        move = _search_for_move(mouse_pos, size)
                        print(move)
                        if move == '' or move not in game.get_valid_moves():
                            continue
                        else:
                            previous_move = move
                            game.make_move(move)
                            board = game.get_game_board()
                            _draw_game_state(game_surface, background, size, board)
                            pygame.time.wait(1000)
                            break
                if event.type == pygame.QUIT:
                    return
        else:
            move = ai_player.make_move(game, previous_move)
            previous_move = move
            game.make_move(move)
            if move == 'pass':
                surface = game_surface
                game_surface.blit(pass_move, (300, 300))
                pygame.display.flip()
                pygame.time.wait(1000)
                game_surface.blit(surface, (0, 0))
                pygame.display.flip()
            else:
                board = game.get_game_board()
                _draw_game_state(game_surface, background, size, board)
    winner = game.get_winner()
    if winner == user_side:
        victory = pygame.image.load('assets/victory.png')
        game_surface.blit(victory, (300, 300))
        pygame.display.flip()
        pygame.time.wait(3000)
        return
    elif winner == ai_side:
        defeat = pygame.image.load('assets/defeat.png')
        game_surface.blit(defeat, (300, 300))
        pygame.display.flip()
        pygame.time.wait(3000)
        return
    else:
        draw = pygame.image.load('assets/draw.png')
        game_surface.blit(draw, (300, 300))
        pygame.display.flip()
        pygame.time.wait(3000)
        return


def _run_ai_simulation(game_surface: pygame.Surface, size: int,
                       player1: Union[MobilityTreePlayer, PositionalTreePlayer, RandomPlayer,
                                      ReversiGame, MCTSTimeSavingPlayer],
                       player2: Union[MobilityTreePlayer, PositionalTreePlayer, RandomPlayer,
                                      ReversiGame, MCTSTimeSavingPlayer]) -> None:
    if size == 8:
        background = pygame.image.load('assets/gameboard8.png')
    elif size == 6:
        background = pygame.image.load('assets/gameboard6.png')
    else:
        raise ValueError("invalid size.")
    game_surface.blit(background, (0, 0))
    pygame.display.flip()
    game = ReversiGame(size)
    previous_move = '*'
    board = game.get_game_board()
    _draw_game_state(game_surface, background, size, board)
    pass_move = pygame.image.load('assets/pass.png')
    player1_side = BLACK
    while game.get_winner() is None:
        if previous_move == '*' or game.get_current_player() == player1_side:
            move = player1.make_move(game, previous_move)
        else:
            move = player2.make_move(game, previous_move)
        previous_move = move
        game.make_move(move)
        if move == 'pass':
            surface = game_surface
            game_surface.blit(pass_move, (300, 300))
            pygame.display.flip()
            pygame.time.wait(500)
            game_surface.blit(surface, (0, 0))
            pygame.display.flip()
        else:
            board = game.get_game_board()
            _draw_game_state(game_surface, background, size, board)
        pygame.time.wait(500)
    winner = game.get_winner()
    if winner == BLACK:
        victory = pygame.image.load('assets/player1_victory.png')
        game_surface.blit(victory, (300, 300))
        pygame.display.flip()
        pygame.time.wait(3000)
        return
    elif winner == WHITE:
        defeat = pygame.image.load('assets/player2_victory.png')
        game_surface.blit(defeat, (300, 300))
        pygame.display.flip()
        pygame.time.wait(3000)
        return
    else:
        draw = pygame.image.load('assets/draw.png')
        game_surface.blit(draw, (300, 300))
        pygame.display.flip()
        pygame.time.wait(3000)
        return


def _search_for_move(mouse_pos: tuple, board_size: int) -> str:
    x = mouse_pos[0]
    y = mouse_pos[1]
    if board_size == 6:
        board = BOARD_6
    elif board_size == 8:
        board = BOARD_8
    else:
        raise ValueError
    for position in board:
        left = board[position][0]
        right = left + SIDE_6
        up = board[position][1]
        down = up + SIDE_6
        if left <= x <= right and up <= y <= down:
            return position
    return ''


def _draw_game_state(game_surface: pygame.Surface, background: pygame.Surface, size: int,
                     board: list) -> None:
    game_surface.blit(background, (0, 0))
    pygame.display.flip()
    black_chess6 = pygame.image.load('assets/chess/black6.png')
    black_chess8 = pygame.image.load('assets/chess/black8.png')
    white_chess6 = pygame.image.load('assets/chess/white6.png')
    white_chess8 = pygame.image.load('assets/chess/white8.png')
    for row_num in range(0, len(board)):
        for col_num in range(0, len(board)):
            if board[row_num][col_num] == BLACK:
                pos = INDEX_TO_COL[col_num] + INDEX_TO_ROW[row_num]
                if size == 6:
                    coordinates = (BOARD_6[pos][0] + SIDE_6 // 5, BOARD_6[pos][1] + SIDE_6 // 5)
                    game_surface.blit(black_chess6, coordinates)
                else:
                    coordinates = (BOARD_8[pos][0] + SIDE_8 // 6, BOARD_8[pos][1] + SIDE_8 // 6)
                    game_surface.blit(black_chess8, coordinates)
            elif board[row_num][col_num] == WHITE:
                pos = INDEX_TO_COL[col_num] + INDEX_TO_ROW[row_num]
                if size == 6:
                    coordinates = (BOARD_6[pos][0] + SIDE_6 // 5, BOARD_6[pos][1] + SIDE_6 // 5)
                    game_surface.blit(white_chess6, coordinates)
                else:
                    coordinates = (BOARD_8[pos][0] + SIDE_8 // 6, BOARD_8[pos][1] + SIDE_8 // 6)
                    game_surface.blit(white_chess8, coordinates)
    pygame.display.flip()
    return


if __name__ == "__main__":
    # Run this __main__ to see the game
    run_reversi_game()
