import pygame
import random
from datetime import date

pygame.init()

screen_x = 552
screen_y = 516

win = pygame.display.set_mode((screen_x, screen_y))

pygame.display.set_caption('Minion run!')


icon = pygame.image.load('sunny.png')
pygame.display.set_icon(icon)

pygame.mixer.music.load('music.mp3')
pygame.mixer.music.set_volume(0.23)

press_s = pygame.mixer.Sound('click.wav')

score = 0
max_score = 0
jump_over = False


class Something:
    def __init__(self, x, y, w, speed1, pic):
        self.x = x
        self.y = y
        self.speed = speed1
        self.pic = pic
        self.w = w

    def move(self):
        if self.x >= -screen_x:
            win.blit(self.pic, (self.x, self.y))
            self.x -= self.speed
            return True
        else:
            return False

    def return1(self, dis, y, w, pic):
        self.x = dis
        self.y = y
        self.w = w
        self.pic = pic
        win.blit(self.pic, (self.x, self.y))


class Button:
    def __init__(self, w, h):
        self.w = w
        self.h = h

    def set(self, x, y, message, act=None):
        m = pygame.mouse.get_pos()
        press = pygame.mouse.get_pressed(3)

        if x < m[0] < x + self.w:
            if y < m[1] < y + self.h:
                pygame.draw.rect(win, (251, 213, 39), (x, y, self.w, self.h))

                if press[0] == 1 and act is not None:
                    pygame.mixer.Sound.play(press_s)
                    pygame.time.delay(300)
                    if act is not None:
                        if act == quit:
                            pygame.quit()
                            quit()
                        else:
                            act()

        else:
            pygame.draw.rect(win, (255, 151, 17), (x, y, self.w, self.h))

        text1(message, x + 10, y + 10)


button = Button(70, 48)

player = pygame.image.load('minion.png')
player_x = 240
player_y = 370

block1 = pygame.image.load('brickwall.png')
block2 = pygame.image.load('bush.png')
block3 = pygame.image.load('fence.png')
block4 = pygame.image.load('recycle-bin.png')
block5 = pygame.image.load('landslide.png')
blocklist = [block1, block2, block3, block4, block5]

block_size = [64, 370, 63, 395, 64, 370, 64, 370, 64, 370]

clouds = [pygame.image.load('clouds.png'), pygame.image.load('cloud-computing.png'), pygame.image.load('aeroplane.png')]

clock = pygame.time.Clock()

makejump = False
jumpcount = 30

banana = pygame.image.load('banana.png')
life = 3
speed = 4

minions = pygame.image.load('minions.jpg')


def menu():

    s = True

    button1 = Button(130, 70)
    button2 = Button(130, 70)
    button3 = Button(130, 70)

    while s:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.Sound.play(press_s)
                pygame.quit()
                quit()

        win.blit(minions, (0, 0))
        button1.set(210, 200, '       Start', start)
        button2.set(210, 280, '        Quit', quit)
        button3.set(210, 370, '     Records', sc)

        pygame.display.update()
        clock.tick(100)


def sc():

    j = open("Game progress.txt", 'r')
    lines = j.readlines()
    r = True
    button4 = Button(70, 40)

    while r:

        win.fill((255, 224, 17))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        x = 100
        y = 100
        for i in lines:
            text1(i, x, y)
            y += 30

        button4.set(20, 30, 'Back', menu)
        pygame.display.update()


def start():

    global life, score, makejump, player_y, jumpcount

    while game():
        score = 0
        player_y = 370
        life = 3
        makejump = False
        jumpcount = 30


def play(x, y):
    win.blit(player, (x, y))


def game():

    pygame.mixer.music.play(-1)

    global makejump, player_x, life, speed

    run = True

    block_arr = []
    create_block(block_arr)
    background = pygame.image.load('sky.png')
    cloud = random_cloud()

    while run:
        win.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.Sound.play(press_s)
                pygame.quit()
                quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            makejump = True
        if keys[pygame.K_ESCAPE]:
            pygame.mixer.Sound.play(press_s)
            pause()

        if makejump:
            jump()

        bananas()

        if check_play(block_arr) is True:
            if eatbanana() is False:
                run = False

        scores(block_arr)

        text1('Your score is: ' + str(score), 40, 49)
        play(player_x, player_y)
        draw_block(block_arr)
        move_cloud(cloud)
        speed += 1

        button.set(20, 100, 'Menu', menu)

        pygame.display.update()
        clock.tick(30)

    return game_over()


def jump():
    global player_y, makejump, jumpcount
    if jumpcount >= -30:
        player_y -= jumpcount / 3
        jumpcount -= 1
    else:
        jumpcount = 30
        makejump = False


def create_block(array):
    global speed

    choice = random.randrange(0, 5)
    pic = blocklist[choice]
    w = block_size[choice * 2]
    height = block_size[choice * 2 + 1]
    array.append(Something(screen_x, height, w, speed, pic))

    choice = random.randrange(0, 5)
    pic = blocklist[choice]
    w = block_size[choice * 2]
    height = block_size[choice * 2 + 1]
    array.append(Something(screen_x + 300, height, w, speed, pic))

    choice = random.randrange(0, 5)
    pic = blocklist[choice]
    w = block_size[choice * 2]
    height = block_size[choice * 2 + 1]
    array.append(Something(screen_x + 700, height, w, speed, pic))

    choice = random.randrange(0, 5)
    pic = blocklist[choice]
    w = block_size[choice * 2]
    height = block_size[choice * 2 + 1]
    array.append(Something(screen_x + 980, height, w, speed, pic))

    choice = random.randrange(0, 5)
    pic = blocklist[choice]
    w = block_size[choice * 2]
    height = block_size[choice * 2 + 1]
    array.append(Something(screen_x + 1290, height, w, speed, pic))


def find_dis(array):
    maxm = max(array[0].x, array[1].x, array[2].x, array[3].x, array[4].x)
    if maxm < screen_x:
        dis = screen_x
        if dis - maxm < 70:
            dis += 170
    else:
        dis = maxm

    dis += random.randrange(249, 400)

    return dis


def draw_block(array):
    for something in array:
        view = something.move()
        if view is False:
            dis = find_dis(array)

            choice = random.randrange(0, 3)
            pic = blocklist[choice]
            w = block_size[choice * 2]
            height = block_size[choice * 2 + 1]

            something.return1(dis, height, w, pic)


def random_cloud():
    choice = random.randrange(0, 3)
    piccloud = clouds[choice]

    cloud = Something(screen_x, 100, 20, 3, piccloud)
    return cloud


def move_cloud(cloud):
    x = cloud.move()
    if x is False:
        choice = random.randrange(0, 3)
        piccloud = clouds[choice]
        cloud.return1(screen_x, 200 - random.randrange(20,  170), 20, piccloud)


def text1(message, x, y, font='BebasNeue-Regular.ttf', color=(247, 8, 21), big=27):
    font1 = pygame.font.Font(font, big)
    text = font1.render(message, True, color)
    win.blit(text, (x, y))


def pause():
    paused = True
    while paused is True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.Sound.play(press_s)
                pygame.quit()
                quit()

        text1('Paused. Press Enter to continue', screen_x / 4, screen_y / 2)
        text1('To exit the game press Space', screen_x / 4, screen_y / 2 + 33)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            pygame.mixer.Sound.play(press_s)
            paused = False

        if keys[pygame.K_SPACE]:
            pygame.mixer.Sound.play(press_s)
            pygame.quit()
            quit()

        pygame.display.update()
        clock.tick(70)


def check_play(blocks):
    global player_x
    for block in blocks:
        if makejump is False:
            if block.x + 20 <= player_x + 13 <= block.x + block.w:
                if eatbanana() is True:
                    dis = find_dis(blocks)

                    choice = random.randrange(0, 5)
                    pic = blocklist[choice]
                    w = block_size[choice * 2]
                    height = block_size[choice * 2 + 1]

                    block.return1(dis, height, w, pic)
                else:
                    return True

        elif jumpcount >= 0:
            if player_y + 30 >= block.y:
                if block.x <= player_x + 27 <= block.x + 49:
                    return True
            else:
                if player_y + 53 >= block.y:
                    if block.x <= player_x <= block.x + 70:
                        return True


def game_over():
    global score, max_score

    if score > max_score:
        max_score = score
    over = True
    while over is True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.Sound.play(press_s)
                pygame.quit()
                quit()

        text1('Game Over! Press enter for menu. Escape to exit.', 40, screen_y / 2)
        text1('Your maximum score is: ' + str(max_score), 70, screen_y / 2 + 49)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            pygame.mixer.Sound.play(press_s)
            menu()

        if keys[pygame.K_ESCAPE]:
            pygame.mixer.Sound.play(press_s)
            over = False

        pygame.display.update()
        clock.tick(70)
    f = open('Game progress.txt', 'a')
    f.write(str(date.today()) + ' score:' + str(max_score) + '\n')
    f.close()


def bananas():
    global life
    show = 0
    x = 340
    while show != life:
        win.blit(banana, (x, 49))
        x += 33
        show += 1


def eatbanana():
    global life, player_x
    life -= 1
    if life == 0:
        game_over()
    else:
        player_x += 7
        return True


def scores(blocks):
    global score, jump_over
    if jump_over is False:
        for block in blocks:
            if block.x <= player_x + 32 <= block.x + block.w:
                if player_y + 60 <= block.y:
                    jump_over = True
                    break
    else:
        if jumpcount == -30:
            score += 1
            jump_over = False


menu()

quit()
