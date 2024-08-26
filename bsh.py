import random
import pygame
from pygame.locals import (
    K_DOWN,
    K_ESCAPE,
    K_LEFT,
    K_RIGHT,
    K_UP,
    K_SPACE,
    KEYDOWN,
    QUIT,
    MOUSEBUTTONDOWN,
    RLEACCEL,
)

# Game settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700
GRAVITY = 1  # Gravity value for the jet's fall
JUMP_SPEED = -15
BULLET_COOLDOWN = 300  # milliseconds
POINTS_PER_MS = 3  # Points per millisecond
GAME_OVER_DELAY = 3000  # milliseconds before transitioning to the menu

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("plane.png").convert()
        self.surf.set_colorkey((100, 100, 100), RLEACCEL)
        self.rect = self.surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        self.speed_y = 0  # Speed in the Y direction
        self.lives = 3
        self.immortal_time = 0  # Time the player is invincible
        self.immortal_duration = 100  # Duration of invincibility frames
        self.can_jump = True  # Whether the player is on the ground
        self.last_shot_time = 0  # Time of the last bullet shot

    def jump(self):
        if self.can_jump:
            self.speed_y = JUMP_SPEED
            self.can_jump = False

    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > BULLET_COOLDOWN:
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            player_bullets.add(bullet)
            self.last_shot_time = current_time

    def update(self, pressed_keys):
        if self.immortal_time > 0:
            self.immortal_time -= 1
            # Toggle visibility for blinking effect
            if self.immortal_time % 10 < 5:
                self.surf.set_alpha(0)  # Make the jet invisible
            else:
                self.surf.set_alpha(255)  # Make the jet visible
        else:
            self.surf.set_alpha(255)  # Ensure the jet is visible if not immortal

        self.speed_y += GRAVITY
        self.rect.move_ip(0, self.speed_y)

        # Check if on the ground
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.speed_y = 0
            self.can_jump = True
        elif self.rect.top <= 0:
            self.rect.top = 0
            self.speed_y = 0
            self.can_jump = False

        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-10, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(10, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

    def take_damage(self):
        if self.immortal_time <= 0:
            self.lives -= 1
            self.immortal_time = self.immortal_duration
            if self.lives <= 0:
                return False  # Indicate that the player has no lives left
        return True

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Bullet, self).__init__()
        self.surf = pygame.image.load("bullet.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(center=(x, y))
        self.speed = -10  # Bullet moves upward

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.bottom < 0:  # Remove bullet if it goes off the screen
            self.kill()

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("bomb.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(0, SCREEN_WIDTH),
                random.randint(-100, -20),  # Start above the screen
            )
        )
        self.speed = random.randint(5, 20)

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

# Cloud class
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load("cloud.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(0, SCREEN_WIDTH),
                random.randint(-100, -20),  # Start above the screen
            )
        )
        self.speed = random.randint(5, 20)

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

# Background class (for moving background)
class Background(pygame.sprite.Sprite):
    def __init__(self):
        super(Background, self).__init__()
        self.image = pygame.image.load("background.png").convert()
        self.rect1 = self.image.get_rect(topleft=(0, 0))
        self.rect2 = self.image.get_rect(topleft=(0, -self.rect1.height))
        self.speed = 1

    def update(self):
        self.rect1.y += self.speed
        self.rect2.y += self.speed
        if self.rect1.top >= SCREEN_HEIGHT:
            self.rect1.bottom = self.rect2.top
        if self.rect2.top >= SCREEN_HEIGHT:
            self.rect2.bottom = self.rect1.top

# Menu and Game Over functions
def show_menu():
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 74)
    title_text = font.render('Going Home', True, (255, 255, 255))
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))

    font = pygame.font.Font(None, 48)
    start_text = font.render('Start Game', True, (0, 255, 0))  # Start button in green
    start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(start_text, start_rect)
    
    exit_text = font.render('Exit', True, (255, 0, 0))  # Exit button in red
    exit_rect = exit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
    screen.blit(exit_text, exit_rect)
    
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if start_rect.collidepoint(mouse_pos):
                    return 'start'
                if exit_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    exit()

def show_game_over(score):
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 74)
    game_over_text = font.render('Game Over', True, (255, 255, 255))
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))

    font = pygame.font.Font(None, 48)
    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2))
    
    countdown_time = GAME_OVER_DELAY // 1000  # Convert delay to seconds
    start_time = pygame.time.get_ticks()

    while True:
        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
        remaining_time = countdown_time - elapsed_time

        if remaining_time <= 0:
            return  # Automatically return to the menu after the countdown

        countdown_text = font.render(f"Automatically quit in {remaining_time} seconds", True, (255, 255, 255))
        screen.blit(countdown_text, (SCREEN_WIDTH // 2 - countdown_text.get_width() // 2, SCREEN_HEIGHT // 2 + 100))
        
        pygame.display.flip()

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Jet Game')

# Load menu music
pygame.mixer.music.load("Apoxode_-_Electric_1.mp3")  # Menu music
pygame.mixer.music.play(-1)  # Loop indefinitely

# Main loop
running = True
while running:
    result = show_menu()  # Show the menu at the start

    if result == 'start':
        pygame.mixer.music.stop()  # Stop menu music
        pygame.mixer.music.load("sb_indreams.mp3")  # Game music
        pygame.mixer.music.play(loops=-1)
        
        # Create player
        player = Player()
        all_sprites = pygame.sprite.Group()
        player_bullets = pygame.sprite.Group()
        enemies = pygame.sprite.Group()
        clouds = pygame.sprite.Group()
        all_sprites.add(player)

        start_time = pygame.time.get_ticks()

        # Set up timers for spawning enemies and clouds
        ADDENEMY = pygame.USEREVENT + 1
        pygame.time.set_timer(ADDENEMY, 250)  # milliseconds
        ADDCLOUD = pygame.USEREVENT + 2
        pygame.time.set_timer(ADDCLOUD, 1000)

        background = Background()

        move_up_sound = pygame.mixer.Sound("Rising_putter.ogg")
        move_down_sound = pygame.mixer.Sound("Falling_putter.ogg")
        collision_sound = pygame.mixer.Sound("Collision.ogg")
        
        move_up_sound.set_volume(0.5)
        move_down_sound.set_volume(0.5)
        collision_sound.set_volume(0.5)

        clock = pygame.time.Clock()
        
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_UP:
                        player.jump()
                    if event.key == K_SPACE:
                        player.shoot()
                elif event.type == QUIT:
                    running = False
                elif event.type == ADDENEMY:
                    new_enemy = Enemy()
                    enemies.add(new_enemy)
                    all_sprites.add(new_enemy)
                elif event.type == ADDCLOUD:
                    new_cloud = Cloud()
                    clouds.add(new_cloud)
                    all_sprites.add(new_cloud)
            
            pressed_keys = pygame.key.get_pressed()
            player.update(pressed_keys)
            
            enemies.update()
            clouds.update()
            background.update() 
            player_bullets.update()
            
            # Check for bullet collisions with enemies
            for bullet in player_bullets:
                if pygame.sprite.spritecollideany(bullet, enemies):
                    bullet.kill()
                    for enemy in enemies:
                        if pygame.sprite.collide_rect(bullet, enemy):
                            enemy.kill()  # Remove enemy on collision
            
            # Check for collisions between player and enemies
            for enemy in enemies:
                if pygame.sprite.collide_rect(player, enemy):
                    enemy.kill()  # Remove enemy on collision
                    if not player.take_damage():
                        running = False  # End the game if the player has no lives left
                        collision_sound.play()
            
            # Draw the background first
            screen.blit(background.image, background.rect1)
            screen.blit(background.image, background.rect2)
            
            # Draw all sprites on top of the background
            for entity in all_sprites:
                screen.blit(entity.surf, entity.rect)
            
            # Draw player lives
            font = pygame.font.Font(None, 36)
            lives_text = font.render(f"Lives: {player.lives}", True, (255, 255, 255))
            screen.blit(lives_text, (10, 50))
            
            # Calculate points based on elapsed time
            elapsed_time = pygame.time.get_ticks() - start_time
            points = (elapsed_time * POINTS_PER_MS) // 1000
            time_text = font.render(f"Points: {points}", True, (255, 255, 255))
            screen.blit(time_text, (10, 10))
            
            pygame.display.flip()
            clock.tick(30)

        # Show the game over screen
        pygame.mixer.music.stop()
        pygame.mixer.music.load("menu_song.mp3")  # Game Over screen music
        pygame.mixer.music.play(-1)  # Loop indefinitely
        show_game_over(points)  # Show game over screen
