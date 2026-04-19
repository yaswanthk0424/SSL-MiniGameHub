import pygame
import sys,os
import numpy as np
import csv
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from game import Game_Base
#COlOUR CONSTANTS
BG_COlOUR = (0,0,0)
DISC_COLOUR_1 = (226, 32, 32)
DISC_COLOUR_2 = (255,215,0)
ROWS = 7
COLS = 7
class Connect_4(Game_Base):
    def __init__(self, player1, player2):
        super().__init__(player1, player2,ROWS,COLS)
    def Winning_condition(self):
        boolean_mask = (self.Game_Board == self.Current_Player_Value)
        #horizontal check 
        if np.any(boolean_mask[:,:-3] & boolean_mask[:,1:-2]&boolean_mask[:,2:-1]&boolean_mask[:,3:]):
            return self.Current_Player_Value
        #vertical check
        elif np.any(boolean_mask[:-3,:] & boolean_mask[1:-2,:]&boolean_mask[2:-1,:]&boolean_mask[3:,:]):
            return self.Current_Player_Value
        #diagonal check(\)
        elif np.any(boolean_mask[:-3,:-3] & boolean_mask[1:-2,1:-2]&boolean_mask[2:-1,2:-1]&boolean_mask[3:,3:]):
            return self.Current_Player_Value
        #diagonal check(/)
        elif np.any(boolean_mask[3:,:-3] & boolean_mask[2:-1,1:-2]&boolean_mask[1:-2,2:-1]&boolean_mask[:-3,3:]):
            return self.Current_Player_Value
        elif not np.any(self.Game_Board==0):
            return 3
        else: return 0
    def Make_Move(self,row,col):  
        column_data = self.Game_Board[row,:]
        empty_rows= np.where(column_data==0)[0]
        if empty_rows.size >0:
            self.Game_Board[row,empty_rows[-1]] = self.Current_Player_Value
            if self.Winning_condition() == 0:
                self.Player_Switch()
            return True
        return False
    def Draw_Board(self, screen):
        Board_Surface = pygame.image.load('./Images/Connect4/board_new.png').convert_alpha()
        Board_rect = Board_Surface.get_rect(center=(350,400))
        screen.blit(Board_Surface,Board_rect)
        p1_rows,p1_cols = np.where(self.Game_Board == 1) # returns rows and cols as seperate lists whereever 1 is present
        p2_rows,p2_cols = np.where(self.Game_Board == 2) 
        for row ,col in zip(p1_rows,p1_cols):
            x_pos = 100*row + 48
            y_pos = 50+100*col + 48
            pygame.draw.circle(screen,DISC_COLOUR_1,(x_pos,y_pos),40)
        for row,col in zip(p2_rows,p2_cols):
            x_pos = 100*row + 48
            y_pos = 50+100*col + 48
            pygame.draw.circle(screen,DISC_COLOUR_2,(x_pos,y_pos),40)
    def Handle_Click(self, pos , screen): 
            x,y = pos
            row = x//100
            col = y//100
            if col<self.cols:
                return self.Make_Move(row,col)
            return False
def run(player1, player2):
    pygame.init()
    Game = Connect_4(Player1,Player2)   
    screen = pygame.display.set_mode((700,750))
    pygame.display.set_caption("Connect Four")
    red_arrow_surface=pygame.image.load('./Images/Connect4/red_arrow.png').convert_alpha()
    yellow_arrow_surface=pygame.image.load('./Images/Connect4/yellow_arrow.png').convert_alpha()
    arrow_surface=[red_arrow_surface,yellow_arrow_surface]
    clock = pygame.time.Clock()
    running = True
    game_over = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 :
                mouse_pos = event.pos
                Game.Handle_Click(mouse_pos,screen)
                if Game.Winning_condition() != 0:
                    winner = Game.Winning_condition()
                    running = False
                    is_Draw = True if winner == 3 else False
                    if winner != 3:
                        Game.Log_Game_Result("Connect_4",Game.Player_List[winner-1],Game.Player_List[2-winner],is_Draw)
                    else:Game.Log_Game_Result("Connect_4",Game.Player1,Game.Player2,is_Draw)
                    game_over = True
        (mouse_pos_x,mouse_pos_y) = pygame.mouse.get_pos()
        column_no = mouse_pos_x//100
        arrow_rect = arrow_surface[1-Game.Current_Player_Value].get_rect(center = (49+column_no*100,30))
        screen.fill((0,0,0))
        Game.Draw_Board(screen)
        screen.blit(arrow_surface[1-Game.Current_Player_Value],arrow_rect)
        pygame.display.update()
        clock.tick(60)
    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        Game_over_surface = pygame.Surface((700, 750),pygame.SRCALPHA)
        Game_over_surface.fill((0, 0, 0, 180)) # 180 is the alpha (transparency) level
        screen.blit(Game_over_surface, (0, 0))
        text_font = pygame.font.SysFont("impact",72)
        if winner == 3:
            text_surface = text_font.render(f"Draw!", True, (255, 0, 0))
        else:
            text_surface = text_font.render(f"{Game.Player_List[winner-1]} Wins!", True, (255, 0, 0))
        text_rect = text_surface.get_rect(center=(350, 350))
        screen.blit(text_surface, text_rect)
        pygame.display.update()
        clock.tick(60)
if __name__ == "__main__":
    Player1 = sys.argv[1]
    Player2 = sys.argv[2]
    run(Player1, Player2)
    pygame.quit()
    sys.exit()