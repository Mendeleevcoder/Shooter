#Создай собственный Шутер!
from pygame import *
from random import randint
import sys
import os

def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    elif hasattr(sys, "_MEIPASS2"):
        return os.path.join(sys._MEIPASS2, relative_path)
    else:
        return os.path.join(os.path.abspath("."), relative_path)

image_folder = resource_path(".")

mixer.init()
font.init()

w = 700
h = 500
WHITE = (255, 255, 255)
GREEN = (0, 172, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

img_back = os.path.join(image_folder, 'galaxy.jpg')
img_hero = os.path.join(image_folder, 'rocket.png')
img_ufo = os.path.join(image_folder, 'ufo.png')
img_bullet = os.path.join(image_folder, 'bullet.png')
img_heart = os.path.join(image_folder, 'heart.png')
img_asteroid = os.path.join(image_folder, 'asteroid.png')
sound = os.path.join(image_folder, 'space.ogg')
fire_soind = os.path.join(image_folder, 'fire.ogg')

mixer.music.load(sound)
mixer.music.play()
fire_sound = mixer.Sound(fire_soind)

font1 = font.Font(None, 35)
count1 = 0
count2 = 0

font2 = font.Font(None, 50)
win = font2.render('Победа', True, GREEN)
lose = font2.render('Проигрыш', True, RED)

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
            window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < w - 60:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx - 7, self.rect.top, 15, 20, 4)
        bullets.add(bullet)


class Enemy(GameSprite):
    def update(self):
        global count2
        self.rect.y += self.speed
        if self.rect.y >= 600:
            count2 += 1
            self.rect.y = -100
            self.rect.x = randint(0, 600)

class Bullet(GameSprite):
    def update(self):
        global count1
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()    

display.set_caption('Шутер')
window = display.set_mode((w, h))
background = transform.scale(image.load(img_back), (w, h))

ship = Player(img_hero, 600, 400, 60, 80, 10)

monsters = sprite.Group()
bullets = sprite.Group()
asteroids = sprite.Group()

for i in range(5):
    monster = Enemy(img_ufo, randint(0, 600), -100, 100, 60, randint(2, 5))
    monsters.add(monster)

for i in range(2):
    asteroid = Enemy(img_asteroid, randint(0, 600), -100, 100, 60, randint(2, 3))
    asteroids.add(asteroid)

finish = False
run = True
clock = time.Clock()
FPS = 60
while run:

    if not finish:
        window.blit(background, (0, 0))

        ship.update()
        monsters.update()
        monsters.draw(window)
        asteroids.update()
        asteroids.draw(window)
        bullets.update()
        bullets.draw(window)
        ship.reset()

        c_text1 = font1.render('Счёт: '+str(count1), True, WHITE)
        c_text2 = font1  .render('Пропущено: '+str(count2), True, WHITE)
        window.blit(c_text1, (0, 0))
        window.blit(c_text2, (0, 40))

        monsters_list = sprite.spritecollide(ship, monsters, False)

        asteroid_list = sprite.spritecollide(ship, asteroids, False)

        if len(monsters_list) > 0 or len(asteroid_list) > 0:
            finish = True
            window.blit(lose, (270, 210))
            mixer.music.stop()

            

        sprites_list = sprite.groupcollide(monsters, bullets, True, True)
        for i in sprites_list:
            count1 += 1
            monster = Enemy(img_ufo, randint(0, 600), -100, 100, 60, randint(2, 5))
            monsters.add(monster)

        asteroids_list = sprite.groupcollide(asteroids, bullets, False, True)

        if count1 >= 21:
            finish = True
            window.blit(win, (300, 210))
            mixer.music.stop()
        if count2 >= 3:
            finish = True
            window.blit(lose, (270, 210))
            mixer.music.stop()

    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                ship.fire()
            if e.key == K_RETURN and finish == True:
                count1 = 0
                count2 = 0
                for i in monsters:
                    i.rect.y = -100
                for i in bullets:
                    i.kill()
                for i in asteroids:
                    i.rect.y = -100
                finish = False
                mixer.music.play()
                

    display.update()
    clock.tick(FPS)    

