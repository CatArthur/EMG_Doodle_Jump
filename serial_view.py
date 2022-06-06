import pygame
import serial
import control
import numpy as np

serialPort = serial.Serial(
    port="COM5", baudrate=9600, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE
)

maxLen=800
epsilon = 50
xStep=1
hold=9

pygame.init()
screen = pygame.display.set_mode(((maxLen+1)*xStep,480))
pygame.display.set_caption("Game")

arr = [[],[]]
sd = [[],[]]
zeroHeight = [120,360]
colors = [(0,255,0),(255,0,255)]

def update():
    global arr
    screen.fill((255,255,255))
    for j in range(len(arr)):
        if(len(arr[j])>maxLen):
            arr[j]=arr[j][-maxLen:]
        if(len(sd[j])>maxLen):
            sd[j]=sd[j][-maxLen:]
        for i in range(len(arr[j])-1):
            pygame.draw.line(screen, colors[j], (xStep*i,zeroHeight[j]-arr[j][i]), (xStep*(i+1),zeroHeight[j]-arr[j][i+1]))
        for i in range(len(sd[j])-1):
            pygame.draw.line(screen, colors[-j-1], (xStep*i,zeroHeight[j]-sd[j][i]), (xStep*(i+1),zeroHeight[j]-sd[j][i+1]))
    pygame.display.update()    


clock=pygame.time.Clock()
while(1):
    clock.tick(30)
    control.events()
    while serialPort.in_waiting > 0:  
        signal= serialPort.read(1)
        while(ord(signal)!=255): 
            signal=serialPort.read(1)
        for i in range(len(arr)):
            arr[i].append(ord(serialPort.read(1))-100) 
            if(len(arr[i])>=epsilon):
                sd[i].append(np.std(arr[i][-epsilon:]))
                if(sd[i][-1]<hold):
                    sd[i][-1]=0
            #print(np.std(arr[i][-epsilon:]))
    update()    