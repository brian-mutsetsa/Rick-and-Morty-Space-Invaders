import pygame
import random
import math
from pygame import mixer

# initialize pygame
pygame.init()

# Creating a game window

# create a screen
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load('game background.jpg')

# background sound
playlist = list()
playlist.append("Sounds/background.wav")
playlist.append("Sounds/Gerry Rafferty - Baker Street (Instrumental).mp3")
playlist.append("Sounds/Get Schwifty - Rick and Morty Karaoke.mp3")
playlist.append("Sounds/Head Bent Over - Rick and Morty Karaoke.mp3")
playlist.append("Sounds/Rick and Morty Theme Song [HD].mp3")
playlist.append("Sounds/The Rick Dance!.mp3")

mixer.music.load(playlist.pop())  # Get the first track from the playlist
mixer.music.queue(playlist.pop())  # Queue the 2nd song
mixer.music.set_endevent(pygame.USEREVENT)  # Setup the end track event
mixer.music.play()  # Play the music

# rename screen name
pygame.display.set_caption("Space invaders")

# change the logo/icon of the window
icon = pygame.image.load('alien (1).png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('Ship 80x80.png')
playerX = 370
playerY = 480
playerX_change = 0


def player(x, y):
    # drawing image to screen
    screen.blit(playerImg, (x, y))


# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('icons8-rick-sanchez-96.png'))
    enemyX.append(random.randint(0, 704))
    enemyY.append(random.randint(0, 10))
    enemyX_change.append(0.3)
    enemyY_change.append(40)


def enemy(x, y, i):
    # drawing image to screen
    screen.blit(enemyImg[i], (x, y))


# Bullet
# "ready" - you can't see the bullet on the screen
# "fire" - the bullet is currently moving
bulletImg = pygame.image.load('bullet (1).png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 1.5
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('go3v2.ttf', 32)
textX = 10
textY = 10
speed_increase = 0.1

# Game over text
over_font = pygame.font.Font('go3v2.ttf', 96)


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (0, 0, 0))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def fire_bullet(x, y):
    # drawing image to screen
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    global distance
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + math.pow(enemyY - bulletY, 2))
    if distance < 27:
        return True
    else:
        return False


# creating a game loop so its always running till the close button is pressed
running = True
while running:
    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0))

    # background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.USEREVENT:  # A track has ended
            if len(playlist) > 0:  # If there are more tracks in the queue...
                pygame.mixer.music.queue(playlist.pop())  # Q
            elif len(playlist) == 0:
                playlist.append("Sounds/background.wav")
                playlist.append("Sounds/Gerry Rafferty - Baker Street (Instrumental).mp3")
                playlist.append("Sounds/Get Schwifty - Rick and Morty Karaoke.mp3")
                playlist.append("Sounds/Head Bent Over - Rick and Morty Karaoke.mp3")
                playlist.append("Sounds/Rick and Morty Theme Song [HD].mp3")
                playlist.append("Sounds/The Rick Dance!.mp3")

                # mixer.music.load(playlist.pop())  # Get the first track from the playlist
                mixer.music.queue(playlist.pop())  # Queue the 2nd song
                # mixer.music.set_endevent(pygame.USEREVENT)  # Setup the end track event
                # mixer.music.play()  # Play the music

        # if keystroke is pressed check whether it is right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.6
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.6
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("Sounds/laser_2.wav")
                    bullet_sound.play()
                    # get the current X coordinate of the space ship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0  # stops moving ship when button is let go

    playerX += playerX_change  # moves ship continuously to the intended direction

    # creating the boundary for the ship
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736  # because the image(starting point is at left side) takes up 64 pixels

    # Enemy movement
    for i in range(num_of_enemies):
        # Game over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound("Sounds/explosion.wav")
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 10
            enemyX[i] = random.randint(0, 704)
            enemyY[i] = random.randint(0, 10)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()  # to constantly update the screen
