import pygame
import random
import time
#from replit import audio
from pygame import mixer

class Dog:
    def __init__(self, x, y):
        self.surf = pygame.image.load("img/dog.png").convert_alpha()
        self.x = x
        self.y = y
        self.rect = self.surf.get_rect(center=(self.x, self.y))
        self.anime = False
        self.direction = "UP"

    def draw(self, screen):
        screen.blit(self.surf, self.rect)

    def update(self, counter):
        if self.anime:
            if self.direction == "UP":
                if counter % 5 == 0:
                    self.y -= 20
                if counter % 7 == 0:
                    self.y += 10
                if self.rect.top <= HEIGHT - 130:
                    self.direction = "DOWN"
            elif self.direction == "DOWN":
                if counter % 5 == 0:
                    self.y += 20
                if counter % 7 == 0:
                    self.y -= 10
                if self.rect.top > HEIGHT:
                    self.anime = False
                    self.y = HEIGHT + 130
                    self.direction = "UP"
            self.rect = self.surf.get_rect(center=(self.x, self.y))

pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Chicken Hunt")
WIDTH=800
HEIGHT=600
screen=pygame.display.set_mode((WIDTH,HEIGHT))
BG=pygame.image.load("img/dh-background.png").convert_alpha()
WHITE=(255,255,255)
clock=pygame.time.Clock()

#csirkék
ALT=-7
chick=pygame.image.load("img/chicken.png").convert_alpha()
chick_rect=chick.get_rect(center=(random.randint(50,WIDTH-50),random.randint(50,HEIGHT-50)))

#célkereszt
crosshair_surf=pygame.image.load("img/crosshair.png").convert_alpha()
crosshair_rect=crosshair_surf.get_rect(center=(WIDTH/2,HEIGHT/2))

#text
points=0
FONT_COLOR=(255,255,255)
game_font=pygame.font.SysFont('arial',30, bold=True, italic=False)
text=("POINTS: " + str(points))
text_surf=game_font.render(text,True,FONT_COLOR)
text_rect=text_surf.get_rect(topright=(WIDTH-10,10))

#kutya
dog = Dog(WIDTH/2, HEIGHT+130)
dogSmile=False

#ammo
ammo=4
ammo0=pygame.image.load("img/ammo0.png").convert_alpha()
ammo1=pygame.image.load("img/ammo1.png").convert_alpha()
ammo2=pygame.image.load("img/ammo2.png").convert_alpha()
ammo3=pygame.image.load("img/ammo3.png").convert_alpha()
ammo4=pygame.image.load("img/ammo4.png").convert_alpha()
ammo_surf=[ammo0,ammo1,ammo2,ammo3,ammo4]
ammo_rect=ammo_surf[ammo].get_rect(bottomleft=(5,HEIGHT-5))

#hangok
shot=pygame.mixer.Sound("sound/shot.mp3")
shot.set_volume(0.5)
reload=pygame.mixer.Sound("sound/reload.mp3")
reload.set_volume(0.5)
#shot=audio.play_file("Pygame/sound/shot.mp3")

'''
def sound(name):
    name=audio.play_file(f"Pygame/sound/{name}.mp3")
'''

#FUTTATÁS
running=True
counter=0
katt=0
fire=True
played=False
while running:
    counter+=1
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False

        #MOZGATÁS ÉS LÖVÉS
        if event.type==pygame.MOUSEMOTION:
            crosshair_rect=crosshair_surf.get_rect(center=event.pos)

        if event.type==pygame.MOUSEBUTTONDOWN and fire and ammo>0:
            screen.fill(WHITE)
            pygame.display.flip()
            time.sleep(0.1)
            katt+=1
            ammo-=1
            dogSmile=True
            #sound("shot")
            shot.play()
            #audio.play_file("Pygame/sound/shot.mp3")
          
            
            if chick_rect.collidepoint(event.pos):
                    katt=0
                    dogSmile=False
                    points+=1
                    text=("Points: " + str(points))
                    text_surf=game_font.render(text,True,FONT_COLOR)
                    chick_rect=chick.get_rect(center=(random.randint(50,WIDTH-50),random.randint(50,HEIGHT-50)))

    #GRAFIKA      
    screen.blit(BG, (0,0))
    screen.blit(ammo_surf[ammo],ammo_rect)
    if ammo>0:
        played=False
    if ammo==0:
        fire=False
        pygame.display.flip()
        #time.sleep(1.4)
        if not played:
            reload.play()
            played=True
        if counter%200==0:
            fire=True
            ammo=4

    screen.blit(chick,chick_rect)
    if points%3==1:
        if counter%8==0:
            chick_rect.left-=ALT
        if counter%35==0:
            ALT*=(-1)
    else:
        if counter%8==0:
            chick_rect.top-=ALT
        if counter%35==0:
            ALT*=(-1)
        
    screen.blit(text_surf,text_rect)
    screen.blit(crosshair_surf,crosshair_rect)

    dog.update(counter)
    dog.draw(screen)
    if katt==3 and dogSmile:
        dog.anime = True
        katt=0
        dogSmile=False
            
    pygame.display.update()
    clock.tick(60)
pygame.quit()
