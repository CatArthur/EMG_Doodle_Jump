import pygame

class Block(pygame.sprite.Sprite):
    def __init__(self, screen, x, y, width=150, height=18):
        self.image=pygame.transform.scale(pygame.image.load("assets/sprites/platform_dark.png"),(width,height))
        self.screen = screen
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


    def draw(self,camera_height):
        self.screen.blit(self.image, (self.rect.x,self.rect.y+camera_height))
        #pygame.draw.rect(self.screen, (255,0,255), pygame.Rect(self.rect.x, self.rect.y+camera_height, self.rect.width, self.rect.height),1)
