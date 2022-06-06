import pygame
from player import Player
from level import Level
import control

pygame.init()
#control.initSerial()

SCREEN_HEIGHT = 700
SCREEN_WIDTH = 400
START_X = SCREEN_WIDTH//2-10
START_Y = SCREEN_HEIGHT-80
FPS = 40

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Game")

bg = pygame.image.load("assets/sprites/bg_dark.jpg")
bg = pygame.transform.scale(bg, (bg.get_width()*SCREEN_HEIGHT/bg.get_height(),SCREEN_HEIGHT))
player = Player(screen, START_X, START_Y)
level = Level(screen, player)

deathFont = pygame.font.Font('assets/fonts/jokerman.ttf', 32)
scoreFont = pygame.font.Font('assets/fonts/pixel.fon', 16)
deathScreen = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT)) 
deathScreen.set_alpha(128)
deathScreen.fill((255,255,255)) 

def showText(font, s, color, x, y, place='c'):
    text=font.render(s, True, color)
    textRect = text.get_rect()
    if(place=='c'):
        textRect.center = (x,y)
    elif(place=='tr'):
        textRect.topright = (x,y)
    screen.blit(text, textRect) 

def redraw():
    screen.blit(bg, (0,0)) 
    level.draw()
    showText(scoreFont, f'Max score: {level.maxscore()}',(255,255,255), SCREEN_WIDTH-5, 5, 'tr')
    showText(scoreFont, f'Your score: {level.score()}',(255,255,255), SCREEN_WIDTH-5, 21, 'tr')

clock=pygame.time.Clock()
while(True):
    clock.tick(FPS)
    control.events()
    if not control.dead:
        #control.updateSerial()
        control.movements(player)
        player.jump() 
        level.update() 
        redraw()
        pygame.display.update()
        deathScreenShown=False 
    else:
        redraw()
        screen.blit(deathScreen, (0,0)) 
        control.updateRestartTime(FPS)
        showText(deathFont, f'Your score: {level.score()}',(255,0,0), SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 -32)
        showText(scoreFont, f'Press [Space] to restart ({int(control.restartTimer)+1} sec)',(0,0,0), SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 16)
        pygame.display.update()
        if(control.restartTimer==0):
            player.rect.topleft = (START_X, START_Y)
            level.reset()
            #control.initSerial()
            control.dead = False
