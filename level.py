import pygame
from random import randint
from collisions import check_collison_top
from camera import Camera
from block import Block
import control

class Level(pygame.sprite.Sprite):
    def __init__(self, screen, player):
        self.player = player
        self.camera = Camera(player)
        self.blocks = [Block(screen, 0, player.rect.bottom)] 
        self.blocks[0].rect.centerx=player.rect.centerx
        self.screen=screen

        self.SCREEN_WIDTH = screen.get_width()
        self.SCREEN_HEIGHT = screen.get_height()
        self.generateBlocks()
        with open('maxscore.txt', 'r', encoding='utf8') as f:
            self.maxsc=int(f.readline())

    def reset(self):
        self.maxsc=self.maxscore()
        self.camera = Camera(self.player)
        self.blocks = [Block(self.screen, 0, self.player.rect.bottom)] 
        self.blocks[0].rect.centerx=self.player.rect.centerx  
        self.generateBlocks() 
        with open('maxscore.txt', 'w', encoding='utf8') as f:
            f.write(str(self.maxsc))

    def generateBlocks(self):
        while(self.blocks[-1].rect.y+self.camera.height>0):
            self.blocks.append(Block(self.screen, 
                                    self.blocks[-1].rect.x + randint(self.SCREEN_WIDTH//4, 3*self.SCREEN_WIDTH//4), 
                                    self.blocks[-1].rect.y-randint(120, 150)))
            if (self.blocks[-1].rect.left<0):
                self.blocks.append(Block(self.screen, self.blocks[-1].rect.x+self.SCREEN_WIDTH, self.blocks[-1].rect.y))
            elif (self.blocks[-1].rect.right>self.SCREEN_WIDTH):
                self.blocks.append(Block(self.screen, self.blocks[-1].rect.x-self.SCREEN_WIDTH, self.blocks[-1].rect.y))

    def stopFalling(self):
        for block in self.blocks:
            if check_collison_top(self.player.rect,self.player.p_rect,block.rect):
                self.player.stopY(block.rect.top)  
                self.camera.updatePosition(self.player.rect.bottom)       
                break

    def checkBorder(self):
        if(self.blocks[0].rect.top+self.camera.height>self.SCREEN_HEIGHT):
            self.blocks.remove(self.blocks[0])
        if(self.player.rect.top+self.camera.height>self.SCREEN_HEIGHT):
            control.death()

    def update(self):  
        self.checkBorder() 
        self.generateBlocks()
        self.player.update()  
        self.camera.update() 
        self.stopFalling() 

    def score(self):  
        return self.camera.height   

    def maxscore(self):  
        return max(self.maxsc, self.score()) 

    def draw(self):
        for block in self.blocks:
            block.draw(self.camera.height) 
        self.player.draw(self.camera.height)