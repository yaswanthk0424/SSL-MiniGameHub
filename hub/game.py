import pygame
import numpy
import sys

# start menu
if __name__ == "__main__":
    # initialise pygame
    pygame.init()
    # storing player's name
    user1 = sys.argv[1]
    user2 = sys.argv[2]
    
    # dict name to path
    game_names_toPaths = {}
    
    with open("games.csv","r") as file:
        for line in file:
            arr = line.strip().split(',')
            game_names_toPaths[arr[0]] = arr[1]
    
    # dimensions
    SCREEN_WT = 800
    SCREEN_HT = 500
    title_ht,title_wt = SCREEN_HT/5,SCREEN_WT #text "user1 vs user2"
    header_ht,header_wt = SCREEN_HT/6,SCREEN_WT #text "GAME HUB"
    button_wt = SCREEN_WT/3 
    button_ht = SCREEN_HT/12
    
    BUTTON_BORDER_RADIUS = 0
    # screen
    SCREEN = pygame.display.set_mode((SCREEN_WT,SCREEN_HT))
    
    # colors
    BG_COLOR = (15, 25, 35)         
    BUTTON_FONT_COLOR = (255, 255, 255)
    BUTTON_BG = (40, 60, 110)         
    LIGHT_BUTTON_BG = (60, 90, 160)   
    
    HEADER_BG = (25, 35, 50)          
    HEADER_FONT_COLOR = (0, 200, 200)  
    
    TITLE_BG = (40, 45, 60)           
    TITLE_FONT_COLOR = (255, 255, 255) 
    
    QUIT_BG = (130, 40, 40)           
    LIGHT_QUIT_BG = (180, 50, 50)     
    
    # Fonts 
    TITLE_FONT = pygame.font.SysFont("lucida",100)
    HEADER_FONT = pygame.font.SysFont("timesnewroman",60)
    BUTTON_FONT = pygame.font.SysFont("calibri",40)
    
    def makeBox(text_surface, center_y, wt, ht, color, border_radius=0):
        rect = pygame.Rect(0,0,wt,ht) #rect with req dimensions(virtually)
        rect.center = (SCREEN_WT/2,center_y) #shifting rect to desired centre(virtually)
        pygame.draw.rect(SCREEN,color,rect,border_radius) #pasting on screen
        text_rect = text_surface.get_rect(center = rect.center) #creating a rect for text and centering
        SCREEN.blit(text_surface,text_rect) #pasting
    
    def makeButton(text,center_y,mouse):
        button_text = BUTTON_FONT.render(text,True,BUTTON_FONT_COLOR)
        button_rect = pygame.Rect(0,0,button_wt,button_ht)
        button_rect.center = (SCREEN_WT//2,center_y)
        button_color =  BUTTON_BG if text != "QUIT" else QUIT_BG
        if button_rect.collidepoint(mouse):
            button_color = LIGHT_BUTTON_BG if text != "QUIT" else LIGHT_QUIT_BG
        
        pygame.draw.rect(SCREEN, button_color, button_rect, border_radius=BUTTON_BORDER_RADIUS)
        text_rect = button_text.get_rect(center = button_rect.center)
        SCREEN.blit(button_text, text_rect)
        
    def startmenu():
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pass
                    
            mouse = pygame.mouse.get_pos()
            SCREEN.fill(BG_COLOR)
            
            # title 
            title_text = TITLE_FONT.render("GameHub",True,TITLE_FONT_COLOR) 
            center_y = title_ht//2
            makeBox(title_text,center_y,title_wt,title_ht,TITLE_BG)
            
            # Header
            header_text = HEADER_FONT.render(f"{user1} v/s {user2}",True,HEADER_FONT_COLOR)
            header_center_y = title_ht + (header_ht/2)
            makeBox(header_text,header_center_y,header_wt,header_ht,HEADER_BG)
            
            # Game Buttons
            game_names = list(game_names_toPaths.keys())
            button_center_y = title_ht + header_ht 
            for i in range(len(game_names_toPaths)):
                button_text = game_names[i]
                button_center_y += button_ht//2 + 50
                makeButton(button_text,button_center_y,mouse)
            
            # quit button
            quit_center_y = button_center_y + (button_ht/2) + 50
            makeButton("QUIT",quit_center_y,mouse)
            
            pygame.display.update()
    startmenu()
    pygame.quit()
    sys.exit()