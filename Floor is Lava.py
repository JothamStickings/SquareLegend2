# Floor is Lava Platformer

import pygame
import math
import random

# initialise pygame
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
purple = (128, 0, 128)

# Screen setting up
screen = pygame.display.set_mode(size)
screen.fill(white)
pygame.display.set_caption("Game")

clock = pygame.time.Clock()


class Player:
    def __init__(self):
        self.x = 50
        self.y = 50
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


class Enemy:
    def __init__(self, x, y, speed=1.0):
        self.x = x
        self.y = y
        self.speed = speed
        self.size = 15  # Enemy square size
        self.yspeed = 0
        self.grounded = False
        self.jump_cooldown = 0
        self.next_jump_time = random.randint(60, 180)  # Random jump interval (1-3 seconds at 60fps)
        
    def update(self, player, platform_list):
        # Calculate direction to player
        dx = player.x - self.x
        dy = player.y - self.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        # Handle jumping at random intervals
        self.jump_cooldown -= 1
        if self.jump_cooldown <= 0 and self.grounded:
            self.yspeed = -5  # Jump strength
            self.grounded = False
            self.jump_cooldown = self.next_jump_time
            self.next_jump_time = random.randint(60, 180)  # Set next random jump interval
        
        # Only move if player is not too close (to avoid jittery movement)
        if distance > 5:
            # Normalize direction and apply speed
            move_x = (dx / distance) * self.speed
            
            # Simple AI: move towards player horizontally
            self.x += move_x
            
            # Apply gravity
            if not self.grounded:
                self.yspeed += 0.2
            else:
                self.yspeed = 0
                
            self.y += self.yspeed
            
            # Check collision with platforms
            self.grounded = False
            for platform in platform_list:
                if self.check_platform_collision(platform):
                    break
                    
            # Keep enemy on screen
            if self.x < 0:
                self.x = 0
            elif self.x > SCREEN_WIDTH:
                self.x = SCREEN_WIDTH
                
            # Don't let enemy fall into lava (they hover above it)
            if self.y > 440:
                self.y = 440
                self.yspeed = 0
                self.grounded = True
    
    def check_platform_collision(self, platform):
        # Check if enemy is on top of platform
        if (platform.x - self.size <= self.x <= platform.x + platform.width + self.size and
            platform.y - self.size <= self.y <= platform.y + 5 and
            self.yspeed >= 0):
            self.y = platform.y - self.size
            self.yspeed = 0
            self.grounded = True
            return True
        return False
    
    def check_player_collision(self, player):
        # Check if enemy touches player
        return (abs(self.x - player.x) < 20 and abs(self.y - player.y) < 20)
    
    def draw(self, screen):
        pygame.draw.rect(screen, purple, (self.x - self.size//2, self.y - self.size//2, self.size, self.size))


platform_list = []
enemy_list = []


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


player = Player()

p = Platform(280, 50, 20, 150)
platform_list.append(p)
d = Platform(125, 350, 100, 300, [("x", 0.75, 300), ("y", 1, -300), ("x", -0.75, 900)])
platform_list.append(d)
d = Platform(-150, 270, 150, 30, [("x", -0.5, 600), ("x", 0.5, 300)])
platform_list.append(d)
d = Platform(5, 300, 120, 20, [("y", -0.5, 900), ("y", 0.5, 300)])
platform_list.append(d)

# Create enemies
enemy1 = Enemy(200, 200, 0.8)
enemy_list.append(enemy1)
enemy2 = Enemy(400, 100, 1.2)
enemy_list.append(enemy2)
enemy3 = Enemy(300, 300, 0.6)
enemy_list.append(enemy3)

# Sets up the game loop that runs a frame of the game until done is True
done = False
Ground = True
Lside = False
Rside = False
count = 0
game_over_message = ""

while not done:
    screen.fill(white)

    if player.y >= 450:
        done = True
        game_over_message = "You fell into the lava!"
    if player.x <= 10:
        Lside = True
    if player.x >= 490:
        Rside = True

    # Check enemy collisions with player
    for enemy in enemy_list:
        if enemy.check_player_collision(player):
            done = True
            game_over_message = "Enemy caught you!"

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
                for platform in platform_list:
                    touch = touching(player, platform, platform.width, platform.height)
                    if touch == "Top":
                        for m in platform.move:
                            if m[0] == "x":
                                if count % m[2] < m[2] / 2:
                                    player.xspeed -= m[1]
                                else:
                                    player.xspeed += m[1]
            if event.key == pygame.K_DOWN:
                bouncerlist = []

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
        player.yspeed = 0
    player.y += player.yspeed
    if Lside and (not keys[pygame.K_RIGHT] or player.xspeed <= 0):
        player.xspeed = 0
    if Rside and (not keys[pygame.K_LEFT] or player.xspeed >= 0):
        player.xspeed = 0
    if player.x > 490:
        player.x = 490
    if player.x < 10:
        player.x = 10
    player.x += player.xspeed

    # Update enemies
    for enemy in enemy_list:
        enemy.update(player, platform_list)

    # Draw player
    pygame.draw.rect(screen, black, (player.x - 10, player.y - 10, 20, 20))

    # Draw platforms
    for platform in platform_list:
        pygame.draw.rect(screen, black, (platform.x, platform.y, platform.width, platform.height))
        for m in platform.move:
            if m[0] == "y":
                if count % m[2] <= m[2] / 2:
                    platform.y -= m[1]
                else:
                    platform.y += m[1]
            if m[0] == "x":
                if count % m[2] <= m[2] / 2:
                    platform.x -= m[1]
                else:
                    platform.x += m[1]

    # Draw lava
    pygame.draw.rect(screen, red, (0, 460, 500, 40))

    # Draw enemies
    for enemy in enemy_list:
        enemy.draw(screen)

    top = False
    side = False

    for platform in platform_list:
        touch = touching(player, platform, platform.width, platform.height)
        if not top:
            if touch == "Top":
                Ground = True
                player.y = platform.y - 8.5
                top = True
                for m in platform.move:
                    if m[0] == "x":
                        if count % m[2] < m[2] / 2:
                            player.x -= m[1]
                        else:
                            player.x += m[1]
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

    count += 1
    clock.tick(60)

    pygame.display.flip()

# Display game over message if there is one
if game_over_message:
    print(game_over_message)

# quits pygame
pygame.quit()
