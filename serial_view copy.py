import pygame
import serial
import numpy as np
import sys

serialPort = serial.Serial(
    port="COM5", baudrate=9600, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE
)
pygame.init()

maxLen=800
epsilon = 30
xStep=1
hold=9
arr = [[0],[0]]
sd = [0,0]
channel=0
zeroHeight = [120,360]
colors = [(0,255,0),(255,0,255)]

screen = pygame.display.set_mode(((maxLen+1)*xStep,480))
pygame.display.set_caption("Graph")


clock=pygame.time.Clock()
while(1):
    clock.tick(30)
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
    while serialPort.in_waiting > 0:  
        signal= serialPort.read(1)
        if(ord(signal)==255): 
            channel=0
        else: 
            arr[channel].append(ord(signal)-100) 
            channel+=1
    serialPort.flush()
    screen.fill((255,255,255))
                    
    for j in range(len(arr)):
        if(len(arr[j])>maxLen):
            arr[j]=arr[j][-maxLen:]
        if(len(arr[j])>=epsilon):
            sd[j] = np.std(arr[j][-epsilon:])
        else:
            sd[j] = np.std(arr[j])
        if(sd[j]<hold):
            sd[j] = 0  
        for i in range(len(arr[j])-1):
            pygame.draw.line(screen, colors[j], (xStep*i,zeroHeight[j]-arr[j][i]), (xStep*(i+1),zeroHeight[j]-arr[j][i+1]))
        pygame.draw.line(screen, colors[-j-1], (0,zeroHeight[j]-sd[j]), (screen.get_width(),zeroHeight[j]-sd[j]))
    pygame.display.update()   