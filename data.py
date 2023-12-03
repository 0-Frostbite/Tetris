import pygame, random, time
from sys import exit
from pygame.locals import *
from os import path

S = [[0,1,0],[0,1,1],[0,0,1]],[[0,1,1],[1,1,0],[0,0,0]]
L = [[0,2,0],[0,2,0],[0,2,2]],[[0,0,0],[2,2,2],[2,0,0]],[[2,2,0],[0,2,0],[0,2,0]],[[0,0,2],[2,2,2],[0,0,0]]
O = [[[3,3],[3,3]]]
Z = [[0,0,4],[0,4,4],[0,4,0]],[[4,4,0],[0,4,4],[0,0,0]]
I = [[0,5,0,0],[0,5,0,0],[0,5,0,0],[0,5,0,0]],[[5,5,5,5],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
J = [[0,6,0],[0,6,0],[6,6,0]],[[6,0,0],[6,6,6],[0,0,0]],[[0,6,6],[0,6,0],[0,6,0]],[[0,0,0],[6,6,6],[0,0,6]]
T = [[0,7,0],[7,7,7],[0,0,0]],[[0,7,0],[0,7,7],[0,7,0]],[[0,0,0],[7,7,7],[0,7,0]],[[0,7,0],[7,7,0],[0,7,0]]

pygame.init()

Res = X_Res,Y_Res = 530,720
Screen=pygame.display.set_mode(Res,NOFRAME)
pygame.display.set_caption("Tetris")

Main = pygame.font.Font('arcade.ttf', 40)
Header = pygame.font.Font('arcade.ttf',140)
Main2 = pygame.font.Font('arcade.ttf',30)
score = 0

class Game_Over:

    def __init__(self):
         
        self.b_Play = Main.render('Play Again',True,(255,255,255),(16,16,16))
        self.b_PlayBox = self.b_Play.get_rect()
        self.b_PlayBox.center = (X_Res//2,7*Y_Res//10)

        self.score = Main.render('You Scored',True,(255,255,255),(16,16,16))
        self.scoreBox = self.score.get_rect()
        self.scoreBox.center = (X_Res//2,3*Y_Res//10)

        self.score1 = Header.render(str(score),True,(255,255,255),(16,16,16))
        self.score1Box = self.score1.get_rect()
        self.score1Box.center = (X_Res//2,4*Y_Res//10)

        self.b_Quit = Main.render('QUIT',True,(255,255,255),(16,16,16))
        self.b_QuitBox = self.b_Quit.get_rect()
        self.b_QuitBox.center = (X_Res//2,8*Y_Res//10)
    
        self.buttons={3:self.b_PlayBox,2:self.b_QuitBox}

    def run(self,key=0):
        
        Screen.blit(self.b_Play,self.b_PlayBox)
        Screen.blit(self.b_Quit,self.b_QuitBox)
        Screen.blit(self.score1,self.score1Box)
        Screen.blit(self.score,self.scoreBox)
        

class Instruct:

    def __init__(self):

        self.b_Back = Main.render("Back",True,(255,255,255))
        self.b_BackBox = self.b_Back.get_rect()
        self.b_BackBox.center = (X_Res//2,9*Y_Res//10)

        self.buttons={0:self.b_BackBox}

        Back = pygame.image.load(path.join('assets','Back_Screen.jpg'))
        Screen.blit(Back,Screen.get_rect())
        
    def run(self,key=0):
        
        Screen.blit(self.b_Back,self.b_BackBox)

class Level:

    def __init__(self):

        global score

        score = 0

        self.Base_Tile = pygame.image.load(path.join('assets','Base.png'))
        self.S_Tile = pygame.image.load(path.join('assets','S.png'))
        self.L_Tile = pygame.image.load(path.join('assets','L.png'))
        self.O_Tile = pygame.image.load(path.join('assets','O.png'))
        self.Z_Tile = pygame.image.load(path.join('assets','Z.png'))
        self.I_Tile = pygame.image.load(path.join('assets','I.png'))
        self.J_Tile = pygame.image.load(path.join('assets','J.png'))
        self.T_Tile = pygame.image.load(path.join('assets','T.png'))

        self.Music = pygame.mixer.Sound(path.join('assets','Lo.wav'))
        self.Music.play(loops=-1)
        self.Music.set_volume(0.5)

        self.Destroy = pygame.mixer.Sound(path.join('assets','Line.wav'))
        self.Destroy.set_volume(0.5)
        
        self.Grid = []
        self.shapes = [S,L,O,Z,I,J,T]
        self.colours = [self.Base_Tile,self.S_Tile,self.L_Tile,self.O_Tile,self.Z_Tile,self.I_Tile,self.J_Tile,self.T_Tile]
        self.next_piece,self.play_piece = self.shapes[random.randint(0,6)],0

        self.frame = pygame.image.load(path.join('assets','Game_Screen.png'))
        Screen.blit(self.frame,Screen.get_rect())                               

        [self.Grid.append([pygame.Rect(rows*35+10,columns*35+10,35,35) for rows in range(10)]) for columns in range(20)]
        self.Grid_Code = [[0,0,0,0,0,0,0,0,0,0] for i in range(23)]

        self.Display_Grid = []
        [self.Display_Grid.append([pygame.Rect(rows*35+390,columns*35+210,35,35) for rows in range(3)]) for columns in range(4)]
        self.Display_Grid_Code = [[0,0,0] for i in range(4)]

        self.shapeN = Main2.render('Next',True,(200,200,200))
        self.shapeN_Box = self.shapeN.get_rect()
        self.shapeN_Box.center = (445,50)

        self.shape = Main2.render('Shape',True,(200,200,200))
        self.shape_Box = self.shape.get_rect()
        self.shape_Box.center = (445,70)

        self.Score = Main2.render('Score',True,(200,200,200))
        self.Score_Box = self.Score.get_rect()
        self.Score_Box.center = (445,560)

        self.buttons = {}

    def run(self,key):

        global score

        pygame.draw.rect(Screen,(16,16,16),pygame.Rect(370,10,150,480))
        pygame.draw.rect(Screen,(16,16,16),pygame.Rect(370,500,150,200))

        self.Score2 = Main2.render(str(score),True,(255,255,255))
        self.Score2_Box = self.Score2.get_rect()
        self.Score2_Box.center = (445,610)

        Screen.blit(self.shape,self.shape_Box)
        Screen.blit(self.shapeN,self.shapeN_Box)
        Screen.blit(self.Score,self.Score_Box)
        Screen.blit(self.Score2,self.Score2_Box)
        
        for y in range(4):
            for x in range(3):
                try:
                    code=self.next_piece[0][y][x]
                except IndexError:
                    code=0

                Screen.blit(self.colours[code],self.Display_Grid[y][x])
        
        self.key=key

        if self.play_piece!=[]:
            if key == 115:      # S key - Down
                new_play_piece_points = []                
                for pointY,pointX in self.play_piece_points[::-1]:
                    index=self.play_piece_points.index([pointY,pointX])
                    if pointY<22:   
                        if self.Grid_Code[pointY+1][pointX]==0 or ([pointY+1,pointX] in self.play_piece_points) :
                            new_play_piece_points.append([pointY+1,pointX])  
                        else:
                            self.play_piece=[]
                            break                     
                    else:
                        self.play_piece=[]
                        break
                if len(new_play_piece_points) == 4:
                    for pointY,pointX in new_play_piece_points:
                        self.Grid_Code[pointY][pointX] = self.Grid_Code[pointY-1][pointX]  
                        self.play_piece_points[index]=[pointY,pointX]
                        self.Grid_Code[pointY-1][pointX] = 0
                        if pointY>=3:
                            Screen.blit(self.colours[self.Grid_Code[pointY][pointX]],self.Grid[pointY-3][pointX])
                        if pointY>=4:
                            Screen.blit(self.colours[0],self.Grid[pointY-4][pointX])
                    self.play_piece_points = new_play_piece_points[::-1]      
                else:
                    self.play_piece=[]

            elif key == 97:     # A key - Left
                new_play_piece_points = []
                for pointY,pointX in self.play_piece_points:
                    index=self.play_piece_points.index([pointY,pointX])
                    if pointX>0:
                        if self.Grid_Code[pointY][pointX-1]==0 or ([pointY,pointX-1] in self.play_piece_points):
                            new_play_piece_points.append([pointY,pointX-1])
                if len(new_play_piece_points) == 4:    
                    for pointY,pointX in new_play_piece_points:
                        self.Grid_Code[pointY][pointX] = self.Grid_Code[pointY][pointX+1]  
                        self.play_piece_points[index]=[pointY,pointX]
                        self.Grid_Code[pointY][pointX+1] = 0
                        if pointY>=3:
                            Screen.blit(self.colours[self.Grid_Code[pointY][pointX]],self.Grid[pointY-3][pointX])
                            Screen.blit(self.colours[0],self.Grid[pointY-3][pointX+1])
                    self.play_piece_points = new_play_piece_points[::]                  
            
            elif key == 100:    # D key - Right
                new_play_piece_points = []
                for pointY,pointX in self.play_piece_points[::-1]:
                    index=self.play_piece_points.index([pointY,pointX])
                    if pointX<9:
                        if self.Grid_Code[pointY][pointX+1]==0 or ([pointY,pointX+1] in self.play_piece_points):
                            new_play_piece_points.append([pointY,pointX+1])
                if len(new_play_piece_points)==4:
                    for pointY,pointX in new_play_piece_points:
                        self.Grid_Code[pointY][pointX] = self.Grid_Code[pointY][pointX-1]  
                        self.play_piece_points[index]=[pointY,pointX]
                        self.Grid_Code[pointY][pointX-1] = 0
                        if pointY>=3:
                            Screen.blit(self.colours[self.Grid_Code[pointY][pointX]],self.Grid[pointY-3][pointX])
                            Screen.blit(self.colours[0],self.Grid[pointY-3][pointX-1])
                        self.play_piece_points = new_play_piece_points[::-1]

            elif key == 32:     # SPACE key - Rotate
                self.spin+=1
                if len(self.play_piece)-1<self.spin:
                    self.spin=0
                    
                length = len(self.play_piece[0])
                y,x = self.play_piece_points[0]
                x-=1
                new_play_piece_points=[]

                if y<=22-length and -1<x<=10-length:
                    for row in self.play_piece[self.spin]:
                        for unit in row:
                            if unit!=0 and (self.Grid_Code[y][x]==0 or [y,x] in self.play_piece_points):
                                new_play_piece_points.append([y,x])
                            x+=1
                        y+=1
                        x-=length
                new_play_piece_points.sort()
                
                if len(new_play_piece_points)==4:
                    for y,x in self.play_piece_points:
                        self.Grid_Code[y][x] = 0
                        Screen.blit(self.colours[0],self.Grid[y-3][x])

                    self.play_piece_points = new_play_piece_points[::]

                    for y,x in self.play_piece_points:
                        self.Grid_Code[y][x] = self.shapes.index(self.play_piece)+1
                        Screen.blit(self.colours[0],self.Grid[y-3][x])

        if not self.play_piece:
            
            count=0
            for row in range(3,23):
                if self.Grid_Code[row].count(0)==0:
                    self.Destroy.play()
                    del self.Grid_Code[row]
                    count+=1
                    self.Grid_Code.insert(0,[0,0,0,0,0,0,0,0,0,0])
            for row in range(3,23):       
                for unit in range(10):
                    Screen.blit(self.colours[self.Grid_Code[row][unit]],self.Grid[row-3][unit])
            if count!=0:
                score += count*100+(count-1)*50



            self.play_piece = self.next_piece
            self.play_piece_points = []
            self.next_piece = self.shapes[random.randint(0,6)]
            self.spin=0
            self.Point_X,self.Point_Y = 4,0
            for sub in self.play_piece[self.spin] :
                for sub_sub in sub:
                    if self.Point_Y<20 and (self.Grid_Code[self.Point_Y][self.Point_X]==0):
                        self.Grid_Code[self.Point_Y][self.Point_X] += sub_sub
                        if self.Grid_Code[self.Point_Y][self.Point_X]!=0:
                            self.play_piece_points.append([self.Point_Y,self.Point_X])
                        self.Point_X+=1
                    else:
                        self.Music.fadeout(2)
                        return 4
                        break
                self.Point_Y+=1
                self.Point_X=4
        else:
            new_play_piece_points = []
            for pointY,pointX in self.play_piece_points[::-1]:
                index=self.play_piece_points.index([pointY,pointX])
                if pointY<22:
                    if self.Grid_Code[pointY+1][pointX]==0 or ([pointY+1,pointX] in self.play_piece_points) :
                        new_play_piece_points.append([pointY+1,pointX])  
                    else:
                        self.play_piece=[]
                        break                     
                else:
                    self.play_piece=[]
                    break
            
            if len(new_play_piece_points) == 4:
                for pointY,pointX in new_play_piece_points:
                    self.Grid_Code[pointY][pointX] = self.Grid_Code[pointY-1][pointX]  
                    self.play_piece_points[index]=[pointY,pointX]
                    self.Grid_Code[pointY-1][pointX] = 0
                    if pointY>=3:
                        Screen.blit(self.colours[self.Grid_Code[pointY][pointX]],self.Grid[pointY-3][pointX])
                    if pointY>=4:
                        Screen.blit(self.colours[0],self.Grid[pointY-4][pointX])
                self.play_piece_points = new_play_piece_points[::-1]
            else:
                self.play_piece=[]     
               
class Menu:

    def __init__(self):

        self.Head = Header.render('TETRIS', True, (255,0,255))
        self.HeadBox = self.Head.get_rect()
        self.HeadBox.center = (X_Res//2,Y_Res//4)

        self.Head1 = Header.render('TETRIS', True, (0,255,255))
        self.HeadBox1 = self.Head1.get_rect()
        self.HeadBox1.center = (X_Res//2+3,Y_Res//4+5)

        self.b_Start = Main.render('START',True,(255,255,255))
        self.b_StartBox = self.b_Start.get_rect()
        self.b_StartBox.center = (X_Res//2,6*Y_Res//10)

        self.b_Instruct = Main.render('INSTRUCTIONS',True,(255,255,255))
        self.b_InstructBox = self.b_Instruct.get_rect()
        self.b_InstructBox.center = (X_Res//2,7*Y_Res//10)

        self.b_Quit = Main.render('QUIT',True,(255,255,255))
        self.b_QuitBox = self.b_Quit.get_rect()
        self.b_QuitBox.center = (X_Res//2,8*Y_Res//10)

        self.frame1 = pygame.image.load(path.join('assets','Menu_Screen.jpg'))
        self.frame2 = pygame.image.load(path.join('assets','Menu_Screen2.jpg'))
        self.frame_count=0

        self.buttons = {3:self.b_StartBox,1:self.b_InstructBox,2:self.b_QuitBox}

    def run(self,key=0):

        if self.frame_count==0:
            Screen.blit(self.frame1,Screen.get_rect())
            self.frame_count=1
        else:
            Screen.blit(self.frame2,Screen.get_rect())
            self.frame_count=0

        Screen.blit(self.Head,self.HeadBox)
        Screen.blit(self.Head1,self.HeadBox1)
        Screen.blit(self.b_Start,self.b_StartBox)
        Screen.blit(self.b_Instruct,self.b_InstructBox)
        Screen.blit(self.b_Quit,self.b_QuitBox)

class Quit:

    def __init__(self):
        pygame.quit()
        exit()
