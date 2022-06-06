import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, screen,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.ground_sprites = [[pygame.image.load("sprites/player.png"), pygame.image.load("sprites/run.png")],[None,None],[None,None]]
        self.ground_sprites[0] = [pygame.transform.scale(sprite, (64,64)) for sprite in self.ground_sprites[0]]
        self.ground_sprites[1] = self.ground_sprites[0]
        self.ground_sprites[-1] = [pygame.transform.flip(sprite, 1, 0) for sprite in self.ground_sprites[0]]

        self.jump_sprites = [[pygame.image.load("sprites/jump.png"), pygame.image.load("sprites/jump_side.png")],[None,None],[None,None]]
        self.jump_sprites[0] = [pygame.transform.scale(sprite, (64,64)) for sprite in self.jump_sprites[0]]
        self.jump_sprites[1] = self.jump_sprites[0]
        self.jump_sprites[-1] = [pygame.transform.flip(sprite, 1, 0) for sprite in self.jump_sprites[0]]

        #self.jump_sprite = pygame.image.load("sprites/player.png")
        self.image=self.ground_sprites[0][0]
        self.rect = self.image.get_rect()

        self.screen=screen
        self.screen_rect=screen.get_rect()
        
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
        
        self.speed=10
        self.jumpDuration=8
        self.jumpPower = 0.9
        self.jumpCount=self.jumpDuration
        self.fallCount=0
        
    def jump(self):
        if(self.hasGround):
            self.hasGround=False
            self.isJump=True

    def jumping(self):
        if self.isJump:
            if self.jumpCount >= 0: 
                self.change_y=-int(self.jumpCount**2*self.jumpPower)
                self.jumpCount-=1
            else:
                self.fallCount=0
                self.isJump=False
                self.jumpCount=self.jumpDuration 
    
    def falling(self):
        if (not self.isJump) & (not self.hasGround):
            self.change_y=int(self.fallCount**2*self.jumpPower)
            self.fallCount+=1
        elif(self.hasGround) :
            self.change_y=0
            self.fallCount=0

    def move(self,side):
        self.change_x = side*self.speed
        self.side=side


    def update_image(self):
        if(self.side==1)|(self.side==-1):
            self.ground_sprites[0]=self.ground_sprites[self.side]
            self.jump_sprites[0]=self.jump_sprites[self.side]
        self.image=self.jump_sprites[0][abs(self.side)] if self.isJump else self.ground_sprites[0][abs(self.side)]

    def update(self):
        self.jumping()
        self.falling()
        self.update_image()  
        self.p_rect = self.rect.copy() 

        self.rect.x+=self.change_x
        self.rect.y+=self.change_y
        self.change_x=0
        self.side=0
        self.rect.left=max(self.screen_rect.left,self.rect.left)
        self.rect.right=min(self.screen_rect.right,self.rect.right)

    def draw(self):    
        self.screen.blit(self.image, (self.rect.x+self.x_shift,self.rect.y+self.y_shift))
        pygame.draw.rect(self.screen, (0,255,255), self.rect,1)
             
    