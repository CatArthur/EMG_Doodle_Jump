import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, screen,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.screen=screen
        self.screen_rect=screen.get_rect()

        self.ground_sprites = [[pygame.image.load("assets/sprites/player.png"), pygame.image.load("assets/sprites/run.png")],[None,None],[None,None]]
        self.ground_sprites[0] = [pygame.transform.scale(sprite, (64,64)) for sprite in self.ground_sprites[0]]
        self.ground_sprites[1] = self.ground_sprites[0]
        self.ground_sprites[-1] = [pygame.transform.flip(sprite, 1, 0) for sprite in self.ground_sprites[0]]

        self.jump_sprites = [[pygame.image.load("assets/sprites/player.png"), pygame.image.load("assets/sprites/jump_side.png")],[None,None],[None,None]]
        #self.jump_sprites = [[pygame.image.load("assets/sprites/jump.png"), pygame.image.load("assets/sprites/jump_side.png")],[None,None],[None,None]]
        self.jump_sprites[0] = [pygame.transform.scale(sprite, (64,64)) for sprite in self.jump_sprites[0]]
        self.jump_sprites[1] = self.jump_sprites[0]
        self.jump_sprites[-1] = [pygame.transform.flip(sprite, 1, 0) for sprite in self.jump_sprites[0]]
        self.image=self.ground_sprites[0][0]
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect.width=20
        self.rect.height=42
        self.x_shift = -22
        self.y_shift = -20
        self.p_rect = self.rect.copy()

        self.change_x=0
        self.change_y=0
        self.isJump=False
        self.hasGround=False
        self.side=0
   
        self.jumpPower = 26  ## 24 1   26 2   32 3  
        self.garvity = 2
        
    def jump(self):
        if(self.hasGround):
            self.hasGround=False
            self.change_y=-self.jumpPower

    def stopY(self,bottom):
        self.rect.bottom=bottom
        self.change_y=self.garvity
        self.hasGround=True

    def move(self,side,speed):
        self.change_x = side*speed
        self.side=side

    def update_image(self):
        if(self.side==1)|(self.side==-1):
            self.ground_sprites[0]=self.ground_sprites[self.side]
            self.jump_sprites[0]=self.jump_sprites[self.side]
        self.image=self.ground_sprites[0][abs(self.side)] if self.hasGround else self.jump_sprites[0][abs(self.side)]

    def update(self):
        if not self.hasGround :
            self.change_y+=self.garvity
        self.update_image()  
        self.p_rect = self.rect.copy() 

        self.rect.x+=self.change_x
        self.rect.y+=self.change_y
        self.change_x=0
        self.side=0
        if(self.rect.centerx>self.screen_rect.right):
            self.rect.centerx=self.screen_rect.left       
        if(self.rect.centerx<self.screen_rect.left):
            self.rect.centerx=self.screen_rect.right

    def draw(self, camera_height):    
        self.screen.blit(self.image, (self.rect.x+self.x_shift,self.rect.y+self.y_shift+camera_height))
        if(self.rect.left<self.screen_rect.left):
            self.screen.blit(self.image, (self.rect.x+self.x_shift+self.screen_rect.width,self.rect.y+self.y_shift+camera_height))
        elif(self.rect.right>self.screen_rect.right):
            self.screen.blit(self.image, (self.rect.x+self.x_shift-self.screen_rect.width,self.rect.y+self.y_shift+camera_height))
        #pygame.draw.rect(self.screen, (0,255,255), pygame.Rect(self.rect.x, self.rect.y+camera_height, self.rect.width, self.rect.height),1)
             
    