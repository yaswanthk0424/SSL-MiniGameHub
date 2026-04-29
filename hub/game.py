import pygame
import numpy as np
import sys
import os
import csv
import subprocess
import matplotlib.pyplot as plt
from datetime import date
from plotting import Plotting
class Game_Base:
    """
    Base class for the 2-player, turn-based board game.
    Winning_condition()  returns 0=ongoing, 1=P1 wins, 2=P2 wins, 3=draw
    Make_Move(*args)     returns True if the move was legal and applied
    Draw_Board(screen)   renders the board each frame
    Handle_Click(pos, screen) translate click to a move — returns True/False
    Board convention:  0 = empty | 1 = Player 1 | 2 = Player 2
    """
    def __init__(self, Player1, Player2, rows, cols):
        self.Player1     = Player1
        self.Player2     = Player2
        self.Player_Turn = 0                                   # 0=P1, 1=P2
        self.Player_List = [Player1, Player2]
        self.rows        = rows
        self.cols        = cols
        self.Game_Board  = np.zeros((rows, cols), dtype=int)   # NumPy board

    @property
    def Current_Player(self):
        # Name of the player who is currently playing
        return self.Player_List[self.Player_Turn]
    
    @property
    def Current_Player_Value(self):
        # Value to be placed inside the board
        return self.Player_Turn + 1

    def Player_Switch(self):
        # Switch player turns
        self.Player_Turn = 1 - self.Player_Turn

    def Reset_Board(self):
        # Reset board after every game
        self.Game_Board[:] = 0

    def Winning_condition(self):
        # Overridable — returns 0=ongoing, 1=P1, 2=P2, 3=draw
        return 0

    def Make_Move(self, *args):
        # Overridable — returns True if move was legal
        return False

    def Draw_Board(self, screen):
        # Overridable — render board each frame
        pass

    def Handle_Click(self, pos, screen):
        # Overridable — convert pixel click to a board move
        return False

    def Log_Game_Result(self, game_name: str, Winner, Loser, is_Draw):
        base_dir    = os.path.dirname(os.path.abspath(__file__))
        file_path   = os.path.join(base_dir, "history.csv")
        Draw_status = "Yes" if is_Draw else "No"
        today       = date.today().strftime("%d-%m-%Y")
        new_row     = [game_name, today, Winner, Loser, Draw_status]
        with open(file_path, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(new_row)

    def Leaderboard_Display(self, Sorting_Metric):
        base_dir  = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, "leaderboard.sh")

        Plotting()

        result = subprocess.run([
            "bash", file_path,
            str(self.Player1),
            str(self.Player2),
            str(Sorting_Metric)
        ])

        # Close all matplotlib windows after player picks R or Q
        plt.close("all")

        return result.returncode   # 0=restart, 2=quit


#Screen / layout constants
SCREEN_WT     = 1200
SCREEN_HT     = 900
TITLE_HT      = SCREEN_HT // 5     # "GameHub" banner
HEADER_HT     = SCREEN_HT // 8     # player names bar
BUTTON_WT     = SCREEN_WT // 3     # game button width
BUTTON_HT     = SCREEN_HT // 12    # game button height
BUTTON_RADIUS = 6

# Colours
BG           = (15,  25,  35)
TITLE_BG     = (30,  40,  60)
TITLE_FG     = (255, 255, 255)
HEADER_BG    = (22,  32,  48)
HEADER_FG    = (180, 210, 255)
BUTTON_BG    = (40,  60, 110)
BUTTON_HOVER = (60,  90, 160)
BUTTON_FG    = (255, 255, 255)
QUIT_BG      = (110,  30,  30)
QUIT_HOVER   = (160,  45,  45)


def make_fonts():
    return {
        "title"  : pygame.font.SysFont("lucidagrande", 52),
        "header" : pygame.font.SysFont("calibri",      28),
        "button" : pygame.font.SysFont("calibri",      32),
    }


def draw_banner(screen, font, text, center_y, width, height, bg, fg):
    rect = pygame.Rect(0, 0, width, height)
    rect.center = (SCREEN_WT // 2, center_y)
    pygame.draw.rect(screen, bg, rect)
    surf = font.render(text, True, fg)
    screen.blit(surf, surf.get_rect(center=rect.center))


def draw_button(screen, font, text, center_y, mouse):
    rect = pygame.Rect(0, 0, BUTTON_WT, BUTTON_HT)
    rect.center = (SCREEN_WT // 2, center_y)
    is_quit = (text == "QUIT")
    colour  = (QUIT_HOVER if is_quit else BUTTON_HOVER) if rect.collidepoint(mouse) \
              else (QUIT_BG if is_quit else BUTTON_BG)
    pygame.draw.rect(screen, colour, rect, border_radius=BUTTON_RADIUS)
    surf = font.render(text, True, BUTTON_FG)
    screen.blit(surf, surf.get_rect(center=rect.center))
    return rect


def load_games_csv(path="games.csv"):
    default_games = {
        "TicTacToe"    : "games/tictactoe.py",
        "Othello"      : "games/othello.py",
        "Connect Four" : "games/connect4.py",
    }
    if not os.path.exists(path):
        return default_games
    mapping = {}
    with open(path, newline="") as f:
        for row in csv.reader(f):
            if len(row) >= 2:
                name, script = row[0].strip(), row[1].strip()
                if name and script:
                    mapping[name] = script
    return mapping if mapping else default_games


def launch_game(script_path, player1, player2):
    abs_path = os.path.abspath(script_path)
    if not os.path.exists(abs_path):
        print(f"[game.py] Script not found: {abs_path}")
        return 1

    pygame.display.set_mode((1, 1), pygame.NOFRAME)
    pygame.event.pump()

    result = subprocess.run([sys.executable, abs_path, player1, player2])

    pygame.display.set_mode((SCREEN_WT, SCREEN_HT))
    pygame.display.set_caption("GameHub")
    pygame.event.pump()

    return result.returncode


def startmenu(screen, fonts, player1, player2, game_map):
    clock      = pygame.time.Clock()
    game_names = list(game_map.keys())
    running    = True

    while running:
        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                btn_y  = TITLE_HT + HEADER_HT
                for name in game_names:
                    btn_y += BUTTON_HT + 20
                    r = pygame.Rect(0, 0, BUTTON_WT, BUTTON_HT)
                    r.center = (SCREEN_WT // 2, btn_y)
                    if r.collidepoint(mx, my):
                        code = launch_game(game_map[name], player1, player2)
                        if code == 2:
                            running = False
                        break
                quit_y = btn_y + BUTTON_HT + 20
                quit_r = pygame.Rect(0, 0, BUTTON_WT, BUTTON_HT)
                quit_r.center = (SCREEN_WT // 2, quit_y)
                if quit_r.collidepoint(mx, my):
                    running = False

        screen = pygame.display.get_surface()
        screen.fill(BG)
        draw_banner(screen, fonts["title"], "GameHub",
                    TITLE_HT // 2, SCREEN_WT, TITLE_HT, TITLE_BG, TITLE_FG)
        draw_banner(screen, fonts["header"],
                    f"{player1}   vs   {player2}",
                    TITLE_HT + HEADER_HT // 2,
                    SCREEN_WT, HEADER_HT, HEADER_BG, HEADER_FG)
        btn_y = TITLE_HT + HEADER_HT
        for name in game_names:
            btn_y += BUTTON_HT + 20
            draw_button(screen, fonts["button"], name, btn_y, mouse)
        draw_button(screen, fonts["button"], "QUIT", btn_y + BUTTON_HT + 20, mouse)
        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python game.py <Player1> <Player2>")
        sys.exit(1)

    player1, player2 = sys.argv[1], sys.argv[2]
    game_map         = load_games_csv("games.csv")

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WT, SCREEN_HT))
    pygame.display.set_caption("GameHub")
    fonts  = make_fonts()

    startmenu(screen, fonts, player1, player2, game_map)
    pygame.quit()
    sys.exit()