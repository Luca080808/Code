import pygame 
import random
import numpy
import math
from pygame import mixer 

# Intialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# Background

background = pygame.image.load('Universe.jpg')

#Background Sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption("Lotus-flower")
icon = pygame.image.load('lotus-flower.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('launch.png')
playerX = 370 
playerY = 480
playerX_change = 0
# Ghost 
ghostImg = []
ghostX = []
ghostY = []
ghostX_change = []
ghostY_change = []
num_of_ghosts = 6

for i in range(num_of_ghosts):
    ghostImg.append(pygame.image.load('ghost1.png')) 
    ghostX.append(random.randint(0,735))
    ghostY.append(random.randint(50,150))
    ghostX_change.append(4)
    ghostY_change.append(40)
# Bullet
#Ready - You can't see the bullet on the screen
#Fire - the bullet is currently moving

bulletImg = pygame.image.load('bullet1.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10

bullet_state = 'ready'
#Score
score = 0
score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)

textX = 10
textY = 10

#Game Over Text
over_font = pygame.font.Font('freesansbold.ttf',64)



def show_score(x,y):
    score = font.render('Score :' +  str(score_value), True, (255,255,255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render('GAME OVER ' +  str(score_value), True, (255,255,255))
    screen.blit(over_text, (200, 250))

def player(x, y):
    screen.blit(playerImg, (x, y))
    

def ghost(x, y,i):
    screen.blit(ghostImg[i], (x, y))
    
def fire_bullet(x,y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (x + 16 ,y + 10))
    
    
def isCollision(ghostX,ghostY,bulletX,bulletY):
    distance = math.sqrt(math.pow(ghostX - bulletX,2)) + (math.pow(ghostY-bulletY,2))
    if distance < 27:
        return True
    else:
        return False
    
# Game Loop
running = True
while running:

    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0))
    #background image
    screen.blit(background,(0,0))
    
    # Background Image
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -2
            if event.key == pygame.K_RIGHT:
                playerX_change = 2          
            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    bullet_Sound = mixer.Sound('laser.wav')
                    bullet_Sound.play()
                    #Get the current x coordinate of spaceship
                    
                    bulletX = playerX
                    fire_bullet(bulletX,bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # 5 = 5 + -0.1 -> 5 = 5 - 0.1
    # 5 = 5 + 0.1
    # Checking the boundaries of spaceship 
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX > 736:
        playerX - 736
    # Ghost Movement 
    for i in range(num_of_ghosts): 
        
        #Game Over
        if ghostY[i]  > 440:
            for j in range(num_of_ghosts):
                ghostY[j] = 2000
            game_over_text()
            break
            
        ghostX[i] += ghostX_change[i]
        if ghostX[i] <= 0:
            ghostX_change[i] = 0.5
            ghostY[i] += ghostY_change[i]
        elif ghostX[i] > 736:
            ghostX_change[i] =- 0.5
            ghostY[i] += ghostY_change[i]
      # Collision 
        collision = isCollision(ghostX[i], ghostY[i], bulletX, bulletY)
        if collision:
          explosion_Sound = mixer.Sound('explosion.wav')
          explosion_Sound.play()
          bulletY = 480
          bullet_state = 'ready'
          score_value += 1
          ghostX[i] = random.randint(0,735)
          ghostY[i] = random.randint(50,150)
        
        ghost(ghostX[i],ghostY[i],i)
        
    #Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = 'ready'
        
    if bullet_state == 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
        
    player(playerX, playerY)
    show_score(textX,textY)
    pygame.display.update()
   