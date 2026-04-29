import pygame
import sys
import numpy as np
import os
import subprocess
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from game import Game_Base

ROWS, COLS = 10, 10
SCREEN_WT, SCREEN_HT = 980, 640
TOP_GAP = 105

SIDE_GAPS = 250
CELL_SIZE = (SCREEN_WT - 2 * SIDE_GAPS) // COLS
BOTTOM_GAP = SCREEN_HT - ROWS * CELL_SIZE - TOP_GAP

BG_COLOR   = (18, 18, 28)
GRID_COLOR = (60, 70, 90)

P1_COLOR = (255, 90, 90)      # X
P2_COLOR = (80, 170, 255)     # O

TEXT_COLOR = (230, 230, 240)
ACCENT_COLOR = (255, 215, 120)
BUTTON_WT = SCREEN_WT // 3
BUTTON_HT = SCREEN_HT // 12

def draw_turn_indicator(screen, current_player, p1, p2):#Drawing Turn Indicator
    font_big = pygame.font.SysFont("calibri", 80, bold=True)
    font_small = pygame.font.SysFont("calibri", 36, bold=True)

    if current_player == 1:
        # Player 1 → X on RIGHT
        text = font_big.render("X", True, P1_COLOR)
        name = font_small.render(f"{p1}'s Turn", True, TEXT_COLOR)

        screen.blit(name, name.get_rect(center=(SCREEN_WT // 2, 40)))
        screen.blit(text, text.get_rect(center=(SCREEN_WT - 80, SCREEN_HT // 2)))

    else:
        # Player 2 → O on LEFT
        text = font_big.render("O", True, P2_COLOR)
        name = font_small.render(f"{p2}'s Turn", True, TEXT_COLOR)

        screen.blit(name, name.get_rect(center=(SCREEN_WT // 2, 40)))
        screen.blit(text, text.get_rect(center=(80, SCREEN_HT // 2)))



class TicTacToe(Game_Base):
    def __init__(self, p1, p2, rows, cols):
        super().__init__(p1, p2, rows, cols)
        self.winning_coords = None

    def Make_Move(self, row, col):
        if self.Game_Board[row, col] == 0:
            self.Game_Board[row, col] = self.Current_Player_Value
            return True
        return False

    def Draw_Board(self, screen):
        screen.fill(BG_COLOR)

        # GRID
        for i in range(ROWS + 1):
            pygame.draw.line(screen, GRID_COLOR,
                             (SIDE_GAPS, TOP_GAP + i * CELL_SIZE),
                             (SCREEN_WT - SIDE_GAPS, TOP_GAP + i * CELL_SIZE), 2)

        for j in range(COLS + 1):
            pygame.draw.line(screen, GRID_COLOR,
                             (SIDE_GAPS + j * CELL_SIZE, TOP_GAP),
                             (SIDE_GAPS + j * CELL_SIZE, SCREEN_HT - BOTTOM_GAP), 2)

        # SYMBOLS
        for r in range(ROWS):
            for c in range(COLS):
                start_x = SIDE_GAPS + c * CELL_SIZE
                start_y = TOP_GAP + r * CELL_SIZE

                if self.Game_Board[r, c] == 1:
                    pygame.draw.line(screen, P1_COLOR,
                                     (start_x + 12, start_y + 12),
                                     (start_x + CELL_SIZE - 12, start_y + CELL_SIZE - 12), 4)
                    pygame.draw.line(screen, P1_COLOR,
                                     (start_x + CELL_SIZE - 12, start_y + 12),
                                     (start_x + 12, start_y + CELL_SIZE - 12), 4)

                elif self.Game_Board[r, c] == 2:
                    pygame.draw.circle(screen, P2_COLOR,
                                       (start_x + CELL_SIZE // 2,
                                        start_y + CELL_SIZE // 2),
                                       CELL_SIZE // 3, 4)

        # WINNING LINE
        if getattr(self, 'winning_coords', None):
            (r1, c1), (r2, c2) = self.winning_coords
            start_x = SIDE_GAPS + c1 * CELL_SIZE + CELL_SIZE // 2
            start_y = TOP_GAP + r1 * CELL_SIZE + CELL_SIZE // 2
            end_x = SIDE_GAPS + c2 * CELL_SIZE + CELL_SIZE // 2
            end_y = TOP_GAP + r2 * CELL_SIZE + CELL_SIZE // 2
            # Draw a thick accent line connecting the 5 winning symbols
            pygame.draw.line(screen, ACCENT_COLOR, (start_x, start_y), (end_x, end_y), 8)

        # TURN INDICATOR
        draw_turn_indicator(screen, self.Current_Player_Value, self.Player1, self.Player2)

    def Handle_Click(self, pos, screen):
        x, y = pos
        if (x < SIDE_GAPS or x > SCREEN_WT - SIDE_GAPS or
            y < TOP_GAP or y > SCREEN_HT - BOTTOM_GAP):
            return False

        row = (y - TOP_GAP) // CELL_SIZE
        column = (x - SIDE_GAPS) // CELL_SIZE
        return self.Make_Move(row, column)

    def Winning_condition(self):
        b = (self.Game_Board == self.Current_Player_Value)

        # Horizontal
        mask = b[:, :-4] & b[:, 1:-3] & b[:, 2:-2] & b[:, 3:-1] & b[:, 4:]
        if np.any(mask):
            r, c = np.where(mask)
            self.winning_coords = ((r[0], c[0]), (r[0], c[0] + 4))
            return self.Current_Player_Value

        # Vertical
        mask = b[:-4, :] & b[1:-3, :] & b[2:-2, :] & b[3:-1, :] & b[4:, :]
        if np.any(mask):
            r, c = np.where(mask)
            self.winning_coords = ((r[0], c[0]), (r[0] + 4, c[0]))
            return self.Current_Player_Value

        # Diagonal \
        mask = b[:-4, :-4] & b[1:-3, 1:-3] & b[2:-2, 2:-2] & b[3:-1, 3:-1] & b[4:, 4:]
        if np.any(mask):
            r, c = np.where(mask)
            self.winning_coords = ((r[0], c[0]), (r[0] + 4, c[0] + 4))
            return self.Current_Player_Value
        # Diagonal /
        mask = b[4:, :-4] & b[3:-1, 1:-3] & b[2:-2, 2:-2] & b[1:-3, 3:-1] & b[:-4, 4:]
        if np.any(mask):
            r, c = np.where(mask)
            self.winning_coords = ((r[0] + 4, c[0]), (r[0], c[0] + 4))
            return self.Current_Player_Value
        if not np.any(self.Game_Board == 0):
            return 3
        return 0
def draw_gameover(screen, text):
    overlay = pygame.Surface((SCREEN_WT, SCREEN_HT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))
    screen.blit(overlay, (0, 0))
    font_big = pygame.font.SysFont(None, 70)
    font_mid = pygame.font.SysFont(None, 40)
    title = font_big.render("GAME OVER", True, ACCENT_COLOR)
    screen.blit(title, title.get_rect(center=(SCREEN_WT // 2, 150)))
    result = font_mid.render(text, True, TEXT_COLOR)
    screen.blit(result, result.get_rect(center=(SCREEN_WT // 2, 220)))
    sortMetric = font_mid.render("Select the sorting metric", True, TEXT_COLOR)
    screen.blit(sortMetric, sortMetric.get_rect(center=(SCREEN_WT // 2, 290)))
def draw_button(screen, text, y, mouse, color):
    rect = pygame.Rect(0, 0, BUTTON_WT, BUTTON_HT)
    rect.center = (SCREEN_WT // 2, y)
    if rect.collidepoint(mouse):
        color = tuple(max(0, c - 40) for c in color)
    shadow = rect.copy()
    shadow.y += 5
    pygame.draw.rect(screen, (0, 0, 0), shadow, border_radius=10)
    pygame.draw.rect(screen, color, rect, border_radius=10)
    font = pygame.font.SysFont("calibri", 30)
    surf = font.render(text, True, (255, 255, 255))
    screen.blit(surf, surf.get_rect(center=rect.center))
    return rect
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
    win_time = 0
    wins_btn = None
    win_pct_btn = None
    worlRatio_btn = None
    while running:
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not game_over:
                    if game.Handle_Click(event.pos, screen):
                        result = game.Winning_condition()
                        if result != 0:
                            game_over = True
                            win_time = pygame.time.get_ticks() # Record the time of the win
                        else:
                            game.Player_Switch()
                else:
                    # Only accept button clicks if the 2-second wait is over
                    if pygame.time.get_ticks() - win_time > 2000:
                        if wins_btn and wins_btn.collidepoint(event.pos):
                            code = game.Leaderboard_Display("wins")
                            sys.exit(code)
                        elif win_pct_btn and win_pct_btn.collidepoint(event.pos):
                            code = game.Leaderboard_Display("win_pct")
                            sys.exit(code)
                        elif worlRatio_btn and worlRatio_btn.collidepoint(event.pos):
                            code = game.Leaderboard_Display("worlRatio")
                            sys.exit(code)
        game.Draw_Board(screen)
        if game_over:
            # Wait 2 seconds before showing the GAME OVER overlay
            if pygame.time.get_ticks() - win_time > 2000:
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
                if count == 1:
                    game.Log_Game_Result("TicTacToe", winner, loser, is_draw)
                    count = 0
                wins_btn = draw_button(screen, "Wins", 360, mouse, (46, 204, 113))
                win_pct_btn = draw_button(screen, "Win_pct", 440, mouse, (52, 152, 219))
                worlRatio_btn = draw_button(screen, "Win/Loss", 520, mouse, (155, 89, 182))
        pygame.display.update()
        clock.tick(60)
    pygame.quit()
    sys.exit()