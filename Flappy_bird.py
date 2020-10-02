#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pygame,sys,random

pygame.init()
pygame.mixer.pre_init(frequency = 44100, size = 16, channels = 1, buffer = 512)

speed = 5
game_run = False
win_width, win_height = 476,700
window = pygame.display.set_mode((win_width, win_height))
clock = pygame.time.Clock()
pygame.display.set_caption("Flappy Bird")
gravity = 1
bird_movement=0

def draw_floor():
    window.blit(floor_surface,(floor_xpos,win_height-100))
    window.blit(floor_surface,(floor_xpos+win_width,win_height-100))

def animation():
    new_bird = pygame.transform.scale2x(bird_flaps[bird_index])
    rect = new_bird.get_rect(center = (100,bird_rect.centery))
    return new_bird,rect
    
def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= speed
    return pipes

def create_pipe():
    random_pos = random.choice([300,400,500,350,450])
    top = flipped_pipe_surface.get_rect(midbottom = (int(win_height*1.2),random_pos-200))
    bottom = pipe_surface.get_rect(midtop = (int(win_height*1.2),random_pos))
    return top,bottom

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.centerx > -win_width:
            if pipe.top>0:
                window.blit(pipe_surface,pipe)
            else:
                window.blit(flipped_pipe_surface,pipe)
        else:
            pipes.remove(pipe)

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            hit_sound.play()
            return False
        elif bird_rect.bottom >= (win_height-180) or bird_rect.top<=-12*speed:
            die_sound.play()
            return False
    return True

def score_check(pipes):
    score = 0
    for pipe in pipes[::2]:
        if pipe.centerx < 100 and pipe.centerx > 90:
            score_sound.play()
            score+=1
            break
    return score

def score_display():
    score_surface = game_font.render(str(int(score)),True,(255,255,255))
    score_rect = score_surface.get_rect(center = (win_width//2,win_height//4))
    window.blit(score_surface,score_rect)

game_font = pygame.font.Font('04B_19.ttf',40)    
bg_surface = pygame.image.load("images/background-day.png").convert()
bg_surface = pygame.transform.scale(bg_surface,(win_width,win_height))
gameover_surface = pygame.image.load("images/message.png").convert_alpha()
gameover_surface = pygame.transform.scale(gameover_surface,(win_width,win_height))
gameover_rect = gameover_surface.get_rect(center = (win_width//2,win_height//2))

floor_surface = pygame.image.load("images/base.png").convert()
floor_surface = pygame.transform.scale(floor_surface,(win_width,180))
floor_xpos = 0

bird_up = pygame.image.load("images/bluebird-upflap.png").convert_alpha()
bird_mid = pygame.image.load("images/bluebird-midflap.png").convert_alpha()
bird_down = pygame.image.load("images/bluebird-downflap.png").convert_alpha()
bird_flaps = [bird_up,bird_mid,bird_down]
bird_surface = bird_up
bird_rect = bird_surface.get_rect(center = (100,512))
BIRDSFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDSFLAP,200)
bird_index = 0

pipe_surface = pygame.image.load("images/pipe-red.png").convert_alpha()
pipe_surface = pygame.transform.scale(pipe_surface, (int(win_width*0.2),win_height))
flipped_pipe_surface = pygame.transform.flip(pipe_surface,0,True)
SWANPIPE = pygame.USEREVENT
pipes = []
pygame.time.set_timer(SWANPIPE,2200)

#sounds
flap_sound = pygame.mixer.Sound("audio/wing.wav")
hit_sound = pygame.mixer.Sound("audio/hit.wav")
die_sound = pygame.mixer.Sound("audio/die.wav")
score_sound = pygame.mixer.Sound("audio/point.wav")
score = 0
while True:
    pygame.time.delay(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == BIRDSFLAP:
            if bird_index<2:
                bird_index+=1
            else:
                bird_index=0
            bird_surface,bird_rect = animation()
        if event.type == SWANPIPE:
            pipes.extend(create_pipe())
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_run:
                bird_movement = 0
                bird_movement -= 15
                flap_sound.play()
            elif event.key == pygame.K_SPACE:
                bird_movement = 0
                score = 0
                bird_rect.center = (100,450)
                pipes.clear()
                game_run = True
    
    
    window.blit(bg_surface,(0,0))
    if game_run:
        bird_movement+=gravity
        bird_rect.centery += bird_movement
        window.blit(bird_surface,bird_rect)
        game_run = check_collision(pipes)

        pipes = move_pipes(pipes)
        draw_pipes(pipes)
        score += score_check(pipes)
        score_display()
        
    else:
        window.blit(gameover_surface,gameover_rect)
    draw_floor()
    floor_xpos-=speed
    if(floor_xpos<=-win_width):
        floor_xpos=0
    pygame.display.update()
    clock.tick(120)


# In[ ]:




