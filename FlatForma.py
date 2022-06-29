# Twin Stick Shooter

import pygame

# initialise pygame
from Rope import Rope

pygame.init()
pygame.mixer.init()

# useful definitions
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
size = [SCREEN_WIDTH, SCREEN_HEIGHT]
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# Screen setting up
screen = pygame.display.set_mode(size)
screen.fill(white)
pygame.display.set_caption("Flatforma")

clock = pygame.time.Clock()


class Player:
    def __init__(self):
        self.x = 400
        self.y = 400
        self.yspeed = 0
        self.xspeed = 0


class Platform:
    def __init__(self, x, y, width, height, move=None):
        if move is None:
            move = []
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.move = move


platformlist = []

def touching(ob1, ob2, width, height):
    if ob1.y >= ob2.y - 10 and ob2.x - 9 <= ob1.x <= ob2.x + width + 9:
        if 10 >= ob1.y - (ob2.y - 10) >= 0:
            ob1.y = ob2.y - 10
            return "Top"
        if ob1.y <= ob2.y + height + 10:
            if 6 >= ob1.x - (ob2.x - 10) >= 0:
                return "rside"
            if -6 <= ob1.x - (ob2.x + width + 10) <= 0:
                return "lside"
        if ob1.y <= ob2.y + height + 10:
            ob1.yspeed *= -0.8
            ob1.y += 1
    return None


def touching_any(point, obj_list):
    for obj in obj_list:
        if obj.x < point[0] < obj.x + obj.width and obj.y < point[1] < obj.y + obj.height:
            return True
    return False

player = Player()

p = Platform(280, 50, 20, 150)
platformlist.append(p)
d = Platform(125, 350, 100, 300, [("x", 0.75, 300), ("y", 1, -300), ("x", -0.75, 900)])
platformlist.append(d)
d = Platform(-150, 270, 150, 30, [("x", -0.5, 600), ("x", 0.5, 300)])
platformlist.append(d)
d = Platform(5, 300, 120, 20, [("y", -0.5, 900), ("y", 0.5, 300)])
platformlist.append(d)

# Sets up the game loop that runs a frame of the game until done is True
done = False
Ground = True
Lside = False
Rside = False
count = 0

rope = None

grappling = False

while not done:
    screen.fill(white)

    if pygame.mouse.get_pressed(3)[2] and rope is not None:
        rope.shorten()

    if pygame.mouse.get_pressed(3)[0]:
        pos = pygame.mouse.get_pos()
        if rope is None:
            if touching_any(pos, platformlist):
                grappling = True
                rope = Rope(player, pos)
                Ground = False
                player.y -= 2
        else:
            pygame.draw.line(screen, black, rope.point, (player.x, player.y))
            rope.pull()
    else:
        grappling = False
        rope = None

    if player.y >= 450:
        Ground = True
        player.y = 450
    if player.x <= 10:
        Lside = True
    if player.x >= 490:
        Rside = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and Rside and not Ground:
                player.yspeed = -6
                player.xspeed = -4
                player.x -= 2
                Rside = False
            if event.key == pygame.K_UP and Lside and not Ground:
                player.yspeed = -6
                player.xspeed = 4
                player.x += 2
                Lside = False
            if event.key == pygame.K_UP and Ground:
                player.yspeed = -7
                player.y -= 1
                Ground = False
                for platform in platformlist:
                    touch = touching(player, platform, platform.width, platform.height)
                    if touch == "Top":
                        for m in platform.move:
                            if m[0] == "x":
                                if count % m[2] < m[2] / 2:
                                    player.xspeed -= m[1]
                                else:
                                    player.xspeed += m[1]

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and not Lside and player.xspeed >= -3.6:
        if not Ground:
            player.xspeed -= 0.05
        else:
            player.xspeed -= 0.2
    if keys[pygame.K_RIGHT] and not Rside and player.xspeed <= 3.6:
        if not Ground:
            player.xspeed += 0.05
        else:
            player.xspeed += 0.2
    if not keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT] and Ground:
        player.xspeed *= 0.95

    if not Ground:
        if Rside or Lside:
            if player.yspeed <= 3:
                player.yspeed += 0.15
        else:
            player.yspeed += 0.2
    else:
        if grappling:
            player.yspeed *= -0.5
        else:
            player.yspeed = 0
    player.y += player.yspeed
    if Lside and (not keys[pygame.K_RIGHT] or player.xspeed <= 0):
        if grappling:
            player.xspeed *= -0.5
        else:
            player.xspeed = 0
    if Rside and (not keys[pygame.K_LEFT] or player.xspeed >= 0):
        if grappling:
            player.xspeed *= -0.5
        else:
            player.xspeed = 0
    if player.x > 490:
        player.x = 490
    if player.x < 10:
        player.x = 10
    player.x += player.xspeed

    pygame.draw.rect(screen, black, (player.x - 10, player.y - 10, 20, 20))

    for platform in platformlist:
        pygame.draw.rect(screen, black, (platform.x, platform.y, platform.width, platform.height))
        for m in platform.move:
            if m[0] == "y":
                if count % m[2] < m[2] / 2:
                    platform.y -= m[1]
                else:
                    platform.y += m[1]
            if m[0] == "x":
                if count % m[2] < m[2] / 2:
                    platform.x -= m[1]
                else:
                    platform.x += m[1]

    pygame.draw.rect(screen, black, (0, 460, 500, 40))

    top = False
    side = False

    for platform in platformlist:
        touch = touching(player, platform, platform.width, platform.height)
        if not top:
            if touch == "Top":
                Ground = True
                top = True
                for m in platform.move:
                    if m[0] == "x":
                        if count % m[2] < m[2] / 2:
                            player.x -= m[1]
                        else:
                            player.x += m[1]
                    if m[0] == "y":
                        if count % m[2] < m[2] / 2:
                            player.y -= m[1]
                        else:
                            player.y += m[1]
            else:
                Ground = False
        if not side:
            if touch == "lside":
                side = True
                Lside = True
                player.x = platform.x + platform.width + 9

            elif touch == "rside":
                side = True
                Rside = True
                player.x = platform.x - 9
            else:
                Lside = False
                Rside = False

    if rope is not None and rope.length < 3:
        rope = None

    count += 1
    clock.tick(60)

    pygame.display.flip()

# quits pygame
pygame.quit()
