# importer modules
import time
from random import randrange

import pygame

pygame.init() # pylint: disable=no-member

BLANC=(255,255,255)
NOIR=(0,0,0)
ROUGE=(255,0,0)
VERT=(0,255,0)
VERTFONCE=(0,127,0)
GRIS=(128,128,128)
applecolor=pygame.Color(ROUGE)
#appleimg=pygame.image.load("apple_snake.jpg")
txtcolor=pygame.Color(NOIR)
snakecolor=pygame.Color(VERT)
headcolor=pygame.Color(VERTFONCE)
screencolor=pygame.Color((128,128,255))
stonecolor=pygame.Color(GRIS)
highscorefile="HIGH_SCORE.txt"
try:
    f=open(highscorefile, encoding="UTF8")
    highscore=int(f.read())
    f.close()
except:
    highscore=0


# largeur pixels par carré
d=32

# nbr carrés
lines,cols=15,30

# largeur, hauteur en pixels
w,h=cols*d,lines*d

pygame.display.set_caption("SNAKE le jeu le plus cool")
screen=pygame.display.set_mode((w,h))
clock=pygame.time.Clock()

font=pygame.font.Font(None,48)
petitfont=pygame.font.Font(None,18)

jouer=True
indices=False
gameover=False
autoplay=True

score=0
speed=1
pomme=(2,2)
tete=(7,3)
corps=[(5,3),(6,3)]
stones=[]
direction=(1,0)

def affiche_lines():
    for c in range(cols):
        x=c*d
        pygame.draw.line(screen,NOIR,(x,0),(x,lines*d))
    for l in range(lines):
        y=l*d
        pygame.draw.line(screen,NOIR,(0,y),(cols*d,y))
def affiche_indices():
    if indices:
        for c in range(cols):
            for l in range(lines):
                txt=str(c)+", "+str(l)
                img=petitfont.render(txt,True,txtcolor)
                x=c*d
                y=l*d
                screen.blit(img,(x,y))
                
def affiche_pomme():
    c,l=pomme
    x=c*d
    y=l*d
    pygame.draw.ellipse(screen,applecolor,(x,y,d,d))
    
    #screen.blit(appleimg,(x,y))
def affiche_stones():
    for stone in stones:
        c,l=stone
        x=c*d
        y=l*d
        pygame.draw.ellipse(screen,stonecolor,(x,y,d,d))
        
def affiche_snake():
    for c,l in corps:
        x=c*d
        y=l*d
        pygame.draw.ellipse(screen,snakecolor,(x,y,d,d))
    x,y=tete[0]*d,tete[1]*d
    pygame.draw.ellipse(screen,headcolor,(x,y,d,d))
    
def affiche_score():
    txt=font.render(str(score),True,txtcolor)
    screen.blit(txt,(d,d))
    txt=font.render("highscore:"+str(highscore),True,txtcolor)
    rect=txt.get_rect()
    rect.y=d
    rect.right=d*(cols-1)
    screen.blit(txt,rect)
    
def affiche_gameover():
    if gameover:
        if autoplay:
            txt=font.render('GAME OVER',True,txtcolor)
            screen.blit(txt,(3*d,d))
            txt=font.render('N to replay',True,txtcolor)
            screen.blit(txt,(3*d,d*2))
        else:
            txt=font.render('N to play',True,txtcolor)
            screen.blit(txt,(3*d,d*2))
            
def nouvelle_pomme(wh=True):
    global pomme
    c=randrange(cols)
    l=randrange(lines)
    pomme=(c,l)
    if wh:
        while pomme in [*corps,tete]:
            nouvelle_pomme(False)
            
def nouveau_snake():
    global tete,corps,direction
    c=randrange(2,cols//2+1)
#     l=randrange(2,lines//2+1)
    l=randrange(lines)
    direction=(1,0)
    tete=(c,l)
    corps=[(c-2,l),(c-1,l)]
    
def nouveau_stone(wh=True):
    global stone
    c=randrange(cols)
    l=randrange(lines)
    stone=(c,l)
    if wh:
        while stone in [*corps,tete,pomme,*stones]:
            nouveau_stone(False)
        stones.append(stone)
        
def move_snake():
    global score,tete
    corps.append(tete)
    tete=tete[0]+direction[0],tete[1]+direction[1]
    if tete==pomme:
        score+=1
        nouvelle_pomme()
        if not score%1:
            nouveau_stone()
    else:
        del corps[0]
    test_snake()
    
def test_snake():
    global gameover,tete
    if tete in (*corps,*stones) or not (-1<tete[0]<cols) or not (-1<tete[1]<lines):
        gameover=True
        if score>highscore:
            sethighscore(score)
            
def changehsva(color,h=0,s=0,v=0,a=0):
    hsva=color.hsva
    color.hsva=((hsva[0]+h)%360,hsva[1]+s%101,hsva[2]+v%101,hsva[3]+a%255)
    
def verifk(k):
    global indices,gameover,score,direction,autoplay,stones
    if 1:
            if k==pygame.K_i: # pylint: disable=no-member
                indices=not indices
            elif k==pygame.K_n: # pylint: disable=no-member
                gameover=False
                score=0
                stones=[]
                if autoplay:
                    nouveau_snake()
                    nouvelle_pomme()
                autoplay=True
            elif k==pygame.K_s: # pylint: disable=no-member
                nouveau_stone()
            if k==pygame.K_RIGHT: # pylint: disable=no-member
                if direction!=(-1,0):
                    direction=(1,0)
            elif k==pygame.K_DOWN: # pylint: disable=no-member
                if direction!=(0,-1):
                    direction=(0,1)
            elif k==pygame.K_LEFT: # pylint: disable=no-member
                if direction!=(1,0):
                    direction=(-1,0)
            elif k==pygame.K_UP: # pylint: disable=no-member
                if direction!=(0,1):
                    direction=(0,-1)
                    
def sethighscore(new):
    global highscore
    highscore=new
    f=open(highscorefile,"w")
    f.write(str(highscore))
    f.close()
    
if not autoplay:
    gameover=True
tt=time.time()
while jouer:
    for e in [*pygame.event.get()]:
        Break=True
        if e.type==pygame.QUIT: # pylint: disable=no-member:
            jouer=False
        elif e.type==pygame.KEYDOWN: # pylint: disable=no-member:
            k=e.key
            verifk(k)
        else:
            Break=False
        if Break:break
#     animation
    if not gameover:
        move_snake()
#     affiche
    screen.fill(screencolor)
    affiche_lines()
    affiche_indices()
    affiche_pomme()
    affiche_stones()
    affiche_snake()
    affiche_score()
    affiche_gameover()
    pygame.display.flip()
    changehsva(screencolor,4)
    changehsva(headcolor,4)
    changehsva(snakecolor,4)
    speed=4+score/2
    tt2=time.time()
    #print(round(tt2-tt,2))
    clock.tick(speed)
    tt=tt2
pygame.quit() # pylint: disable=no-member
# exit()
