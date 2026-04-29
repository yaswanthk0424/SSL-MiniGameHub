import pygame
import sys,os
import numpy as np
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from game import Game_Base

DISC_COLOUR_1 = (0,0,0)
DISC_COLOUR_2 = (255,255,255)
ROWS = 8
COLS = 8 

SIDE_PANEL_WT = 200 
SCREEN_WT = 800 + 2 * SIDE_PANEL_WT  # 1200 total width
SCREEN_HT = 800

BUTTON_WT    = SCREEN_WT // 3         
BUTTON_HT    = SCREEN_HT // 12
LEADER_BTN_WT = int(SCREEN_WT * 0.55) 

BTN_BG     = (40,  60, 110)
BTN_HOVER  = (60,  90, 160)
BTN_FG     = (255, 255, 255)
BTN_RADIUS = 6

#(row,col) direction changes
DIRECTIONS = [(-1,-1),(-1,0),(-1,1),
              (0,-1),        (0,1),
              (1,-1), (1,0), (1,1)]

class Othello(Game_Base):
    def __init__(self,Player1,Player2):
        super().__init__(Player1,Player2,ROWS,COLS)
        self.Player1_Name = Player1
        self.Player2_Name = Player2
        self.Board_surface = pygame.image.load('./Images/Othello/Othello_board.png').convert_alpha()
        # Centering board according to the new expanded screen width
        self.Board_rect = self.Board_surface.get_rect(center = (SCREEN_WT//2,400))
        self._setup_board()

    def _setup_board(self):
        self.Game_Board[3,3] = 1
        self.Game_Board[3,4] = 2
        self.Game_Board[4,4] = 1
        self.Game_Board[4,3] = 2

    def get_flips(self,row,col,player):
        if self.Game_Board[row,col] != 0:
            return []
        opponent = 3 - player
        all_flips = []
        for dr,dc in DIRECTIONS:
            line = []
            r , c = row + dr , col + dc
            while 0 <= r < ROWS and  0 <= c < COLS and  self.Game_Board[r,c] == opponent:
                line.append((r,c))
                r += dr
                c += dc
            if line and 0 <= r < ROWS and 0 <= c < COLS and self.Game_Board[r,c] == player:
                all_flips.extend(line)
        return all_flips

    def valid_move(self,row,col,player):
        return len(self.get_flips(row,col,player)) > 0

    def get_all_valid_moves(self,player):
        moves = []
        empty_cells = np.argwhere(self.Game_Board == 0)
        for r,c in empty_cells:
            if self.valid_move(r,c,player):
                moves.append((r,c))
        return moves

    def Make_Move(self,row,col):
        flips = self.get_flips(row,col,self.Current_Player_Value)
        if not flips:
            return False
        self.Game_Board[row,col] = self.Current_Player_Value
        flip_rows = np.array([r for r,c in flips ])
        flip_cols = np.array([c for r,c in flips])
        self.Game_Board[flip_rows,flip_cols] = self.Current_Player_Value
        return True

    def Winning_condition(self):
        Player1_discs = np.count_nonzero(self.Game_Board == 1)
        Player2_discs = np.count_nonzero(self.Game_Board == 2)
        if Player1_discs > Player2_discs :return 1
        elif Player2_discs > Player1_discs :return 2
        else: return 3

    def Draw_Side_Panels(self, screen):
        font_title = pygame.font.SysFont("calibri", 36, bold=True)
        font_info = pygame.font.SysFont("calibri", 28)
        
        p1_discs = np.count_nonzero(self.Game_Board == 1)
        p2_discs = np.count_nonzero(self.Game_Board == 2)
        

        pygame.draw.rect(screen, (20, 20, 20), (0, 0, SIDE_PANEL_WT, SCREEN_HT))
        pygame.draw.line(screen, (100, 100, 100), (SIDE_PANEL_WT, 0), (SIDE_PANEL_WT, SCREEN_HT), 2)
        
        right_x = SCREEN_WT - SIDE_PANEL_WT
        pygame.draw.rect(screen, (20, 20, 20), (right_x, 0, SIDE_PANEL_WT, SCREEN_HT))
        pygame.draw.line(screen, (100, 100, 100), (right_x, 0), (right_x, SCREEN_HT), 2)
        

        if self.Current_Player_Value == 1:
            pygame.draw.rect(screen, (0, 200, 0), (0, 0, SIDE_PANEL_WT, SCREEN_HT), 4)
        elif self.Current_Player_Value == 2:
            pygame.draw.rect(screen, (0, 200, 0), (right_x, 0, SIDE_PANEL_WT, SCREEN_HT), 4)
            
        # Left Side: Player 1 (Black)
        cx1 = SIDE_PANEL_WT // 2
        name1 = font_title.render(self.Player1_Name, True, (255, 255, 255))
        screen.blit(name1, name1.get_rect(center=(cx1, 150)))
        
        pygame.draw.circle(screen, DISC_COLOUR_1, (cx1, 250), 40)
        pygame.draw.circle(screen, (150, 150, 150), (cx1, 250), 42, 2) 
        
        count1 = font_info.render(f"Discs: {p1_discs}", True, (255, 255, 255))
        screen.blit(count1, count1.get_rect(center=(cx1, 350)))
        
        if self.Current_Player_Value == 1:

            turn1 = font_info.render(f"{self.Player1_Name}'s TURN", True, (0, 255, 0))
            screen.blit(turn1, turn1.get_rect(center=(cx1, 450)))
            
        cx2 = right_x + SIDE_PANEL_WT // 2
        name2 = font_title.render(self.Player2_Name, True, (255, 255, 255))
        screen.blit(name2, name2.get_rect(center=(cx2, 150)))
        
        pygame.draw.circle(screen, DISC_COLOUR_2, (cx2, 250), 40)
        pygame.draw.circle(screen, (150, 150, 150), (cx2, 250), 42, 2)
        
        count2 = font_info.render(f"Discs: {p2_discs}", True, (255, 255, 255))
        screen.blit(count2, count2.get_rect(center=(cx2, 350)))
        
        if self.Current_Player_Value == 2:

            turn2 = font_info.render(f"{self.Player2_Name}'s TURN", True, (0, 255, 0))
            screen.blit(turn2, turn2.get_rect(center=(cx2, 450)))

    def Draw_Board(self, screen):
        screen.blit(self.Board_surface,self.Board_rect)
        p1_rows,p1_cols = np.where(self.Game_Board == 1)
        p2_rows,p2_cols = np.where(self.Game_Board == 2)
        
        for row ,col in zip(p1_rows,p1_cols):
            x_pos = 100*col + 50 + SIDE_PANEL_WT 
            y_pos = 100*row + 50
            pygame.draw.circle(screen,DISC_COLOUR_1,(x_pos,y_pos),48)
            
        for row ,col in zip(p2_rows,p2_cols):
            x_pos = 100*col + 50 + SIDE_PANEL_WT
            y_pos = 100*row + 50
            pygame.draw.circle(screen,DISC_COLOUR_2,(x_pos,y_pos),48)  
            
        for r,c in self.get_all_valid_moves(self.Current_Player_Value):
            x_pos = 100*c + 50 + SIDE_PANEL_WT
            y_pos = 100*r + 50
            if self.Current_Player_Value==1:
                pygame.draw.circle(screen,DISC_COLOUR_1,(x_pos, y_pos),12)
            else:
                pygame.draw.circle(screen,DISC_COLOUR_2,(x_pos, y_pos),12)

        self.Draw_Side_Panels(screen)

    def Handle_Click(self, pos, screen):
        x,y = pos
        row = y//100
        col = (x - SIDE_PANEL_WT)//100 # Account for the left panel offset in clicks
        if 0 <= row < 8 and 0 <= col < 8 :
            return self.Make_Move(row,col)
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
        screen.fill((0,0,0))
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
        color = (0,255,255)   # P1 Cyan
    else:
        color = (220,20,60)   # P2 Red

    winner_surf = font_winner.render(text, True, color)
    screen.blit(winner_surf, winner_surf.get_rect(center=(SCREEN_WT//2, 265)))

def run(Player1, Player2):
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WT, SCREEN_HT))
    pygame.display.set_caption("Othello")
    clock  = pygame.time.Clock()
    Game   = Othello(Player1, Player2)
    running   = True
    game_over = False
    result    = 0
    count     = 1
    leader_btn = None

    while running:
        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not game_over:
                    if Game.Handle_Click(event.pos, screen):
                        Game.Player_Switch()
                        # check if current player has no moves
                        if not Game.get_all_valid_moves(Game.Current_Player_Value):
                            Game.Player_Switch()
                            # if neither player has moves — game ends
                            if not Game.get_all_valid_moves(Game.Current_Player_Value):
                                result    = Game.Winning_condition()
                                game_over = True  
                else:
                    if leader_btn and leader_btn.collidepoint(event.pos):
                        metric = show_metric_screen(screen, clock)
                        pygame.quit()
                        code = Game.Leaderboard_Display(metric)
                        sys.exit(code)

        screen.fill((0, 0, 0))
        Game.Draw_Board(screen)

        if game_over:
            if result == 3:
                text = "It's a Draw!"
                w_name, l_name, is_draw = Player1, Player2, True
            elif result == 1:
                text = f"{Player1} Wins!"
                w_name, l_name, is_draw = Player1, Player2, False
            else:
                text = f"{Player2} Wins!"
                w_name, l_name, is_draw = Player2, Player1, False

            if count == 1:
                Game.Log_Game_Result("Othello", w_name, l_name, is_draw)
                count = 0

            draw_gameover(screen, text, Player1, Player2)
            leader_btn = draw_hub_button(
                screen, "View Leaderboard", 400, mouse, width=LEADER_BTN_WT)

        pygame.display.update()
        clock.tick(60)

    pygame.quit()
    sys.exit(1)

if __name__ == "__main__":
    Player1 = sys.argv[1]
    Player2 = sys.argv[2]
    run(Player1,Player2)
    pygame.quit()
    sys.exit()