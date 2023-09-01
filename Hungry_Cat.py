import pygame, random

pygame.init()

# Set a display surface and icon
WINDOW_WIDTH = 700
WINDOW_HEIGHT = 700
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Hungry Cat")
icon = pygame.image.load("Icon_Cat.png")
pygame.display.set_icon(icon)

# Set FPS and clock
FPS = 60
clock = pygame.time.Clock()

# Set a game values
PLAYER_STARTING_LIVES = 5
PLAYER_VELOCITY = 7
FOOD_STARTING_VELOCITY = 5
FOOD_ACCELERATION = 0.2
BUFFER_DISTANCE = -100
score = 0
player_lives = PLAYER_STARTING_LIVES
food_velocity = FOOD_STARTING_VELOCITY

# Import custom font
custom_font = pygame.font.Font("IniyaDisplay-ow0Ra.otf", 32)

# Render texts
score_text = custom_font.render(f"Score: {score}", True, (255, 255, 255))
score_rect = score_text.get_rect()
score_rect.center = ((WINDOW_WIDTH // 4), 30)

lives_text = custom_font.render(f"Lives: {player_lives}", True, (255, 255, 255))
lives_rect = lives_text.get_rect()
lives_rect.center = ((WINDOW_WIDTH // 4) * 3, 30)

game_over_text = custom_font.render(
    "I really don't like stones...", True, (255, 255, 255)
)
game_over_rect = game_over_text.get_rect()
game_over_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 80)

continue_text = custom_font.render("Press SPACE to play again", True, (255, 255, 255))
continue_rect = continue_text.get_rect()
continue_rect.center = (WINDOW_WIDTH // 2, 600)

# Import sound effects
eat_sound = pygame.mixer.Sound("Boost.wav")
stone_sound = pygame.mixer.Sound("Stone.wav")
miss_sound = pygame.mixer.Sound("miss.wav")
# Background music
pygame.mixer.music.load("music.wav")

# Import a bacground image
background = pygame.image.load("background_image.jfif")
# Import game images
cat_img = pygame.image.load("Hungry_Cat.png")
cat_rect = cat_img.get_rect()
cat_rect.bottomleft = (WINDOW_WIDTH // 2, WINDOW_HEIGHT)

food_img = pygame.image.load("Food.png")
food_rect = food_img.get_rect()
food_rect.x = random.randint(15, 615)
food_rect.y = BUFFER_DISTANCE

stone_img = pygame.image.load("Stone.png")
stone_rect = stone_img.get_rect()
stone_rect.x = random.randint(15, 615)
stone_rect.y = BUFFER_DISTANCE

end_cat_img = pygame.image.load("End_Cat.png")
end_cat_rect = end_cat_img.get_rect()
end_cat_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 40)

# The main game loop
pygame.mixer.music.play(-1, 0.0)
running = True
while running:
    # Check to see if uses wants to quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movements
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and cat_rect.left > 0:
        cat_rect.x -= PLAYER_VELOCITY
    if keys[pygame.K_RIGHT] and cat_rect.right < WINDOW_WIDTH:
        cat_rect.x += PLAYER_VELOCITY
    if keys[pygame.K_UP] and cat_rect.top > 60:
        cat_rect.y -= PLAYER_VELOCITY
    if keys[pygame.K_DOWN] and cat_rect.bottom < WINDOW_HEIGHT:
        cat_rect.y += PLAYER_VELOCITY

    # Move the food
    if food_rect.y > WINDOW_HEIGHT:
        # Player missed food
        miss_sound.play()
        food_rect.x = random.randint(15, 615)
        food_rect.y = BUFFER_DISTANCE
    else:
        # Move the food
        food_rect.y += food_velocity

    # Move the stone
    if stone_rect.y > WINDOW_HEIGHT:
        stone_rect.x = random.randint(15, 615)
        stone_rect.y = BUFFER_DISTANCE
    else:
        stone_velocity = food_velocity
        stone_rect.y += stone_velocity

    # Check a collision beetween two rects
    if cat_rect.colliderect(food_rect):
        eat_sound.play()
        score += 1
        food_velocity += FOOD_ACCELERATION
        food_rect.x = random.randint(15, 615)
        food_rect.y = BUFFER_DISTANCE

    if cat_rect.colliderect(stone_rect):
        stone_sound.play()
        player_lives -= 1
        stone_rect.x = random.randint(15, 615)
        stone_rect.y = BUFFER_DISTANCE

    # Update HUD
    score_text = custom_font.render(f"Score: {score}", True, (255, 255, 255))
    lives_text = custom_font.render(f"Lives: {player_lives}", True, (255, 255, 255))

    # Check for GAME OVER
    if player_lives == 0:
        display_surface.fill((0, 0, 0))
        display_surface.blit(score_text, score_rect)
        display_surface.blit(game_over_text, game_over_rect)
        display_surface.blit(continue_text, continue_rect)
        display_surface.blit(end_cat_img, end_cat_rect)
        pygame.display.update()

        # Pause the game until player presses a key, then reste the game
        pygame.mixer.music.stop()
        is_pause = True
        while is_pause:
            for event in pygame.event.get():
                # The player want to play
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    score = 0
                    player_lives = PLAYER_STARTING_LIVES
                    cat_rect.bottomleft = (WINDOW_WIDTH // 2, WINDOW_HEIGHT)
                    food_velocity = FOOD_STARTING_VELOCITY
                    pygame.mixer.music.play(-1, 0.0)
                    is_pause = False
                # The player want to quit
                if event.type == pygame.QUIT:
                    is_pause = False
                    running = False

    # Blit assets to the screen
    display_surface.blit(background, (0, 0))
    display_surface.blit(cat_img, cat_rect)
    display_surface.blit(food_img, food_rect)
    display_surface.blit(stone_img, stone_rect)

    # Blit the HUD to the screen
    display_surface.blit(score_text, score_rect)
    display_surface.blit(lives_text, lives_rect)
    pygame.draw.line(display_surface, (255, 255, 255), (0, 60), (WINDOW_WIDTH, 60), 1)

    # Update display_surface
    pygame.display.update()

    # Tick the clock
    clock.tick(FPS)

# End the game
pygame.quit()
