import pygame
import numpy as np

class Panel:
    def __init__(self,screen,top=30,bottom=710,left=300,right=980,grid_number=14):
        self.top=top
        self.bottom=bottom
        self.left=left
        self.right=right
        self.grid_number=grid_number
        self.turn=1
        self.state=np.zeros((grid_number+1,grid_number+1))
        self.luozi=[]
        self.screen=screen
    
    def draw_panel(self):
        self.screen.fill((224,224,224))
        length=(self.right-self.left)/self.grid_number
        width=(self.bottom-self.top)/self.grid_number
        edge=[(self.left-25,self.top-25),(self.left-25,self.bottom+25),(self.right+25,self.bottom+25),(self.right+25,self.top-25)]
        pygame.draw.rect(self.screen,"orange",((self.left-25,self.top-25),(self.right-self.left+50,self.bottom-self.top+50)))
        pygame.draw.lines(self.screen,"black",True,edge,2)
        pygame.draw.circle(self.screen,"black",((self.left+self.right)/2,(self.top+self.bottom)/2),3)
        for i in range(self.grid_number+1):
            pygame.draw.line(self.screen,"black",(self.left,self.top+width*i),(self.right,self.top+width*i))
            pygame.draw.line(self.screen,"black",(self.left+length*i,self.top),(self.left+length*i,self.bottom))
        for j in range(self.grid_number+1):
            for k in range(self.grid_number+1):
                if self.state[j][k]==1:
                    pygame.draw.circle(self.screen,"black",(self.left+length*k,self.top+length*j),20)
                elif self.state[j][k]==-1:
                    pygame.draw.circle(self.screen,"white",(self.left+length*k,self.top+length*j),20)
        
    
    def write_words(self):
        font = pygame.font.Font(None, 36)
        if self.game_over()==0:
            status = "Status: In Progress"
            turn = "Current Turn: " + ("Black" if self.turn == 1 else "White")
            text_surface_status = font.render(status, True, (0, 0, 0))
            text_surface_turn = font.render(turn, True, (0, 0, 0))
            self.screen.blit(text_surface_status, (self.right+50, self.top+30))
            self.screen.blit(text_surface_turn, (self.right+50, self.top+60))
        elif self.game_over()==1 or self.game_over()==-1:
            status = "Status: Game Over"
            winner = "Winner: " + ("Black" if self.game_over() == 1 else "White")
            text_surface_status = font.render(status, True, (0, 0, 0))
            text_surface_winner = font.render(winner, True, (0, 0, 0))
            self.screen.blit(text_surface_status, (self.right+50, self.top+30))
            self.screen.blit(text_surface_winner, (self.right+50, self.top+60))
        elif self.game_over()==100:
            status = "Status: Game Over"
            winner = "Draw"
            text_surface_status = font.render(status, True, (0, 0, 0))
            text_surface_winner = font.render(winner, True, (0, 0, 0))
            self.screen.blit(text_surface_status, (self.right+50, self.top+30))
            self.screen.blit(text_surface_winner, (self.right+50, self.top+60))

        self.text_surface_restart=font.render("Click to restart", True, (0, 0, 0))
        pygame.draw.rect(self.screen,(0,220,250),(self.right+45, self.top+145, self.text_surface_restart.get_width()+10, self.text_surface_restart.get_height()+10))
        self.screen.blit(self.text_surface_restart, (self.right+50, self.top+150))
        

        self.text_surface_undo=font.render("Click to undo", True, (0, 0, 0))
        pygame.draw.rect(self.screen,(255,0,127),(self.right+45, self.top+215, self.text_surface_undo.get_width()+10, self.text_surface_undo.get_height()+10))
        self.screen.blit(self.text_surface_undo, (self.right+50, self.top+220))


    def pos2grid(self,x,y):
        length=(self.right-self.left)/self.grid_number
        width=(self.bottom-self.top)/self.grid_number
        row=-1
        col=-1
        for i in range(self.grid_number+1):
            if self.left+length*i-length*0.4<=x and self.left+length*i+length*0.4>=x:
                col=i
                break
        for j in range(self.grid_number+1):
            if self.top+width*j-width*0.4<=y and self.top+width*j+width*0.4>=y:
                row=j
                break
        return row,col
    def can_luozi(self,row,col):
        if row==-1 or col==-1 or self.game_over()!=0:
            return False
        return self.state[row][col]==0
    def click (self,x,y):
        row,col=self.pos2grid(x,y)
        if self.can_luozi(row,col):
            self.state[row][col]=self.turn
            self.turn=-self.turn
            self.luozi.append((row,col,self.turn))
        if self.right+45<=x<=self.right+45+self.text_surface_restart.get_width()+10 and self.top+145<=y<=self.top+145+self.text_surface_restart.get_height()+10:
            self.state=np.zeros((self.grid_number+1,self.grid_number+1))
            self.luozi=[]
            self.turn=1
        if self.right+45<=x<=self.right+45+self.text_surface_undo.get_width()+10 and self.top+215<=y<=self.top+215+self.text_surface_undo.get_height()+10:
            if len(self.luozi)>0:
                self.state[self.luozi[-1][0]][self.luozi[-1][1]]=0
                self.luozi.pop()
                self.turn=-self.turn

        self.draw_panel()
        self.write_words()

    def game_over(self):
        a=self.state
        
        for i in range(self.grid_number+1):
            for j in range(self.grid_number-3):
                if abs(a[i][j])==1 and a[i][j+1]==a[i][j] and a[i][j+2]==a[i][j] and a[i][j+3]==a[i][j] and a[i][j+4]==a[i][j]:
                    return a[i][j]
        for i in range(self.grid_number-3):
            for j in range(self.grid_number+1):
                if abs(a[i][j])==1 and a[i+1][j]==a[i][j] and a[i+2][j]==a[i][j] and a[i+3][j]==a[i][j] and a[i+4][j]==a[i][j]:
                    return a[i][j]
        for i in range(self.grid_number-3):
            for j in range(self.grid_number-3):
                if abs(a[i][j])==1 and a[i+1][j+1]==a[i][j] and a[i+2][j+2]==a[i][j] and a[i+3][j+3]==a[i][j] and a[i+4][j+4]==a[i][j]:
                    return a[i][j]
        for i in range(4,self.grid_number+1):
            for j in range(self.grid_number-3):
                if abs(a[i][j])==1 and a[i-1][j+1]==a[i][j] and a[i-2][j+2]==a[i][j] and a[i-3][j+3]==a[i][j] and a[i-4][j+4]==a[i][j]:
                    return a[i][j]
                
        if len(self.luozi)==(self.grid_number+1)**2:
            return 100
        
        return 0
    

def start_game():
    pygame.init()
    screen=pygame.display.set_mode((1280, 780))
    running=True
    panel=Panel(screen)
    panel.draw_panel()
    panel.write_words()
    pygame.display.flip()

    down=True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        button=pygame.mouse.get_pressed()
    
        if down==True:
            if button[0]:
                pre_x,pre_y=pygame.mouse.get_pos()
                pre_row,pre_col= panel.pos2grid(pre_x,pre_y)
                down=False
        if down==False:
            if button[0]==False:
                post_x,post_y=pygame.mouse.get_pos()
                post_row,post_col=panel.pos2grid(post_x,post_y)
                if post_row==pre_row and post_col==pre_col:
                    panel.click(post_x,post_y)
                    pygame.display.flip()
                down=True
    pygame.quit()


if __name__ == '__main__':
    start_game()