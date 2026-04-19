import pygame
import sys,os
import numpy as np
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from game import Game_Base
DISC_COLOUR_1 = (0,0,0)
DISC_COLOUR_2 = (255,255,255)
ROWS = 8
COLS = 8 
#(row,col) direction changes
DIRECTIONS = [(-1,-1),(-1,0),(-1,1),
              (0,-1),        (0,1),
              (1,-1), (1,0), (1,1)]
class Othello(Game_Base):
    def __init__(self,Player1,Player2):
        super().__init__(Player1,Player2,ROWS,COLS)
        self.Board_surface = pygame.image.load('./Images/Othello/Othello_board.png').convert_alpha()
        self.Board_rect = self.Board_surface.get_rect(center = (400,400))
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
    def Draw_Board(self, screen):
        screen.blit(self.Board_surface,self.Board_rect)
        p1_rows,p1_cols = np.where(self.Game_Board == 1)
        p2_rows,p2_cols = np.where(self.Game_Board == 2)
        for row ,col in zip(p1_rows,p1_cols):
            x_pos = 100*col + 50
            y_pos = 100*row + 50
            pygame.draw.circle(screen,DISC_COLOUR_1,(x_pos,y_pos),50)
        for row ,col in zip(p2_rows,p2_cols):
            x_pos = 100*col + 50
            y_pos = 100*row + 50
            pygame.draw.circle(screen,DISC_COLOUR_2,(x_pos,y_pos),50)  
        for r,c in self.get_all_valid_moves(self.Current_Player_Value):
            if self.Current_Player_Value==1:
                pygame.draw.circle(screen,DISC_COLOUR_1,(100*c+50,100*r+50),12)
            else:pygame.draw.circle(screen,DISC_COLOUR_2,(100*c+50,100*r+50),12)
    def Handle_Click(self, pos, screen):
        x,y = pos
        row = y//100
        col = x//100
        if 0 <= row < 8 and 0<= col < 8 :
            return self.Make_Move(row,col)
        return False
def run(Player1,Player2):
    pygame.init()
    screen = pygame.display.set_mode((800,800))
    pygame.display.set_caption("Othello")
    clock = pygame.time.Clock()
    Game = Othello(Player1,Player2)
    running = True
    result = 0
    Game_over = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if result == 0:
                    mouse_pos = event.pos
                    if Game.Handle_Click(mouse_pos,screen):
                        Game.Player_Switch()
                        if not Game.get_all_valid_moves(Game.Current_Player_Value):
                            Game.Player_Switch()
                            if not Game.get_all_valid_moves(Game.Current_Player_Value):
                                result = Game.Winning_condition()
                                is_Draw = (result == 3)
                                if result != 3:
                                    Game.Log_Game_Result("Othello",Game.Player_List[result-1],Game.Player_List[2-result],is_Draw)
                                else:Game.Log_Game_Result("Othello",Game.Player1,Game.Player2,is_Draw)
                                running = False
                                Game_over = True

        screen.fill((0,0,0))
        Game.Draw_Board(screen)
        pygame.display.update()
        clock.tick(60)
    font = pygame.font.SysFont("calibri", 48, bold=True)
    while Game_over and result != 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Game_over = False
        if result == 3:
            msg = "Draw!"
        else:
            winner = Game.Player_List[result - 1]
            msg = f"{winner} Wins!"
        screen.fill((0,0,0))
        text = font.render(msg, True, (255, 220, 50))
        screen.blit(text, text.get_rect(center=(400, 400)))
        pygame.display.update()
        clock.tick(60)
if __name__ == "__main__":
    Player1 = sys.argv[1]
    Player2 = sys.argv[2]
    run(Player1,Player2)
    pygame.quit()
    sys.exit()
