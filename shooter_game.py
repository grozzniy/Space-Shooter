from pygame import *
from random import randint
from time import time as timer
win_width = 700
win_height = 500
w = display.set_mode((win_width, win_height))
display.set_caption('Шутер')
background = transform.scale(image.load('galaxy.jpg'),(win_width,win_height))
bullets = sprite.Group()
class GameSprite(sprite.Sprite):
    def __init__ (self,player_image,player_x,player_y,size_x,size_y,player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        w.blit(self.image, (self.rect.x,self.rect.y))
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x>0:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x<630:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png',self.rect.centerx,self.rect.top,5,10,10)
        fire_sound.play()
        bullets.add(bullet)
        
lambda parameter_list: expression
lost = 0
score = 10
win = 0
life = 3
num_fire = 0
rel_time = False
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost += 1
class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed



font.init()
font1 = font.SysFont('Georgia',36)
player = Player('rocket.png', 5, win_height - 100, 80, 100, 10)
enemies = sprite.Group()
for i in range(1, 6):
    enemy = Enemy("ufo.png", randint(80, win_width - 80), -40, 80, 50, 1)
    enemies.add(enemy)
asteroids = sprite.Group()
for i in range(1, 3):
    asteroid = Asteroid("asteroid.png", randint(80, win_width - 80), -40, randint(50,75), randint(50,75), 1)
    asteroids.add(asteroid)
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
FPS = time.Clock()
finish = False
game = True
while game == True:
    
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 10 and rel_time == False:
                    num_fire = num_fire + 1
                    fire_sound.play()
                    player.fire()
                if num_fire >= 10 and rel_time == False:
                    last_time = timer()
                    rel_time = True 
                    

    if not finish:
        w.blit(background,(0,0))
        
        text_life = font1.render("Здоровье:"+ str(life), True, (255,255,255))
        text_lose = font1.render("Пропущено:"+ str(lost), True, (255,255,255))
        text_win = font1.render("Счет:"+ str(win), True, (255,255,255))
        finish_text = font1.render("Победа!", True, (0,154,0))
        badfin_text = font1.render("Поражение!", True, (255,0,0))        

        player.reset()
        player.update()
        enemies.draw(w)
        enemies.update()
        asteroids.draw(w)
        asteroids.update()
        bullets.draw(w)
        bullets.update()
        display.update()

        w.blit(text_life, (0,0))
        w.blit(text_lose,(0,50))
        w.blit(text_win,(0,25))

        if rel_time == True:
            now_time = timer()

            if now_time - last_time < 2:
                text_reload = text_reload = font1.render("ПЕРЕЗАРЯДКА", True, (255,0,0))
                w.blit(text_reload, (260, 460))
            else: 
                num_fire = 0
                rel_time = False
        collides = sprite.groupcollide(enemies, bullets, True, True)
        for i in collides:
            win += 1
            enemy = Enemy("ufo.png", randint(80, win_width - 80), -40, 80, 50, 1)
            enemies.add(enemy)

        if sprite.spritecollide(player, asteroids, True):
            life -= 1
            asteroid = Asteroid("asteroid.png", randint(80, win_width - 80), -40, randint(50,75), randint(50,75), 2)
            asteroids.add(asteroid)
        if win >= score:
            w.blit(finish_text, (250,250))
            finish = True
        if lost >= 3 or life <= 0:
            w.blit(badfin_text, (250,250))
            finish = True
    display.update()        
    FPS.tick(60)