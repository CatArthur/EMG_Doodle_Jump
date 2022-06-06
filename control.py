import pygame
import sys
import serial
import numpy as np

pygame.init()

EPSILON = 50
HOLD=9
RESTART_TIME = 2.8

dead=False
serialPort = None
arr = [[0],[0]]
sd = [0,0]
channel=0
restartTimer=0

def initSerial():
    global arr,sd
    serialPort = serial.Serial(port="COM5", baudrate=9600, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
    arr = [[0],[0]]
    sd = [0,0]
    serialPort.flush()

def events():
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

def movements(player):
    if(sd[0]>sd[1]):
        player.move(-1,sd[0]) 
    elif(sd[0]<sd[1]): 
        player.move(1,sd[1]) 
    keys=pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move(-1,10)
    if keys[pygame.K_RIGHT]:
        player.move(1,10)
    if keys[pygame.K_SPACE]:
        player.jump() 
 

def updateRestartTime(fps):
    global restartTimer
    restartTimer -= 1/fps
    if(restartTimer<=0):
        restartTimer=0 
    if pygame.key.get_pressed()[pygame.K_SPACE]:
        restartTimer=0 

def death():
    global dead, restartTimer
    dead = True
    restartTimer = RESTART_TIME           

def updateSerial():
    global channel

    while serialPort.in_waiting > 0:  
        signal= serialPort.read(1)
        if(ord(signal)==255): 
            channel=0
        else: 
            arr[channel].append(ord(signal)-100) 
            channel+=1
    serialPort.flush()
                    
    for j in range(len(arr)):
        if(len(arr[j])>EPSILON):
            arr[j]=arr[j][-EPSILON:]
        sd[j] = np.std(arr[j])
        if(sd[j]<HOLD):
            sd[j] = 0   