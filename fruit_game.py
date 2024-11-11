import pygame
import random
import os

pygame.init()

screen_width, screen_height = 600, 600
window = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Fol Dhorar Mojar Khela")

# Colors
green = (0, 255, 0)
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

def config_mp3():
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
            fruit_images.append(pygame.transform.scale(image, (fruit_width, fruit_height)))
        except pygame.error:
            print(f"Error loading image: Assets/fruit{i}.png")
    return fruit_images

def load_bugs():
    bug_images = []
    for i in range(0, 6):
        try:
            image = pygame.image.load(f'Assets/bug{i}.png')
            bug_images.append(pygame.transform.scale(image, (fruit_width, fruit_height)))
        except pygame.error:
            print(f"Error loading image: Assets/bug{i}.png")
    return bug_images

# Images Sizes
basket_width, basket_height = 150, 100
fruit_width, fruit_height = 70, 70
bomb_width, bomb_height = 50, 50

try:
    basket_img = pygame.transform.scale(pygame.image.load('basket.png'), (basket_width, basket_height))
    bomb_img = pygame.transform.scale(pygame.image.load('bomb.png'), (bomb_width, bomb_height))

    # Backgrounds
    bg_dashboard = pygame.transform.scale(pygame.image.load('Assets/bg_front.jpg'), (screen_width, screen_height))
    bg_ending = pygame.transform.scale(pygame.image.load('Assets/bg_ending.jpg'), (screen_width, screen_height))
    bg_img_day = pygame.transform.scale(pygame.image.load('Assets/Dupur.jpg'), (screen_width, screen_height))
    bg_img_morning = pygame.transform.scale(pygame.image.load('Assets/Shokal.jpg'), (screen_width, screen_height))
    bg_img_night = pygame.transform.scale(pygame.image.load('Assets/Rat.jpg'), (screen_width, screen_height))
    bg_img_noon = pygame.transform.scale(pygame.image.load('Assets/Bikal.jpg'), (screen_width, screen_height))
except pygame.error as e:
    print(f"Error loading image: {e}")

# Background image list
bg_images = [bg_img_day, bg_img_morning, bg_img_night, bg_img_noon]
current_bg_index = 0
bg_img = bg_images[current_bg_index]

# Time-based changing
bg_change_time = 15000  # Change -> 15 seconds
last_bg_change_time = pygame.time.get_ticks()

fruit_img = load_fruits()
bug_img = load_bugs()

# clock for FPS
clock = pygame.time.Clock()

# Game variables
def reset_game():
    global basket_x, basket_y, fruit_x, fruit_y, bomb_x, bomb_y, bug_x, bug_y, score, high_score, level, fruit_speed, bomb_speed, bug_speed, current_fruit_index, current_bug_index, player_health
    basket_x = screen_width // 2 - basket_width // 2
    basket_y = screen_height - basket_height - 20
    fruit_x = random.randint(50, screen_width - fruit_width - 50)
    fruit_y = 0
    current_fruit_index = random.randint(0, len(fruit_img) - 1)
    bomb_x = random.randint(50, screen_width - bomb_width - 50)
    bomb_y = -100
    bug_x = random.randint(50, screen_width - bomb_width - 50)
    bug_y = -100
    current_bug_index = random.randint(0, len(bug_img) - 1)  # Select a random bug for the first time
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
    display_text("Select Level", 50, black, screen_width // 2 - 100, screen_height // 2 - 100)
    display_text("1. Easy", 35, black, screen_width // 2 - 50, screen_height // 2 - 50)
    display_text("2. Medium", 35, black, screen_width // 2 - 50, screen_height // 2)
    display_text("3. Hard", 35, black, screen_width // 2 - 50, screen_height // 2 + 50)
    pygame.display.update()

def display_game_over():
    global high_score
    if score > high_score:
        high_score = score
        save_high_score(high_score)
    window.blit(bg_ending, (0, 0))
    display_text(f"Score: {score}", 35, white, 20, 60)
    display_text(f"High Score: {high_score}", 35, white, screen_width - 180, 60)
    display_text("Press R to Restart", 35, white, screen_width // 2 - 100, screen_height // 2 + 250)
    pygame.display.update()

def draw_health_bar(health):
    pygame.draw.rect(window, red, (10, 10, 200, 20))
    pygame.draw.rect(window, green, (10, 10, 2 * health, 20))

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
        if keys[pygame.K_RIGHT] and basket_x < screen_width - basket_width:
            basket_x += 10

        # Draw the basket
        window.blit(basket_img, (basket_x, basket_y))

        # Move the fruit down
        fruit_y += fruit_speed

        # Check if fruit is caught by the basket
        if (fruit_x + fruit_width > basket_x and fruit_x < basket_x + basket_width and
            fruit_y + fruit_height > basket_y and fruit_y < basket_y + basket_height):
            score += 1
            current_fruit_index = random.randint(0, len(fruit_img) - 1)
            fruit_x = random.randint(50, screen_width - fruit_width - 50)
            fruit_y = 0
            fruit_speed += 0.5
            sounds["fruitCollision"].play()

        # Reset fruit if it falls off screen
        if fruit_y > screen_height:
            current_fruit_index = random.randint(0, len(fruit_img) - 1)
            fruit_x = random.randint(50, screen_width - fruit_width - 50)
            fruit_y = 0

        # Draw the fruit
        window.blit(fruit_img[current_fruit_index], (fruit_x, fruit_y))

        # Move the bug down
        bug_y += bug_speed
        
        # Check if the bug hits the basket
        if (bug_x + bomb_width > basket_x and bug_x < basket_x + basket_width and
            bug_y + bomb_height > basket_y and bug_y < basket_y + basket_height):
            player_health -= 20
            if player_health <= 0:
                game_over = True
            sounds["bugCollision"].play()
            bug_x = random.randint(50, screen_width - bomb_width - 50)
            bug_y = -100
            
        # Reset bug if it falls off screen
        if bug_y > screen_height:
            bug_x = random.randint(50, screen_width - bomb_width - 50)
            bug_y = -100
            current_bug_index = random.randint(0, len(bug_img) - 1)  # Select a new random bug image

        # Draw the bug
        window.blit(bug_img[current_bug_index], (bug_x, bug_y))

        # Handle bombs in levels 2 and 3
        if level > 1:
            bomb_y += bomb_speed

            if (bomb_x + bomb_width > basket_x and bomb_x < basket_x + basket_width and
                bomb_y + bomb_height > basket_y and bomb_y < basket_y + basket_height):
                player_health -= 50
                if player_health <= 0:
                    game_over = True
                sounds["bombCollision"].play()
                bomb_x = random.randint(50, screen_width - bomb_width - 50)
                bomb_y = -100

            if bomb_y > screen_height:
                bomb_x = random.randint(50, screen_width - bomb_width - 50)
                bomb_y = -100

            window.blit(bomb_img, (bomb_x, bomb_y))

        draw_health_bar(player_health)
        display_text(f"Score: {score}", 35, green, 10, 40)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        current_time = pygame.time.get_ticks()
        if current_time - last_bg_change_time > bg_change_time:
            current_bg_index = (current_bg_index + 1) % len(bg_images)
            bg_img = bg_images[current_bg_index]
            last_bg_change_time = current_time

        pygame.display.update()
        clock.tick(30)

pygame.quit()