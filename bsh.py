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

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Going Home')

# Create sprite groups
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
player_bullets = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

# Create player
player = Player()
all_sprites.add(player)

# Set up timers for spawning enemies and clouds
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)  # milliseconds
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)

background = Background()

# Load and play background music
menu_music = pygame.mixer.music.load("Apoxode_-_Electric_1.mp3")
game_music = pygame.mixer.music.load("sb_indreams.mp3")
pygame.mixer.music.play(loops=-1, start=0)  # Start menu music

# Load sound effects
move_up_sound = pygame.mixer.Sound("Rising_putter.ogg")
move_down_sound = pygame.mixer.Sound("Falling_putter.ogg")
collision_sound = pygame.mixer.Sound("Collision.ogg")

# Set sound volumes
move_up_sound.set_volume(0.5)
move_down_sound.set_volume(0.5)
collision_sound.set_volume(0.5)

start_time = pygame.time.get_ticks()
points = 0  # Initialize points

# Define game states
START_MENU = "start_menu"
GAME_RUNNING = "game_running"
GAME_OVER = "game_over"
current_state = START_MENU

# Button class for menu and game over screens
class Button:
    def __init__(self, text, width, height, pos, elevation):
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elecation = elevation
        self.original_y_pos = pos[1]

        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = "#475F77"

        self.bottom_rect = pygame.Rect(pos, (width, height))
        self.bottom_color = "#354B5E"

        self.text_surf = pygame.font.Font(None, 30).render(text, True, "#FFFFFF")
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

    def draw(self):
        # Elevation logic
        self.top_rect.y = self.original_y_pos - self.dynamic_elecation
        self.text_rect.center = self.top_rect.center

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elecation

        pygame.draw.rect(screen, self.bottom_color, self.bottom_rect)
        pygame.draw.rect(screen, self.top_color, self.top_rect)
        screen.blit(self.text_surf, self.text_rect)

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elecation = 0
                return True
            self.dynamic_elecation = self.elevation
        return False

# Create buttons
start_button = Button("Start", 200, 50, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 - 25), 5)
return_to_menu_button = Button("Return to Menu", 200, 50, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 - 25), 5)
exit_button = Button("Exit", 200, 50, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 25), 5)

# Main game loop
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            if event.key == K_UP and current_state == GAME_RUNNING:
                player.jump()
            if event.key == K_SPACE and current_state == GAME_RUNNING:
                player.shoot()
        elif event.type == QUIT:
            running = False
        elif event.type == ADDENEMY and current_state == GAME_RUNNING:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
        elif event.type == ADDCLOUD and current_state == GAME_RUNNING:
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)

    if current_state == START_MENU:
        screen.fill((0, 0, 0))  # Fill screen with black
        pygame.mixer.music.load("Apoxode_-_Electric_1.mp3")
        pygame.mixer.music.play(loops=-1, start=0)  # Play menu music

        # Display game title
        title_font = pygame.font.Font(None, 74)
        title_text = title_font.render("Going Home", True, (255, 255, 255))
        screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, SCREEN_HEIGHT//4))

        # Draw start button
        if start_button.check_click():
            current_state = GAME_RUNNING  # Change state to start the game
            pygame.mixer.music.stop()
            pygame.mixer.music.load("sb_indreams.mp3")
            pygame.mixer.music.play(loops=-1, start=0)  # Play game music
            start_time = pygame.time.get_ticks()  # Reset the start time when the game begins
            points = 0  # Reset points when starting a new game
            player.lives = 3  # Reset player lives when starting a new game

        start_button.draw()

    elif current_state == GAME_RUNNING:
        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys)

        enemies.update()
        clouds.update()
        background.update() 
        player_bullets.update()

        # Update points based on time
        current_time = pygame.time.get_ticks()
        points = current_time - start_time

        # Check for bullet collisions with enemies
        for bullet in player_bullets:
            if pygame.sprite.spritecollideany(bullet, enemies):
                bullet.kill()
                for enemy in enemies:
                    if pygame.sprite.collide_rect(bullet, enemy):
                        enemy.kill()  # Remove enemy on collision

        # Check for collisions between player and enemies
        if pygame.sprite.spritecollideany(player, enemies):
            if not player.take_damage():
                current_state = GAME_OVER  # Switch to game over screen
                pygame.mixer.music.stop()
                pygame.mixer.music.load("Apoxode_-_Electric_1.mp3")
                pygame.mixer.music.play(loops=-1, start=0)  # Play menu music again
                collision_sound.play()

        # Draw the background first
        screen.blit(background.image, background.rect1)
        screen.blit(background.image, background.rect2)

        # Draw all sprites on top of the background
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)
        
        # Draw player lives and points
        font = pygame.font.Font(None, 36)
        lives_text = font.render(f"Lives: {player.lives}", True, (255, 255, 255))
        screen.blit(lives_text, (10, 50))
        
        time_text = font.render(f"Time: {(current_time - start_time) // 1000}s", True, (255, 255, 255))
        points_text = font.render(f"Points: {points}", True, (255, 255, 255))
        screen.blit(time_text, (10, 10))
        screen.blit(points_text, (10, 90))

    elif current_state == GAME_OVER:
        screen.fill((0, 0, 0))  # Fill screen with black

        # Display game over text
        game_over_font = pygame.font.Font(None, 74)
        game_over_text = game_over_font.render("Game Over", True, (255, 0, 0))
        screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, SCREEN_HEIGHT//4))

        # Draw buttons
        if return_to_menu_button.check_click():
            current_state = START_MENU
            points = 0  # Reset points when returning to menu
            player.lives = 3  # Reset player lives when returning to menu
            pygame.mixer.music.stop()
            pygame.mixer.music.load("Apoxode_-_Electric_1.mp3")
            pygame.mixer.music.play(loops=-1, start=0)  # Play menu music

        if exit_button.check_click():
            pygame.quit()
            running = False

        return_to_menu_button.draw()
        exit_button.draw()

    pygame.display.flip()
    clock.tick(30)

pygame.mixer.music.stop()
pygame.mixer.quit()
pygame.quit()
