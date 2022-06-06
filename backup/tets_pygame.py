from os import remove
import pygame
from player import Player
from block import Block
from camera import Camera
from collisions import check_collison_top
from random import randint
import control


pygame.init()

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 500
START_X = SCREEN_WIDTH//2-10
START_Y = SCREEN_HEIGHT-80

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Game")

bg = pygame.image.load("sprites/bg.jpg")
bg = pygame.transform.scale(bg, (bg.get_width()*SCREEN_HEIGHT/bg.get_height(),SCREEN_HEIGHT))
player = Player(screen, START_X, START_Y)
camera = Camera(player)

blocks = [Block(screen, START_X-75, player.rect.bottom)] 

while(blocks[-1].rect.y>0):
    blocks.append(Block(screen, randint(0, SCREEN_WIDTH), blocks[-1].rect.y-100))
    if (blocks[-1].rect.left<0):
        blocks.append(Block(screen, blocks[-1].rect.x+SCREEN_WIDTH, blocks[-1].rect.y))
    elif (blocks[-1].rect.right>SCREEN_WIDTH):
        blocks.append(Block(screen, blocks[-1].rect.x-SCREEN_WIDTH, blocks[-1].rect.y))


def stop_falling():
    for block in blocks:
        if check_collison_top(player.rect,player.p_rect,block.rect):
            player.stopY(block.rect.top)  
            camera.updatePosition(player.rect.bottom)       
            break

def redraw():
    screen.blit(bg, (0,0))
    player.update()  
    camera.update()
    stop_falling()
    for block in blocks:
        block.draw(camera.height)
    player.draw(camera.height)
    pygame.display.update()

def checkBorder():
    for block in blocks:
        if(block.rect.top+camera.height>SCREEN_HEIGHT):
            blocks.remove(block)

clock=pygame.time.Clock()
while(True):
    control.events()
    control.movements(player)

    player.jump() 
    redraw()
    checkBorder()

    clock.tick(30)
