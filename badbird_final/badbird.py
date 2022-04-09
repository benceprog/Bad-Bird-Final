import pygame
import os
import random
import time
import ctypes

taskbaricon = 'bird.png'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(taskbaricon)

from pygame import mixer

os.system('cls')

WIDTH, HEIGHT = 1280, 720

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Bad Bird')

FPS = 60

VEL = 6

WHITE = (255, 255, 255)
        
PLAYER = pygame.Rect(298, 300, 50, 50)

BIRD = pygame.image.load('bird.png')
BIRD_MOD = pygame.transform.scale(BIRD, (50, 50))

pygame.display.set_icon(BIRD_MOD)

BLOCK_TEXTURE = pygame.image.load('block.png')

BACKGROUND = pygame.image.load('cloud.png')

def bacgkroundMusic():
    pygame.mixer.init()
    mixer.music.load('music.wav')
    mixer.music.play()

bacgkroundMusic()

def newBLock():
    calculate_BLOCK_UP_HEIGHT =  random.randint(1, 10)
    if calculate_BLOCK_UP_HEIGHT == 1:
        calculate_BLOCK_UP_HEIGHT = 100
    elif calculate_BLOCK_UP_HEIGHT == 2:
        calculate_BLOCK_UP_HEIGHT = 200 
    elif calculate_BLOCK_UP_HEIGHT == 3:
        calculate_BLOCK_UP_HEIGHT = 300
    elif calculate_BLOCK_UP_HEIGHT == 4:
        calculate_BLOCK_UP_HEIGHT = 400
    elif calculate_BLOCK_UP_HEIGHT == 5:
        calculate_BLOCK_UP_HEIGHT = 500
    elif calculate_BLOCK_UP_HEIGHT == 6:   
        calculate_BLOCK_UP_HEIGHT = 150
    elif calculate_BLOCK_UP_HEIGHT == 7:
        calculate_BLOCK_UP_HEIGHT = 250
    elif calculate_BLOCK_UP_HEIGHT == 8:
        calculate_BLOCK_UP_HEIGHT = 350
    elif calculate_BLOCK_UP_HEIGHT == 9:
        calculate_BLOCK_UP_HEIGHT = 450
    elif calculate_BLOCK_UP_HEIGHT == 10:
        calculate_BLOCK_UP_HEIGHT = 550

    global BLOCK_UP_HEIGHT

    BLOCK_UP_HEIGHT = calculate_BLOCK_UP_HEIGHT
    BLOCK_BOTTOM_HEIGHT = HEIGHT - calculate_BLOCK_UP_HEIGHT
    BLOCK_BOTTOM_HEIGHT = BLOCK_BOTTOM_HEIGHT - 100

    global BLOCK_UP
    global BLOCK_BOTTOM

    BLOCK_UP = pygame.Rect(1000, 0, 50, BLOCK_UP_HEIGHT)
    BLOCK_BOTTOM = pygame.Rect(1000, HEIGHT - BLOCK_BOTTOM_HEIGHT, 50, BLOCK_BOTTOM_HEIGHT + 25)

    global BLOCK_TEXTURE_MOD_01
    global BLOCK_TEXTURE_MOD_02
    BLOCK_TEXTURE_MOD_01 = pygame.transform.rotate(pygame.transform.scale(BLOCK_TEXTURE, (50, BLOCK_UP_HEIGHT)), 180)
    BLOCK_TEXTURE_MOD_02 = pygame.transform.rotate(pygame.transform.scale(BLOCK_TEXTURE, (50, BLOCK_BOTTOM_HEIGHT + 25)), 0)


newBLock()

point = 0

def window():   
    WIN.blit(BACKGROUND, (0, 0))

    WIN.blit(BIRD_MOD, (PLAYER.x, PLAYER.y))
    WIN.blit(BLOCK_TEXTURE_MOD_01, (BLOCK_UP.x, BLOCK_UP.y))
    WIN.blit(BLOCK_TEXTURE_MOD_02, (BLOCK_BOTTOM.x, BLOCK_BOTTOM.y))

    global point

    if PLAYER.x == BLOCK_UP.x:
        point += 1


    pygame.init()
    score_font = pygame.font.SysFont('rubik', 50)
    score_text = score_font.render(f'Points: {point}', 1, (0, 0, 0))

    WIN.blit(score_text, (50, 50))

    pygame.display.update()


def block():
    BLOCK_BOTTOM.x -= VEL
    BLOCK_UP.x -= VEL

    global score_send

    if BLOCK_BOTTOM.x < 200:
        newBLock()
        pygame.mixer.init()
        mixer.music.load('effect.wav')
        mixer.music.play()

        time.sleep(0.05)

        bacgkroundMusic()

    if BLOCK_UP.x < 200:
        newBLock()

def movementPlayer():
    PLAYER.y += VEL / 2

    key_press = pygame.key.get_pressed()
    if key_press[pygame.K_SPACE] and key_press[pygame.K_LSHIFT] == False:
        PLAYER.y -= VEL

    if key_press[pygame.K_SPACE] and key_press[pygame.K_LSHIFT]:
        PLAYER.y -= VEL * 1.5
    
    if key_press[pygame.K_SPACE] and key_press[pygame.K_LCTRL]:
        PLAYER.y += VEL * 1.5
    

def endscene(deadtype):
    WIN.fill((0, 0, 0))

    endground = pygame.image.load('endground.png')

    WIN.blit(endground, (0, 0))

    global point

    pygame.init()
    score_font = pygame.font.SysFont('rubik', 50)
    if deadtype == 'wall':
        score_text = score_font.render(f'Points: {point - 1}', 1, (255, 255, 255))

    if deadtype == 'out':
        score_text = score_font.render(f'Points: {point}', 1, (255, 255, 255))

    WIN.blit(score_text, (50, 50))


    pygame.display.update()

def main():
    clock = pygame.time.Clock()
    run = True
    endgame = False
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        if PLAYER.y > 720 or PLAYER.y < 0:
            run = False
            endgame = True
            deadtype = 'out'

        if PLAYER.left == BLOCK_BOTTOM.left and PLAYER.bottom >= BLOCK_BOTTOM.top:
            run = False
            endgame = True
            deadtype = 'wall'

        if PLAYER.left == BLOCK_UP.left and PLAYER.top <= BLOCK_UP.bottom: 
            run = False
            endgame = True
            deadtype = 'wall'

        window()
        block()
        movementPlayer()
    
    while endgame:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                endgame = False
            
        endscene(deadtype)

    pygame.quit()


if __name__ == '__main__':
    main()