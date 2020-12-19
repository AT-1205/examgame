import pygame
import random
import math

pygame.init()

screen_x = 500
screen_y = 500
win = pygame.display.set_mode((screen_x, screen_y))

pygame.display.set_caption('Exam game')
icon = pygame.image.load('recycle-symbol.png')
pygame.display.set_icon(icon)

background = pygame.image.load('nature.png')
player = pygame.image.load('recycling-bin.png')
bottle = pygame.image.load('plasticbottle.png')
banana = pygame.image.load('banana.png')
chicken = pygame.image.load('chicken.png')
apple = pygame.image.load('apple.png')

score = 0
recycle_binx = 340
recycle_biny = 440
speed = 9
pause = False

applex = random.randint(40, screen_x - 80)
appley = -4

bananax = random.randint(40, screen_x - 80)
bananay = -7
bootle_x = random.randint(40, screen_x - 80)
bootle_y = 0

chickenx = random.randint(40, screen_x - 80)
chickeny = 0

move = 4

run = True
clock = pygame.time.Clock()
timepass = 1327


def play(x, y):
    win.blit(player, (x, y))


def trash(tr, x, y):
    win.blit(tr, (x, y))


def collect(c, t, p, r):
    distance = math.sqrt((math.pow(r - t, 2)) + math.pow(p - c, 2))
    if distance < 50:
        return True
    else:
        return False


while run:

    win.blit(background, (0, 0))

    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        if pause is False:
            pause = True
        else:
            pause = False
    if pause is False:
        if keys[pygame.K_LEFT]:
                recycle_binx -= speed
        if keys[pygame.K_RIGHT]:
                recycle_binx += speed
        bootle_y += move

        appley += move - 2.4

        if bootle_y > screen_y - 70:
            bootle_y = 0
            bootle_x = random.randint(40, screen_x - 80)

        if bananay > screen_y - 80:
            bananay = -7
            bananax = random.randint(40, screen_x - 80)

        if recycle_binx < 40:
            recycle_binx = 40
        if recycle_binx > screen_x - 90:
            recycle_binx = screen_x - 90

    if collect(bootle_x, bootle_y, recycle_binx, recycle_biny) is True:
        score += 1
        print(score)
        bootle_y = 0
        bootle_x = random.randint(40, screen_x - 80)

    if collect(bananax, bananay, recycle_binx, recycle_biny) is True:
        score += 1
        print(score)
        bananay = 0
        bananax = random.randint(40, screen_x - 80)



    play(recycle_binx, recycle_biny)
    trash(bottle, bootle_x, bootle_y)

    current_time = pygame.time.get_ticks()
    if bootle_y > 100:
        trash(chicken, chickenx, chickeny)
        chickeny += move


    pygame.display.update()
