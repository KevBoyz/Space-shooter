import pygame
from pygame import display
from pygame import font
from pygame import mixer
from pygame.image import load
from pygame.transform import scale
from pygame.sprite import Sprite, GroupSingle, Group, groupcollide
from pygame import event
from pygame.locals import QUIT, KEYDOWN, K_SPACE, K_a, K_d
from pygame.time import Clock
from random import randint

pygame.init()
fonte = font.SysFont('comicsans', 50)
lfont = font.SysFont('comicsans', 300)





class SpaceShip(Sprite):
    def __init__(self, bullet):
        super().__init__()
        self.image = load('Sprites/spaceship.png')  # Sprite
        self.rect = self.image.get_rect(center=(540, 550))  # Hit box
        self.speed = 3.5
        self.bullet = bullet
        self.life = 3

    def shot(self):
        if len(nave) > 0:
            nv_shot = mixer.music.load('Sounds/nave-shot.wav')
            mixer.music.play(1)
            self.bullet.add(Bullet(self.rect.x + 70, self.rect.y - 6))
            self.bullet.add(Bullet(self.rect.x + 32, self.rect.y + 63))
            self.bullet.add(Bullet(self.rect.x + 107, self.rect.y + 63))

    def hit(self):
        if self.life <= 0:
            self.kill()
        else:
            self.life -= 1

    def update(self):
        global laser, nave
        if groupcollide(laser, nave, True, False):
            self.hit()
        keys = pygame.key.get_pressed()
        if keys[K_a]:
            if not self.rect.x <= 0:
                self.rect.x -= self.speed
        elif keys[K_d]:
            if not self.rect.x >= 940:
                self.rect.x += self.speed


class Bullet(Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = load('Sprites/bullet.png')
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 4

    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()


class OVNI(Sprite):
    def __init__(self, laser, x, y):
        super().__init__()
        self.image = load('Sprites/ovni.png')
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 4
        self.direction = 0
        self.laser = laser
        self.life = 3

    def shot(self):
        ufo_shot = mixer.music.load('Sounds/ufo-shot.wav')
        mixer.music.play(1)
        self.laser.add(Laser(self.rect.x + 81, self.rect.y + 15))
        self.laser.add(Laser(self.rect.x + 181, self.rect.y + 15))

    def hit(self):
        if self.life <= 0:
            global kills
            self.kill()
            kills += 1
        else:
            self.life -= 1

    def update(self):
        global bullet, ufo
        if groupcollide(bullet, ufo, True, False):
            self.hit()
        if randint(0, 200) == 18:
            self.shot()
        if self.direction == 0:
            self.rect.x -= self.speed
            if self.rect.x <= 0:
                self.direction = 1
        else:
            self.rect.x += self.speed
            if self.rect.x >= 850:
                self.direction = 0


class Laser(Sprite):
    def __init__(self, x, y):
        super(Laser, self).__init__()
        self.image = load('Sprites/ufo-laser.png')
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 3

    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 700:
            self.kill()





bullet = Group()
laser = Group()

spship = SpaceShip(bullet)
nave = GroupSingle(spship)

ufo = Group()

size = (1080, 700)
window = display.set_mode(
    display=0,  # display = monitor
    size=size,
    depth=0,
    vsync=0,
    flags=0
)

display.set_caption('Space-shooter')
bg = scale(load('images/space-bg.jpg'), size)

clock = Clock()
kills = 0
round = 0
while True:
    clock.tick(300)  # FPS
    for ev in event.get():  # Close event
        if ev.type == QUIT:
            pygame.quit()
        if ev.type == KEYDOWN:
            if ev.key == K_SPACE:
                spship.shot()
    window.blit(bg, (0, 0))  # (200, 50) Position, 4 cartesian quadrant
    kill_count = fonte.render(
        f'Kills: {kills}',
        True,  # No serif
        (255, 255, 255)
    )
    life_show = fonte.render(
        f'Life: {spship.life}',
        True,  # No serif
        (255, 255, 255)
    )
    lose = lfont.render(
        'You Lose',
        True,  # No serif
        (255, 255, 255)
    )
    if len(nave) == 0:
        window.blit(lose, (80, 270))
    window.blit(kill_count, (20, 650))
    window.blit(life_show, (180, 650))
    nave.draw(window)
    if round % 200 == 0 and len(ufo) <= 10:
        ufo.add(OVNI(laser, randint(0, 1080), randint(0, 200)))
        if kills >= 20:
            ufo.add(OVNI(laser, randint(0, 1080), randint(0, 200)))
        if kills >= 50:
            ufo.add(OVNI(laser, randint(0, 1080), randint(0, 200)))
        if kills >= 70:
            ufo.add(OVNI(laser, randint(0, 1080), randint(0, 200)))
        if kills >= 90:
            ufo.add(OVNI(laser, randint(0, 1080), randint(0, 200)))
        if kills >= 100:
            ufo.add(OVNI(laser, randint(0, 1080), randint(0, 200)))
    ufo.draw(window)
    bullet.draw(window)
    laser.draw(window)
    nave.update()
    bullet.update()
    laser.update()
    ufo.update()
    display.update()
    round += 1
