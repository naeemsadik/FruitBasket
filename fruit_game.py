"""
Fol Dhorar Mojar Khela (Fruit Catching Game)
===========================================

A PyGame-based arcade game where players catch falling fruits while avoiding bugs and bombs.
The game features multiple difficulty levels, dynamic backgrounds, and sound effects.

Features:
- Three difficulty levels
- Dynamic day/night cycle backgrounds
- Health system
- High score tracking
- Sound effects and background music
- Progressive difficulty scaling

Requirements:
- Python 3.x
- Pygame library

Assets required (in Assets/ directory):
- Fruits: fruit1.png to fruit9.png
- Bugs: bug0.png to bug5.png
- Backgrounds: Dupur.jpg, Shokal.jpg, Rat.jpg, Bikal.jpg, bg_front.jpg, bg_ending.jpg
- Other: basket.png, bomb.png
- Sound effects in Assets/mp3/: bg_music.mp3, menu_music.mp3, fruit_se.mp3, bug_se.mp3, bomb.mp3, levelUp.mp3

Author: [Naeem Abdullah Sadik, S M Sifatul Islam]
License: MIT
Version: 1.0.0
"""

import pygame
import random
import os

# Initialize Pygame
pygame.init()

# Game Configuration Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 800
BASKET_WIDTH, BASKET_HEIGHT = 150, 100
FRUIT_WIDTH, FRUIT_HEIGHT = 70, 70
BOMB_WIDTH, BOMB_HEIGHT = 50, 50
BG_CHANGE_INTERVAL = 15000  # milliseconds
FPS = 30
MAX_SPEED = 20  # New constant for maximum speed

# Colors
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Initialize game window
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Fol Dhorar Mojar Khela")

def config_mp3():
    """Configure and load all game sound effects and music."""
    file_paths = {
        "bgMusic": "Assets/mp3/bg_music.mp3",
        "menuMusic": "Assets/mp3/menu_music.mp3",
        "fruitCollision": "Assets/mp3/fruit_se.mp3",
        "bugCollision": "Assets/mp3/bug_se.mp3",
        "bombCollision": "Assets/mp3/bomb.mp3",
        "lvlUp": "Assets/mp3/levelUp.mp3"
    }
    sounds = {}
    for key, path in file_paths.items():
        try:
            sounds[key] = pygame.mixer.Sound(path)
        except pygame.error:
            print(f"Error loading sound: {path}")
    return sounds

def load_fruits():
    fruit_images = []
    for i in range(1, 10):
        try:
            image = pygame.image.load(f'Assets/fruit{i}.png')
            fruit_images.append(pygame.transform.scale(image, (FRUIT_WIDTH, FRUIT_HEIGHT)))
        except pygame.error:
            print(f"Error loading image: Assets/fruit{i}.png")
    return fruit_images

def load_bugs():
    bug_images = []
    for i in range(0, 6):
        try:
            image = pygame.image.load(f'Assets/bug{i}.png')
            bug_images.append(pygame.transform.scale(image, (FRUIT_WIDTH, FRUIT_HEIGHT)))
        except pygame.error:
            print(f"Error loading image: Assets/bug{i}.png")
    return bug_images

# Load images
try:
    basket_img = pygame.transform.scale(pygame.image.load('Assets/basket.png'), (BASKET_WIDTH, BASKET_HEIGHT))
    bomb_img = pygame.transform.scale(pygame.image.load('Assets/bomb.png'), (BOMB_WIDTH, BOMB_HEIGHT))

    # Backgrounds
    bg_dashboard = pygame.transform.scale(pygame.image.load('Assets/bg_front.jpg'), (SCREEN_WIDTH, SCREEN_HEIGHT))
    bg_ending = pygame.transform.scale(pygame.image.load('Assets/bg_ending.jpg'), (SCREEN_WIDTH, SCREEN_HEIGHT))
    bg_img_day = pygame.transform.scale(pygame.image.load('Assets/Dupur.jpg'), (SCREEN_WIDTH, SCREEN_HEIGHT))
    bg_img_morning = pygame.transform.scale(pygame.image.load('Assets/Shokal.jpg'), (SCREEN_WIDTH, SCREEN_HEIGHT))
    bg_img_night = pygame.transform.scale(pygame.image.load('Assets/Rat.jpg'), (SCREEN_WIDTH, SCREEN_HEIGHT))
    bg_img_noon = pygame.transform.scale(pygame.image.load('Assets/Bikal.jpg'), (SCREEN_WIDTH, SCREEN_HEIGHT))
except pygame.error as e:
    print(f"Error loading image: {e}")

# Background image list
bg_images = [bg_img_day, bg_img_morning, bg_img_night, bg_img_noon]
current_bg_index = 0
bg_img = bg_images[current_bg_index]

# Time-based changing
last_bg_change_time = pygame.time.get_ticks()

fruit_img = load_fruits()
bug_img = load_bugs()

# clock for FPS
clock = pygame.time.Clock()

def reset_game():
    global basket_x, basket_y, fruit_x, fruit_y, bomb_x, bomb_y, bug_x, bug_y, score, high_score, level
    global fruit_speed, bomb_speed, bug_speed, current_fruit_index, current_bug_index, player_health
    basket_x = SCREEN_WIDTH // 2 - BASKET_WIDTH // 2
    basket_y = SCREEN_HEIGHT - BASKET_HEIGHT - 20
    fruit_x = random.randint(50, SCREEN_WIDTH - FRUIT_WIDTH - 50)
    fruit_y = 0
    current_fruit_index = random.randint(0, len(fruit_img) - 1)
    bomb_x = random.randint(50, SCREEN_WIDTH - BOMB_WIDTH - 50)
    bomb_y = -100
    bug_x = random.randint(50, SCREEN_WIDTH - BOMB_WIDTH - 50)
    bug_y = -100
    current_bug_index = random.randint(0, len(bug_img) - 1)
    score = 0
    level = 1
    fruit_speed = 10
    bomb_speed = 10
    bug_speed = 5
    player_health = 100

def load_high_score():
    if os.path.exists("high_score.txt"):
        with open("high_score.txt", "r") as file:
            return int(file.read())
    return 0

def save_high_score(score):
    with open("high_score.txt", "w") as file:
        file.write(str(score))

high_score = load_high_score()
reset_game()

# Setting bomb speed
levels = {1: 10, 2: 15, 3: 20}

sounds = config_mp3()
sounds["bgMusic"].play(-1)

def display_text(text, size, color, x, y):
    font = pygame.font.SysFont(None, size)
    text_surface = font.render(text, True, color)
    window.blit(text_surface, (x, y))

def display_dashboard():
    window.blit(bg_dashboard, (0, 0))
    display_text("Select Level", 50, BLACK, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 100)
    display_text("1. Easy", 35, BLACK, SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 50)
    display_text("2. Medium", 35, BLACK, SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2)
    display_text("3. Hard", 35, BLACK, SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 50)
    pygame.display.update()

def display_game_over():
    global high_score
    if score > high_score:
        high_score = score
        save_high_score(high_score)
    window.blit(bg_ending, (0, 0))
    display_text(f"Score: {score}", 35, WHITE, 20, 60)
    display_text(f"High Score: {high_score}", 35, WHITE, SCREEN_WIDTH - 180, 60)
    display_text("Press R to Restart", 35, WHITE, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 250)
    pygame.display.update()

def draw_health_bar(health):
    pygame.draw.rect(window, RED, (10, 10, 200, 20))
    pygame.draw.rect(window, GREEN, (10, 10, 2 * health, 20))

running = True
in_dashboard = True
game_over = False

while running:
    if in_dashboard:
        display_dashboard()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    level = 1
                    fruit_speed = levels[level]
                    bomb_speed = 10
                    bug_speed = 5
                    in_dashboard = False
                elif event.key == pygame.K_2:
                    level = 2
                    fruit_speed = levels[level]
                    bomb_speed = levels[level]
                    bug_speed = levels[level]
                    in_dashboard = False
                elif event.key == pygame.K_3:
                    level = 3
                    fruit_speed = levels[level]
                    bomb_speed = levels[level]
                    bug_speed = levels[level]
                    in_dashboard = False
    elif game_over:
        display_game_over()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()
                    in_dashboard = True
                    game_over = False
    else:
        window.blit(bg_img, (0, 0))
        
        # Move the basket based on input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and basket_x > 0:
            basket_x -= 10
        if keys[pygame.K_RIGHT] and basket_x < SCREEN_WIDTH - BASKET_WIDTH:
            basket_x += 10

        # Create hitboxes for collision detection
        basket_hitbox = pygame.Rect(basket_x, basket_y, BASKET_WIDTH, BASKET_HEIGHT)
        
        # Draw the basket
        window.blit(basket_img, (basket_x, basket_y))

        # Move and handle fruit
        fruit_y += fruit_speed
        fruit_hitbox = pygame.Rect(fruit_x, fruit_y, FRUIT_WIDTH, FRUIT_HEIGHT)

        # Check if fruit is caught by the basket using improved collision detection
        if basket_hitbox.colliderect(fruit_hitbox):
            score += 1
            current_fruit_index = random.randint(0, len(fruit_img) - 1)
            fruit_x = random.randint(50, SCREEN_WIDTH - FRUIT_WIDTH - 50)
            fruit_y = 0
            # Increase speed with a cap
            fruit_speed = min(fruit_speed + 0.1, MAX_SPEED)
            sounds["fruitCollision"].play()

        # Reset fruit if it falls off screen
        if fruit_y > SCREEN_HEIGHT:
            current_fruit_index = random.randint(0, len(fruit_img) - 1)
            fruit_x = random.randint(50, SCREEN_WIDTH - FRUIT_WIDTH - 50)
            fruit_y = 0

        # Draw the fruit
        window.blit(fruit_img[current_fruit_index], (fruit_x, fruit_y))

        # Move and handle bug
        bug_y += bug_speed
        bug_hitbox = pygame.Rect(bug_x, bug_y, FRUIT_WIDTH, FRUIT_HEIGHT)
        
        # Check bug collision with improved detection
        if basket_hitbox.colliderect(bug_hitbox):
            player_health -= 20
            if player_health <= 0:
                game_over = True
            sounds["bugCollision"].play()
            bug_x = random.randint(50, SCREEN_WIDTH - BOMB_WIDTH - 50)
            bug_y = -100
            
        # Reset bug if it falls off screen
        if bug_y > SCREEN_HEIGHT:
            bug_x = random.randint(50, SCREEN_WIDTH - BOMB_WIDTH - 50)
            bug_y = -100
            current_bug_index = random.randint(0, len(bug_img) - 1)

        # Draw the bug
        window.blit(bug_img[current_bug_index], (bug_x, bug_y))

        # Handle bombs in levels 2 and 3
        if level > 1:
            bomb_y += bomb_speed
            bomb_hitbox = pygame.Rect(bomb_x, bomb_y, BOMB_WIDTH, BOMB_HEIGHT)

            if (bomb_x + BOMB_WIDTH > basket_x and bomb_x < basket_x + BASKET_WIDTH and
                bomb_y + BOMB_HEIGHT > basket_y and bomb_y < basket_y + BASKET_HEIGHT):
                player_health -= 50
                if player_health <= 0:
                    game_over = True
                sounds["bombCollision"].play()
                bomb_x = random.randint(50, SCREEN_WIDTH - BOMB_WIDTH - 50)
                bomb_y = -100

            if bomb_y > SCREEN_HEIGHT:
                bomb_x = random.randint(50, SCREEN_WIDTH - BOMB_WIDTH - 50)
                bomb_y = -100

            window.blit(bomb_img, (bomb_x, bomb_y))

        draw_health_bar(player_health)
        display_text(f"Score: {score}", 35, GREEN, 10, 40)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        current_time = pygame.time.get_ticks()
        if current_time - last_bg_change_time > BG_CHANGE_INTERVAL:
            current_bg_index = (current_bg_index + 1) % len(bg_images)
            bg_img = bg_images[current_bg_index]
            last_bg_change_time = current_time

        pygame.display.update()
        clock.tick(FPS)

pygame.quit()