import random
import sys
from random import randrange

import pygame

pygame.init()
screen = pygame.display.set_mode((1024, 768))
clock = pygame.time.Clock()

font = pygame.font.Font('GameOfSquids.ttf',40)
background = pygame.image.load('bk5.png').convert()

flap_music = pygame.mixer.Sound('sound/coin.wav')
death_music = pygame.mixer.Sound('sound/bomb2.wav')
song_music = pygame.mixer.Sound('sound/song.wav')

pygame.display.set_caption('Squid Game')

# status
man_status, speed = 0, 1.0 ## 0 for stop, 1 for run
otherman_status = 0
light_status = 0
gameover_status = 0

man_frames, pman_green_frames, pman_red_frames, girl_frames = [], [], [], []
for i in range(1, 8):
    man_frames.append(pygame.image.load(f'red_man/man_{i}.png').convert_alpha())
    pman_green_frames.append(pygame.image.load(f'green_man/man_{i}.png').convert_alpha())
    pman_red_frames.append(pygame.image.load(f'red_man/man_{i}.png').convert_alpha())
for i in list(range(6, -1, -1))+[0]+list(range(0, 7)):
    girl_frames.append(pygame.image.load(f'girl/girl_{i}.png').convert_alpha())

# man init
man_index = 0
man_surface = man_frames[0]
man_rect = man_surface.get_rect(center = (100,700))
manFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(manFLAP, 20)
pos_x, pos_y = 100, 700

# pman init
pman_index, pman_list = 0, []
pmanFLAP = pygame.USEREVENT + 4
pygame.time.set_timer(pmanFLAP, 20)

# girl init
girl_index = 0
girl_surface = girl_frames[0]
girl_rect = girl_surface.get_rect(center = (850,100))
girlFLAP = pygame.USEREVENT + 2
pygame.time.set_timer(girlFLAP, 200)

# spawn time step
SPAWNpman = pygame.USEREVENT
pygame.time.set_timer(SPAWNpman, 1200)


def girl_animation():
	new_girl = girl_frames[girl_index]
	new_girl_rect = new_girl.get_rect(center = (girl_rect.centerx,girl_rect.centery))
	return new_girl, new_girl_rect

def man_animation():
	new_man = man_frames[man_index]
	new_man_rect = new_man.get_rect(center = (man_rect.centerx,man_rect.centery))
	return new_man, new_man_rect

def pman_animation():
    pman_green_frame = pman_green_frames[pman_index]
    pman_red_frame = pman_red_frames[pman_index]
    return pman_green_frame, pman_red_frame

def pman_stop():
    pman_green_frame = pman_green_frames[0]
    pman_red_frame = pman_red_frames[0]
    return pman_green_frame, pman_red_frame

def man_stop():
	new_man = man_frames[0]
	new_man_rect = new_man.get_rect(center = (man_rect.centerx,man_rect.centery))
	return new_man,new_man_rect

def light_display(game_state):
    if light_status == 1: score_sf = font.render("RED LIGHT",True,(255,0,0))
    else: score_sf = font.render("GREEN LIGHT",True,(0,255,0)) 
    score_rect = score_sf.get_rect(center = (180,50))
    screen.blit(score_sf,score_rect)

def gameover_display(gameover_status):
    if gameover_status == 1:
        gameover_sf = font.render("GAME OVER",True,(255,0,0))
        gameover_rect = gameover_sf.get_rect(center = (1024/2,768/2))
        screen.blit(gameover_sf,gameover_rect)

        gameover_sf = font.render("Press Space to restart",True,(255,0,0))
        gameover_rect = gameover_sf.get_rect(center = (1024/2,768/2+50))
        screen.blit(gameover_sf,gameover_rect)

    if gameover_status == 2:
        gameover_sf = font.render("YOU WIN",True,(255,0,0))
        gameover_rect = gameover_sf.get_rect(center = (1024/2,768/2))
        screen.blit(gameover_sf,gameover_rect)

        gameover_sf = font.render("Press Space to restart",True,(255,0,0))
        gameover_rect = gameover_sf.get_rect(center = (1024/2,768/2+50))
        screen.blit(gameover_sf,gameover_rect)

def move_pmans(pmans):
    for pman in pmans:
        if otherman_status == 1:
            pman[0].centerx += 2
            pman[0].centery -= 1

        if pman[0].centery < -10:
            pmans.remove(pman)
    return pmans

def create_pman():
    if gameover_status == 0:
        if random.random() < 0.5:
            new_pman = pman_green_frames[0].get_rect(center = (randrange(1024)-600,800+randrange(500)))
            pman_color = 'green'
        else:
            new_pman = pman_red_frames[0].get_rect(center = (randrange(1024)-600,800+randrange(500)))
            pman_color = 'red'
        return new_pman, pman_color

while True:
    if 5 <= girl_index <= 10:
        light_status = 1
        otherman_status = 0
    else:
        light_status = 0  
        otherman_status = 1 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                man_status = 1
                flap_music.play()
            if event.key == pygame.K_a:
                man_status = 0
                flap_music.play()
            if event.key == pygame.K_SPACE and gameover_status != 0:
                man_status = 0
                gameover_status = 0 
                pman_list = [] 
                man_rect.centerx = 100
                man_rect.centery = 700
                pos_x = 100
                pos_y = 700

        elif event.type == SPAWNpman:
            if otherman_status == 1 and gameover_status == 0:
                for num in range(8):
                    pman_list.append(create_pman())
                print(f"pile count = {len(pman_list)}")

        elif event.type == pmanFLAP:
            if pman_index < 6: pman_index += 1
            else: pman_index = 0

            if otherman_status == 1: pman_g_surface, pman_r_surface = pman_animation()
            else: pman_g_surface, pman_r_surface = pman_stop()

        elif event.type == manFLAP:
            if man_index < 6: man_index += 1
            else: man_index = 0
            if man_status == 1: man_surface,man_rect = man_animation()
            else: man_surface,man_rect = man_stop()

        elif event.type == girlFLAP:
            if gameover_status == 0:
                if girl_index < 14: girl_index += 1
                else:
                    girl_index = 0
                    song_music.play()
            girl_surface, girl_rect = girl_animation()

    if gameover_status == 0:

        screen.blit(background, (0,0))
        text_surface = font.render("Press (D) to Go, (A) Stop",True,(0,0,0))
        text_rect = text_surface.get_rect(center = (1024/2,768-50))
        screen.blit(text_surface,text_rect)
        screen.blit(man_surface, man_rect)
        screen.blit(girl_surface, girl_rect)

        pman_list = move_pmans(pman_list)

        for pman in pman_list:
            if pman[1] == 'red':
                screen.blit(pman_r_surface, pman[0])
            elif pman[1] == 'green':
                screen.blit(pman_g_surface, pman[0])

        if man_status == 1:
            pos_x = pos_x + speed
            pos_y = pos_y - speed / 2
            man_rect.centerx = pos_x
            man_rect.centery = pos_y

        if man_status == 1 and light_status == 1:
            gameover_status = 1
            death_music.play()
            gameover_display(gameover_status)

        if pos_y < 250:
            gameover_status = 2
            death_music.play()
            gameover_display(gameover_status)

        light_display('main_game')
        
    else:
        gameover_display(gameover_status)

    pygame.display.update()
    clock.tick(120)
