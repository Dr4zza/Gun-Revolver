import pygame
import math
from PIL import Image
import particlepy

pygame.init()
pygame.mixer.init()
pygame.mixer.music.set_volume(0.7)
screen = pygame.display.set_mode((1000,600)) # Creates a window
pygame.display.set_caption('Gun Revolver') # sets a title of the window
clock = pygame.time.Clock() # a variable to set the fps
game_active = False
player_gravity = 0
enemy_gravity = 0
angle = 0
moving = False
gun_inactive = False
shot = False
collision = False
score = 0
player_health = 10

player_surf = pygame.image.load('graphics/player.png').convert_alpha()
player_rect = player_surf.get_rect(topright = (200,300))

gun_surf = pygame.image.load('graphics/gun.png').convert_alpha()
gun_rect = gun_surf.get_rect(center = player_rect.center)

bullet_surf = pygame.image.load('graphics/bullet.png').convert_alpha()
bullet_rect = bullet_surf.get_rect(center = gun_rect.center)

sky_surface = pygame.image.load('graphics/Sky.png').convert_alpha()

ground_surface = pygame.image.load('graphics/ground.png').convert_alpha()
ground_rect = ground_surface.get_rect()

enemy_surface = pygame.image.load('graphics/enemy.png').convert_alpha()
enemy_rect = enemy_surface.get_rect()

pistol_surf = pygame.image.load('graphics/pistol.png').convert_alpha()
pistol_rect = pistol_surf.get_rect()

shootparticle_surf = pygame.image.load('graphics/shootingparticle.png').convert_alpha()
shootparticle_rect = shootparticle_surf.get_rect()

text_font = pygame.font.Font('graphics/PixelType.ttf', 50)

reload_surf = pygame.image.load('graphics/reload.png').convert_alpha()

title_surf = pygame.image.load('graphics/title.png').convert_alpha()

playbutton_surf = pygame.image.load('graphics/playbutton.png').convert_alpha()

gameover_surf = pygame.image.load('graphics/gameover.png').convert_alpha()

replay_surf = pygame.image.load('graphics/restart.png').convert_alpha()

class Player():
    def playergravity():
        global player_gravity
        if moving == False:
            player_gravity += 1
            player_rect.y += player_gravity
        if player_rect.bottom >= 550: player_rect.bottom = 550
        if player_rect.top <= 0: player_rect.top = 0
        screen.blit(player_surf, player_rect)

    def playerfriction():
        global player_gravity, collision
        if player_rect.left <= 0: player_rect.left = 0
        if player_rect.right >= 1000: player_rect.right = 1000
        screen.blit(player_surf, player_rect)
    
    def healthbar():
        pygame.draw.rect(screen, (255,0,0), (10, 10, 120, 20))
        pygame.draw.rect(screen, (0,128,0), (10, 10, 120 - (5 * (10 - player_health)), 20))

class gun():
    def gunrotate():
        global gun_rect, gun_inactive, player_gravity
        pos = pygame.mouse.get_pos()
        angle = 360-math.atan2(pos[1]-player_rect.centery,pos[0]-player_rect.centerx)*180/math.pi
        #if angle < 345 and angle > 194:
            #if str(angle)[0] == "3":
                #gun_inactive = True
                #rotimg = pygame.transform.rotate(gun_surf, 345)
                #rects = rotimg.get_rect(center = player_rect.center)
                #screen.blit(rotimg, rects)
                #return
            #else:
                #gun_inactive = True
                #rotimg = pygame.transform.rotate(gun_surf, 194)
                #rects = rotimg.get_rect(center = player_rect.center)
                #screen.blit(rotimg, rects)
                #return
        #else:
        gun_inactive = False
        rotimg = pygame.transform.rotate(gun_surf, angle)
        rects = rotimg.get_rect(center = player_rect.center)
        screen.blit(rotimg, rects)
        return angle


class Bullet():
    def __init__(self, x, y):
        self.pos = (x, y)
        mx, my = pygame.mouse.get_pos()
        self.dir = (mx - x, my - y)
        length = math.hypot(*self.dir)
        if length == 0.0:
            self.dir = (0, -1)
        else:
            self.dir = (self.dir[0]/length, self.dir[1]/length)
        angle = math.degrees(math.atan2(-self.dir[1], self.dir[0]))-10

        self.bullet = bullet_surf
        self.rect = bullet_surf.get_rect()
        self.bullet = pygame.transform.rotate(self.bullet, angle)
        self.speed = 10

    def update(self):
        global direction
        self.pos = (self.pos[0]+self.dir[0]*self.speed, 
                    self.pos[1]+self.dir[1]*self.speed)
        direction = self.dir
        return self.dir 

    def draw(self, surf):
        bullet_rect = self.bullet.get_rect(center = (self.pos[0], self.pos[1]))
        self.rect = bullet_rect
        surf.blit(self.bullet, bullet_rect) 

class Enemy:
    def __init__ (self, x, y):
        global collision
        self.life = 2
        self.pos = (x,y)
        self.player = player_rect.bottomright
        self.dir = (self.player[0] - x, self.player[1] - y)
        length = math.hypot(*self.dir)
        if length == 0.0:
            self.dir = (0, -1)
        else:
            self.dir = (self.dir[0]/length, self.dir[1]/length)
        self.enemy = enemy_surface
        self.rect = self.enemy.get_rect(center = (self.pos[0],self.pos[1]))

    def data():
        ppos = player_rect.center

    def update(self):
        global enemy_gravity, collision, player_gravity
        self.pos = self.rect
        enemy_gravity += 1
        self.rect.y += enemy_gravity
        if self.rect.bottom >= 550: self.rect.bottom = 550
        if self.rect.top <= 0: self.rect.top = 0
        if self.rect.left <= 0: 
            self.dir = list(self.dir)
            self.dir[0] = self.dir[0]*-1
            self.dir = tuple(self.dir)
        if self.rect.right >= 1000: 
            self.dir = list(self.dir)
            self.dir[0] = self.dir[0]*-1
            self.dir = tuple(self.dir)

        if self.rect.collidepoint(player_rect.topleft):
            self.rect.topright = player_rect.topleft
            collision = True
        
        elif self.rect.collidepoint(player_rect.topright):
            self.rect.topleft = player_rect.topright
            collision = True

        elif player_rect.collidepoint(self.rect.midtop): 
            player_rect.midbottom = (player_rect.midtop[0],self.rect.top)
            player_gravity = 0

            if str(direction[0]*-1)[1] != "-":
                collision = False
            else:
                collision = True
        else:
            collision = False
        
        if collision == False:
            self.rect.x = (self.rect[0]+self.dir[0]*5)

    def gunrotate_enemy(self):
        global ppos
        ppos = player_rect.center
        angle = (360-math.atan2(ppos[1]-self.rect.centery,ppos[0]-self.rect.centerx)*180/math.pi)-10
        rotimg = pygame.transform.rotate(pistol_surf, angle)
        rects = rotimg.get_rect(center = self.rect.center)
        screen.blit(rotimg, rects)
    

    def draw(self, surf):
        surf.blit(self.enemy,self.rect)

class EnemyBullet():
    def __init__(self, x, y):
        self.pos = (x, y)
        mx, my = player_rect.center
        self.dir = (mx - x, my - y)
        length = math.hypot(*self.dir)
        if length == 0.0:
            self.dir = (0, -1)
        else:
            self.dir = (self.dir[0]/length, self.dir[1]/length)
        angle = math.degrees(math.atan2(-self.dir[1], self.dir[0]))

        self.bullet = bullet_surf
        self.bullet = pygame.transform.rotate(self.bullet, angle)
        self.speed = 8 

    def update(self):
        global direction
        self.pos = (self.pos[0]+self.dir[0]*self.speed, 
                    self.pos[1]+self.dir[1]*self.speed)
        direction = self.dir
        return self.dir
        
    def draw(self, surf):
        bullet_rect = self.bullet.get_rect(center = (self.pos[0], self.pos[1]))
        surf.blit(self.bullet, bullet_rect)

class particles():
    def __init__(self, x, y):
        self.rect = pygame.draw.rect(screen,(145,145,145),(x,y,1000,1000))

class menu():
    def __init__(self):
        global game_active, score
        self.title_rect = title_surf.get_rect(center = (500,200))
        self.title_surf = title_surf
        self.button_surf = playbutton_surf
        self.button_rect = playbutton_surf.get_rect(center = (500,400))
        self.game_over = gameover_surf
        self.game_over_rect = gameover_surf.get_rect(center = (500,300))
        self.restart_surf = replay_surf
        self.restart_rect = replay_surf.get_rect(center = (600,400))
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,550))

        mouse_pos = pygame.mouse.get_pos()
        
        if score == 0:
            if self.title_rect.collidepoint(mouse_pos):
                transformed = pygame.transform.scale(title_surf,(613,173)).convert_alpha()
                transformed_rect = transformed.get_rect(center = (500,200))
                screen.blit(transformed, transformed_rect)
                screen.blit(self.button_surf, self.button_rect)

            elif self.button_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0] == False:
                transformed = pygame.transform.scale(playbutton_surf, (311, 94)).convert_alpha()
                transformed_rect = transformed.get_rect(center = (500,400))
                screen.blit(self.title_surf,self.title_rect)
                screen.blit(transformed, transformed_rect)

            elif pygame.mouse.get_pressed()[0] == True and self.button_rect.collidepoint(mouse_pos):
                transformed = pygame.transform.scale(playbutton_surf,(207,62)).convert_alpha()
                transformed_rect = transformed.get_rect(center = (500,400))
                screen.blit(self.title_surf,self.title_rect)
                screen.blit(transformed,transformed_rect)
                game_active = True
                
            else:
                screen.blit(self.title_surf,self.title_rect)
                screen.blit(self.button_surf, self.button_rect)
        
        else:
            if self.restart_rect.collidepoint(mouse_pos):
                transformed = pygame.transform.scale(replay_surf, (100,100)).convert_alpha()
                transformed_rect = transformed.get_rect(center = (600,400))
                screen.blit(self.game_over, self.game_over_rect)
                screen.blit(transformed,transformed_rect)
                screen.blit(text_font.render(f"Score: {str(score)}", False, "Black"),(415,300))
                if pygame.mouse.get_pressed()[0] == True:
                    score = 0
                    game_active = True
            else:
                screen.blit(self.game_over, self.game_over_rect)
                screen.blit(self.restart_surf, self.restart_rect)
                screen.blit(text_font.render(f"Score: {str(score)}", False, "Black"),(415,300))