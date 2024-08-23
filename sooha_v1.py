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
                self.kill()  # Remove the player when lives reach 0
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

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Jet Game')

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

# Load and play background music
pygame.mixer.music.load("Apoxode_-_Electric_1.mp3")
pygame.mixer.music.play(loops=-1)

# Load sound effects
move_up_sound = pygame.mixer.Sound("Rising_putter.ogg")
move_down_sound = pygame.mixer.Sound("Falling_putter.ogg")
collision_sound = pygame.mixer.Sound("Collision.ogg")

# Set sound volumes
move_up_sound.set_volume(0.5)
move_down_sound.set_volume(0.5)
collision_sound.set_volume(0.5)

# Main game loop
clock = pygame.time.Clock()
running = True
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
    player_bullets.update()

    for bullet in player_bullets:
        if pygame.sprite.spritecollideany(bullet, enemies):
            bullet.kill()
            for enemy in enemies:
                if pygame.sprite.collide_rect(bullet, enemy):
                    enemy.kill()  # Remove enemy on collision

    if pygame.sprite.spritecollideany(player, enemies):
        if not player.take_damage():
            running = False  # End the game if the player has no lives left
            collision_sound.play()

    screen.fill((0, 0, 0))  # Clear screen with black
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # Draw player lives
    font = pygame.font.Font(None, 36)
    lives_text = font.render(f"Lives: {player.lives}", True, (255, 255, 255))
    screen.blit(lives_text, (10, 50))

    pygame.display.flip()
    clock.tick(30)

pygame.mixer.music.stop()
pygame.mixer.quit()
pygame.quit()