import pygame
import sys
import numpy as np
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from game import Game_Base

# ================= CONSTANTS =================
ROWS, COLS = 10, 10
SCREEN_WT, SCREEN_HT = 600, 600
CELL_SIZE = SCREEN_WT // COLS

# COLORS 
BG_COLOR   = (20, 20, 30)
LINE_COLOR = (70, 80, 110)

P1_COLOR = (255, 120, 120)
P2_COLOR = (120, 180, 255)

BUTTON_WT = SCREEN_WT // 3
BUTTON_HT = SCREEN_HT // 12


# === GAME CLASS ===
class TicTacToe(Game_Base):

    def Make_move(self, row, col):
        if self.Game_Board[row, col] == 0:
            self.Game_Board[row, col] = self.Current_Player_Value
            return True
        return False

    def Draw_Board(self, screen):
        screen.fill(BG_COLOR)

        # grid
        for i in range(ROWS):
            pygame.draw.line(screen, LINE_COLOR,
                             (0, i * CELL_SIZE),
                             (SCREEN_WT, i * CELL_SIZE), 2)

        for j in range(COLS):
            pygame.draw.line(screen, LINE_COLOR,
                             (j * CELL_SIZE, 0),
                             (j * CELL_SIZE, SCREEN_HT), 2)

        # X and O
        for r in range(ROWS):
            for c in range(COLS):
                if self.Game_Board[r, c] == 1:
                    pygame.draw.line(screen, P1_COLOR,
                                     (c*CELL_SIZE+15, r*CELL_SIZE+15),
                                     ((c+1)*CELL_SIZE-15, (r+1)*CELL_SIZE-15), 3)
                    pygame.draw.line(screen, P1_COLOR,
                                     ((c+1)*CELL_SIZE-15, r*CELL_SIZE+15),
                                     (c*CELL_SIZE+15, (r+1)*CELL_SIZE-15), 3)

                elif self.Game_Board[r, c] == 2:
                    pygame.draw.circle(screen, P2_COLOR,
                                       (c*CELL_SIZE + CELL_SIZE//2,
                                        r*CELL_SIZE + CELL_SIZE//2),
                                       CELL_SIZE//3, 3)

    def Handle_Click(self, pos, screen):
        x, y = pos
        row = y // CELL_SIZE
        col = x // CELL_SIZE
        if col < COLS:
            return self.Make_move(row, col)
        return False

    def Winning_condition(self):
        b = (self.Game_Board == self.Current_Player_Value)

        if np.any(b[:, :-4] & b[:, 1:-3] & b[:, 2:-2] & b[:, 3:-1] & b[:, 4:]):
            return self.Current_Player_Value

        elif np.any(b[:-4, :] & b[1:-3, :] & b[2:-2, :] & b[3:-1, :] & b[4:, :]):
            return self.Current_Player_Value

        elif np.any(b[:-4, :-4] & b[1:-3, 1:-3] & b[2:-2, 2:-2] & b[3:-1, 3:-1] & b[4:, 4:]):
            return self.Current_Player_Value

        elif np.any(b[4:, :-4] & b[3:-1, 1:-3] & b[2:-2, 2:-2] & b[1:-3, 3:-1] & b[:-4, 4:]):
            return self.Current_Player_Value

        elif not np.any(self.Game_Board == 0):
            return 3

        return 0


def draw_gameover(screen, text):
    overlay = pygame.Surface((SCREEN_WT, SCREEN_HT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))
    screen.blit(overlay, (0, 0))

    font_big = pygame.font.SysFont(None, 70)
    font_mid = pygame.font.SysFont(None, 40)

    title = font_big.render("GAME OVER", True, (255, 220, 120))
    screen.blit(title, title.get_rect(center=(SCREEN_WT//2, 180)))

    result = font_mid.render(text, True, (255, 255, 255))
    screen.blit(result, result.get_rect(center=(SCREEN_WT//2, 250)))


def draw_button(screen, text, y, mouse, color):
    rect = pygame.Rect(0, 0, BUTTON_WT, BUTTON_HT)
    rect.center = (SCREEN_WT // 2, y)

    # hover
    if rect.collidepoint(mouse):
        color = tuple(c-40 for c in color)

    # shadow
    shadow = rect.copy()
    shadow.y += 5
    pygame.draw.rect(screen, (0, 0, 0), shadow, border_radius=10)

    pygame.draw.rect(screen, color, rect, border_radius=10)

    font = pygame.font.SysFont("calibri", 30)
    surf = font.render(text, True, (255, 255, 255))
    screen.blit(surf, surf.get_rect(center=rect.center))

    return rect


# ================= MAIN =================
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WT, SCREEN_HT))
    clock = pygame.time.Clock()

    p1 = sys.argv[1]
    p2 = sys.argv[2]

    game = TicTacToe(p1, p2, ROWS, COLS)

    game_over = False
    running = True
    is_draw = False
    count = 1

    
    restart_btn = None
    leader_btn = None
    back_btn = None

    while running:
        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:

                # GAME PLAY
                if not game_over:
                    if game.Handle_Click(event.pos, screen):
                        result = game.Winning_condition()
                        if result != 0:
                            game_over = True
                        else:
                            game.Player_Switch()

                # GAME OVER BUTTONS
                else:
                    if restart_btn and restart_btn.collidepoint(event.pos):
                        game.Reset_Board()
                        game_over = False
                        count = 1
                        is_draw = False

                    elif back_btn and back_btn.collidepoint(event.pos):
                        running = False

                    elif leader_btn and leader_btn.collidepoint(event.pos):
                        import subprocess
                        print("Running leaderboard...")

                        subprocess.run(["bash", "../hub/leaderboard.sh"], check=True)
        # Draw Board
        game.Draw_Board(screen)

        # Game Over Interface
        if game_over:
            result = game.Winning_condition()

            if result == 1:
                text = f"{p1} Wins!"
                winner, loser = p1, p2
                is_draw = False

            elif result == 2:
                text = f"{p2} Wins!"
                winner, loser = p2, p1
                is_draw = False

            else:
                text = "Draw"
                winner, loser = None, None
                is_draw = True

            draw_gameover(screen, text)

            # saving in history.csv 
            if count == 1:
                game.Log_Game_Result("TicTacToe", winner, loser, is_draw)
                count = 0

            restart_btn = draw_button(screen, "Restart", 320, mouse, (80, 200, 120))
            leader_btn  = draw_button(screen, "Leaderboard", 400, mouse, (90, 140, 255))
            back_btn    = draw_button(screen, "Back", 480, mouse, (180, 80, 200))

        pygame.display.update()
        clock.tick(60)

    pygame.quit()
    sys.exit()
