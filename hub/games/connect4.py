import pygame
import sys,os
import numpy as np
import csv
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from game import Game_Base

#Colour constants
BG_COlOUR     = (0,  0,  0)
DISC_COLOUR_1 = (226, 32,  32)
DISC_COLOUR_2 = (255,215,   0)
ROWS = 7
COLS = 7

#Screen constants
SCREEN_WT, SCREEN_HT = 700, 800
BUTTON_WT    = SCREEN_WT // 3          
BUTTON_HT    = SCREEN_HT // 12
LEADER_BTN_WT = int(SCREEN_WT * 0.55)  

BTN_BG     = (40,  60, 110)
BTN_HOVER  = (60,  90, 160)
BTN_FG     = (255, 255, 255)
BTN_RADIUS = 6


class Connect_4(Game_Base):
    def __init__(self, player1, player2):
        super().__init__(player1, player2, ROWS, COLS)
        self.winning_coords = None  # To store the start and end coordinates of the winning line

    def Winning_condition(self):
        boolean_mask = (self.Game_Board == self.Current_Player_Value)
        
        # Check Vertical (Varying second index)
        mask = boolean_mask[:,:-3] & boolean_mask[:,1:-2] & boolean_mask[:,2:-1] & boolean_mask[:,3:]
        if np.any(mask):
            r, c = np.where(mask)
            self.winning_coords = ((r[0], c[0]), (r[0], c[0] + 3))
            return self.Current_Player_Value
            
        # Check Horizontal (Varying first index)
        mask = boolean_mask[:-3,:] & boolean_mask[1:-2,:] & boolean_mask[2:-1,:] & boolean_mask[3:,:]
        if np.any(mask):
            r, c = np.where(mask)
            self.winning_coords = ((r[0], c[0]), (r[0] + 3, c[0]))
            return self.Current_Player_Value
            
        # Check Diagonal \ 
        mask = boolean_mask[:-3,:-3] & boolean_mask[1:-2,1:-2] & boolean_mask[2:-1,2:-1] & boolean_mask[3:,3:]
        if np.any(mask):
            r, c = np.where(mask)
            self.winning_coords = ((r[0], c[0]), (r[0] + 3, c[0] + 3))
            return self.Current_Player_Value
            
        # Check Diagonal /
        mask = boolean_mask[3:,:-3] & boolean_mask[2:-1,1:-2] & boolean_mask[1:-2,2:-1] & boolean_mask[:-3,3:]
        if np.any(mask):
            r, c = np.where(mask)
            self.winning_coords = ((r[0] + 3, c[0]), (r[0], c[0] + 3))
            return self.Current_Player_Value
            
        # Check Draw
        if not np.any(self.Game_Board == 0):
            return 3
            
        return 0

    def Make_Move(self, row, col):
        column_data = self.Game_Board[row, :]
        empty_rows  = np.where(column_data == 0)[0]
        if empty_rows.size > 0:
            self.Game_Board[row, empty_rows[-1]] = self.Current_Player_Value
            if self.Winning_condition() == 0:
                self.Player_Switch()
            return True
        return False

    def Draw_Board(self, screen):
        Board_Surface = pygame.image.load('./Images/Connect4/board_new.png').convert_alpha()
        # Shifted board center down by 50px
        Board_rect    = Board_Surface.get_rect(center=(350, 450))
        screen.blit(Board_Surface, Board_rect)
        p1_rows, p1_cols = np.where(self.Game_Board == 1)
        p2_rows, p2_cols = np.where(self.Game_Board == 2)
        
        # Shifted circle coordinates down by 50px (50 -> 100)
        for row, col in zip(p1_rows, p1_cols):
            pygame.draw.circle(screen, DISC_COLOUR_1, (100*row+48, 100+100*col+48), 40)
        for row, col in zip(p2_rows, p2_cols):
            pygame.draw.circle(screen, DISC_COLOUR_2, (100*row+48, 100+100*col+48), 40)
            
        # Draw the winning line if coordinates are set
        if self.winning_coords:
            (r1, c1), (r2, c2) = self.winning_coords
            start_pos = (100*r1+48, 100+100*c1+48)
            end_pos   = (100*r2+48, 100+100*c2+48)
            # Drawing a crisp BLACK line over the winning discs
            pygame.draw.line(screen, (0, 0, 0), start_pos, end_pos, 10)

    def Handle_Click(self, pos, screen):
        x, y = pos
        row  = x // 100
        col  = y // 100
        if col < self.cols:
            return self.Make_Move(row, col)
        return False


def draw_hub_button(screen, text, center_y, mouse, width=BUTTON_WT):
    font = pygame.font.SysFont("calibri", 32)
    rect = pygame.Rect(0, 0, width, BUTTON_HT)
    rect.center = (SCREEN_WT // 2, center_y)
    color = BTN_HOVER if rect.collidepoint(mouse) else BTN_BG
    pygame.draw.rect(screen, color, rect, border_radius=BTN_RADIUS)
    surf = font.render(text, True, BTN_FG)
    screen.blit(surf, surf.get_rect(center=rect.center))
    return rect


def show_metric_screen(screen, clock):
    font_title = pygame.font.SysFont("calibri", 42)
    font       = pygame.font.SysFont("calibri", 32)
    metrics = {
        "Wins"      : "Wins",
        "Win %"     : "Win_pct",
        "W/L Ratio" : "WL_Ratio",
    }
    labels = list(metrics.keys())
    while True:
        mouse = pygame.mouse.get_pos()
        screen.fill(BG_COlOUR)
        title = font_title.render("Sort Leaderboard By", True, (255, 220, 120))
        screen.blit(title, title.get_rect(center=(SCREEN_WT // 2, 120)))
        btn_rects = {}
        for i, label in enumerate(labels):
            rect = pygame.Rect(0, 0, BUTTON_WT, BUTTON_HT)
            rect.center = (SCREEN_WT // 2, 250 + i * (BUTTON_HT + 20))
            color = BTN_HOVER if rect.collidepoint(mouse) else BTN_BG
            pygame.draw.rect(screen, color, rect, border_radius=BTN_RADIUS)
            surf = font.render(label, True, BTN_FG)
            screen.blit(surf, surf.get_rect(center=rect.center))
            btn_rects[label] = rect
        pygame.display.update()
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(2)
            if event.type == pygame.MOUSEBUTTONDOWN:
                for label, rect in btn_rects.items():
                    if rect.collidepoint(event.pos):
                        return metrics[label]


def draw_gameover(screen, text, player1, player2):
    # Strong overlay so board barely shows through
    overlay = pygame.Surface((SCREEN_WT, SCREEN_HT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))

    font_title  = pygame.font.SysFont("lucidagrande", 64)
    font_winner = pygame.font.SysFont("calibri",      48)
    font_sub    = pygame.font.SysFont("calibri",      28)

    # "GAME OVER"
    title = font_title.render("GAME OVER", True, (255, 220, 120))
    screen.blit(title, title.get_rect(center=(SCREEN_WT//2, 160)))

    # Divider line
    pygame.draw.line(screen, (80, 100, 160),
                     (SCREEN_WT//2 - 180, 205),
                     (SCREEN_WT//2 + 180, 205), 2)


    if "Draw" in text:
        color = (180, 180, 255)
    elif player1 in text:
        color = (226, 32,  32)  # P1 Red
    else:
        color = (255,215,   0)   # P2 Yellow

    winner_surf = font_winner.render(text, True, color)
    screen.blit(winner_surf, winner_surf.get_rect(center=(SCREEN_WT//2, 265)))



def run(player1, player2):
    pygame.init()
    Game = Connect_4(player1, player2)
    screen = pygame.display.set_mode((SCREEN_WT, SCREEN_HT))
    pygame.display.set_caption("Connect Four")
    red_arrow_surface = pygame.image.load('./Images/Connect4/red_arrow.png').convert_alpha()
    yellow_arrow_surface = pygame.image.load('./Images/Connect4/yellow_arrow.png').convert_alpha()
    arrow_surface = [red_arrow_surface, yellow_arrow_surface]
    clock = pygame.time.Clock()
    running = True
    game_over = False
    winner = None
    count       = 1
    leader_btn  = None
    win_time    = 0 # Initialize timer tracker

    while running: 
        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not game_over:
                    Game.Handle_Click(event.pos, screen)
                    result = Game.Winning_condition()
                    if result != 0:
                        winner    = result
                        game_over = True
                        win_time  = pygame.time.get_ticks() # Record the exact time of win
                else:
                    if leader_btn and leader_btn.collidepoint(event.pos):
                        metric = show_metric_screen(screen, clock)
                        pygame.quit()
                        code = Game.Leaderboard_Display(metric)
                        sys.exit(code)   # 0=back to hub, 2=quit

        screen.fill(BG_COlOUR)
        
        # --- Draw Turn Indicator ---
        font_turn = pygame.font.SysFont("calibri", 40, bold=True)
        if Game.Current_Player_Value == 1:
            turn_text = f"{player1}'s Turn"
            color = DISC_COLOUR_1
        else:
            turn_text = f"{player2}'s Turn"
            color = DISC_COLOUR_2
            
        turn_surf = font_turn.render(turn_text, True, color)
        screen.blit(turn_surf, turn_surf.get_rect(center=(SCREEN_WT//2, 30)))
        
        # --- Draw Board ---
        Game.Draw_Board(screen)

        if not game_over:
            column_no  = mouse[0] // 100
            # Shifted arrow down to avoid overlapping the new turn text
            arrow_rect = arrow_surface[1 - Game.Current_Player_Value].get_rect(
                center=(49 + column_no * 100, 80)) 
            screen.blit(arrow_surface[1 - Game.Current_Player_Value], arrow_rect)
        else:
            # Check if 2 seconds (2000 milliseconds) have passed since win
            if pygame.time.get_ticks() - win_time > 2000:
                if winner == 3:
                    text = "It's a Draw!"
                    w_name, l_name, is_draw = player1, player2, True
                elif winner == 1:
                    text = f"{player1} Wins!"
                    w_name, l_name, is_draw = player1, player2, False
                else:
                    text = f"{player2} Wins!"
                    w_name, l_name, is_draw = player2, player1, False

                if count == 1:
                    Game.Log_Game_Result("Connect4", w_name, l_name, is_draw)
                    count = 0

                draw_gameover(screen, text, player1, player2)
                leader_btn = draw_hub_button(
                    screen, "View Leaderboard", 450, mouse, width=LEADER_BTN_WT)

        pygame.display.update()
        clock.tick(60)
    pygame.quit()
    sys.exit(1)
if __name__ == "__main__":
    Player1 = sys.argv[1]
    Player2 = sys.argv[2]
    run(Player1, Player2)