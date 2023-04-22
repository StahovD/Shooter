# Створи власний Шутер!

from pygame import *
from random import randint
from time import time as timer


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)

        self.image = transform.flip(transform.scale(image.load(player_image), (size_x, size_y)), False, True)
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        # TODO Написати управління гравцем для руху в сторони (ширина гравця 80 px)
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x = self.rect.x - self.speed
        if keys[K_RIGHT] and self.rect.x < width - 85:
            self.rect.x = self.rect.x + self.speed

    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx-7,
                        self.rect.top, 10, 40, 25)
        bullets.add(bullet)


class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > height:
            self.rect.y = 0
            self.rect.x = randint(0, width-85)
            lost = lost + 1

class Meteor(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > height:
            self.rect.y = 0
            self.rect.x = randint(0, width-85)
        

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= -50:
            self.kill()


font.init()
text1 = font.SysFont("Arial", 36)
text2 = font.SysFont("Arial", 80)

# TODO Напис виграв та напис програв. Описати новий шрифт (80 px)
win = text2.render("YOU WIN!!!", True, (0, 255, 0))
lose = text2.render("YOU LOST!!!", True, (255, 0, 0))


mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()
fire_sound = mixer.Sound("sfx_laser.ogg")



img_back = "blue.png"
img_player = "Hero.png"
img_enemy = "Enemy.png"
img_bullet = "laser.png"
img_asteroid = "meteor.png"


width, height = 700, 500
window = display.set_mode((width, height))
display.set_caption("Shooter")
background = transform.scale(image.load(img_back), (width, height))

# Sprites
player = Player(img_player, 250, height-100, 100, 100, 10)

clock = time.Clock()
FPS = 25


game = True
finish = False
lost = 0
score = 0
goal = 10
max_lost = 3
rel_time = False
num_fire = 0
life = 3
level = 1
change_level = True


bullets = sprite.Group()
monsters = sprite.Group()
asteroids = sprite.Group()


while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire += 1
                    fire_sound.play()
                    player.fire()

                if num_fire >= 5 and not rel_time:
                    last_time = timer()
                    rel_time = True

    if not finish:
        window.blit(background, (0, 0))
        player.update()
        player.reset()
        monsters.update()
        monsters.draw(window)
        asteroids.update()
        asteroids.draw(window)
        bullets.update()
        bullets.draw(window)

        if change_level:
            window.fill((0,0,0))
            level_text = text2.render("Level " + str(level),1, (255,69,0))
            window.blit(level_text, (200, 200))
            display.update()
            time.delay(3000)
            if level == 1:
                for i in range(3):
                    monster = Enemy(img_enemy, randint(0, width-85), 0, 60, 60, randint(1, 5))
                    monsters.add(monster)
                change_level = False
            if level == 2:
                for i in range(5):
                    monster = Enemy(img_enemy, randint(0, width-85), 0, 60, 60, randint(1, 5))
                    monsters.add(monster)
                change_level = False
            if level == 3:
                for i in range(5):
                    monster = Enemy(img_enemy, randint(0, width-85), 0, 60, 60, randint(1, 5))
                    monsters.add(monster)
                for i in range(2):
                    asteroid = Meteor(img_asteroid, randint(
                        0, width-85), 0, 80, 80, randint(1, 3))
                    asteroids.add(asteroid)
                change_level = False
        if rel_time:
            now_time = timer()
            if now_time - last_time < 3:
                reload = text1.render("Reloading", 1, (255, 0, 0))
                window.blit(reload, ((width//2-30), height-50))
            else:
                num_fire = 0
                rel_time = False

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for coliide in collides:
            score += 1
            monster = Enemy(img_enemy, randint(0, width-85),
                            0, 60, 60, randint(1, 3))
            monsters.add(monster)

        if sprite.spritecollide(player, monsters, False) or sprite.spritecollide(player, asteroids, False):

            sprite.spritecollide(player, monsters, True)
            sprite.spritecollide(player, asteroids, True)
            life -= 1
            monster = Enemy(img_enemy, randint(0, width-85),
                            0, 60, 60, randint(1, 3))
            monsters.add(monster)


        if life == 0 or lost >= max_lost:
            level = 1
            change_level = True
            finish = True
            window.blit(lose, (200, 200))
        
        if score >= goal:
            level += 1
            change_level = True
            finish = True


        if score >= goal and level > 3:
            finish = True
            level = 1
            window.blit(win, (200, 200))


        text_score = text1.render(
            "Рахунок: "+str(score), 1, (255,165,0))
        window.blit(text_score, (10, 20))

        # TODO текст для пропущених ворогів і промалювати

        text_lost = text1.render(
            "Пропущено: "+str(lost), 1, (255,165,0))
        window.blit(text_lost, (10, 50))

        text_life = text2.render(str(life), 1, (255,165,0))
        window.blit(text_life, (width-100, 10))

        display.update()
    else:
        finish = False
        score = 0
        lost = 0
        num_fire = 0
        life = 3
        for bullet in bullets:
            bullet.kill()
        for monster in monsters:
            monster.kill()
        for asteroid in asteroids:
            asteroid.kill()
        time.delay(3000)
    clock.tick(FPS)
