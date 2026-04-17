import pygame
import sys
import numpy as np
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from game import Game_Base
# Constants
ROWS,COLS=10,10
WIDTH,HEIGHT=600,600

CELL_SIZE = WIDTH//COLS

LINE_COLOR = (200,200,200)
P1_COLOR = (255,100,100)
P2_COLOR = (100,150,255)
BG_COLOR = (255,216,172)


class TicTacToe(Game_Base): #TicTacToe is child class of Game_Base
    
    
    def Make_move(self,row,col):
        if self.Game_Board[row,col]==0:
            self.Game_Board[row,col]=self.Current_Player_Value
            return True
        
        return False
    
    def Draw_Board(self, screen):
        screen.fill(BG_COLOR)

        # Grid lines
        for i in range(ROWS):
            pygame.draw.line(screen, LINE_COLOR,
                             (0, i * CELL_SIZE),
                             (WIDTH, i * CELL_SIZE))
        for j in range(COLS):
            pygame.draw.line(screen, LINE_COLOR,
                             (j * CELL_SIZE, 0),
                             (j * CELL_SIZE, HEIGHT))

        # Draw X and O
        for r in range(ROWS):
            for c in range(COLS):
                if self.Game_Board[r, c] == 1:
                    #  X
                    # pygame.draw.line(surface,color,start,end)
                    pygame.draw.line(screen, P1_COLOR,
                                     (c*CELL_SIZE+10, r*CELL_SIZE+10),
                                     ((c+1)*CELL_SIZE-10, (r+1)*CELL_SIZE-10), 3)
                    pygame.draw.line(screen, P1_COLOR,
                                     ((c+1)*CELL_SIZE-10, r*CELL_SIZE+10),
                                     (c*CELL_SIZE+10, (r+1)*CELL_SIZE-10), 3)
                elif self.Game_Board[r, c] == 2:
                    # O
                    # pygame.draw(surface,color,center,radius)
                    pygame.draw.circle(screen, P2_COLOR,
                                       (c*CELL_SIZE + CELL_SIZE//2,
                                        r*CELL_SIZE + CELL_SIZE//2),
                                       CELL_SIZE//3, 3)
            
    def Handle_Click(self, pos, screen):
        x,y = pos
        row = y//CELL_SIZE         
        col = x//CELL_SIZE
        
        if col<COLS:
            return self.Make_move(row,col)
        return False
    
    def Winning_condition(self):
        board = self.Game_Board
        #horizontal
        for i in range(ROWS):
             for j in range(COLS-4):
                 seq = board[i,j:j+5]
                 if np.all(seq==1):
                     return 1
                 if np.all(seq==2):
                     return 2
        # vertical
        ver_check = np.zeros((1,10),dtype=int)
        
        if np.any(ver_check==1):
             return 1
        if np.any(ver_check==2):
             return 2
        
        # # diagonal
        
        return 0
if __name__=="__main__":
    pygame.init()
    screen = pygame.display.set_mode((WIDTH,HEIGHT))
    screen.fill(BG_COLOR)
    
    def draw_center_banner(screen, text_main, text_sub, font_big, font_small):
        

        banner_height = 120

        # Create transparent surface
        overlay = pygame.Surface((WIDTH, banner_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # black with transparency

        # Position (center vertically)
        y_pos = HEIGHT // 2 - banner_height // 2

        # Draw banner
        screen.blit(overlay, (0, y_pos))

        # Main text
        main_text = font_big.render(text_main, True, (255, 255, 255))
        main_rect = main_text.get_rect(center=(WIDTH // 2, y_pos + 40))

        # Sub text
        sub_text = font_small.render(text_sub, True, (220, 220, 220))
        sub_rect = sub_text.get_rect(center=(WIDTH // 2, y_pos + 80))

        # Draw text
        screen.blit(main_text, main_rect)
        screen.blit(sub_text, sub_rect)
        
    
    clock = pygame.time.Clock()
    running = True # for pygame window
    
    p1 = sys.argv[1] 
    p2 = sys.argv[2]
    
    game = TicTacToe(p1,p2,ROWS,COLS)
    game_over = False # will show game over if this becomes True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                if game.Handle_Click(event.pos,screen):
                    result = game.Winning_condition()
                    if result != 0:
                        game_over = True
                    else:
                        game.Player_Switch()

            # ALWAYS DRAW BOARD FIRST
            game.Draw_Board(screen)

            # THEN DRAW OVERLAY
            if game_over:
                result = game.Winning_condition()

                if result == 1:
                    text = f"{p1} Wins!!"
                elif result == 2:
                    text = f"{p2} Wins!!"
                else:
                    text = "Draw"

                font_big = pygame.font.SysFont(None, 60)
                font_small = pygame.font.SysFont(None, 30)

                draw_center_banner(screen,f"{text}","Press anywhere to view leaderboard",font_big,font_small)

        pygame.display.update()
        clock.tick(60)