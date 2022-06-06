class Camera(object):
    def __init__(self, player):
        self.start = player.rect.bottom
        self.height = 0
        self.targetHeight = 0
        self.steps = 4
	
    def updatePosition(self, newHeight):
        self.targetHeight=self.start-newHeight

    def update(self):
        if(self.height<self.targetHeight):
            self.height += (self.targetHeight-self.height)//self.steps
        
