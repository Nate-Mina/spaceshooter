import pygame
import sys
import random
import math
import os
from player import Player
from enemy import Enemy
from bullet import Bullet, Explosion, PowerUp

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders")

# Colors
BLACK = (0, 0, 0)

# Clock
clock = pygame.time.Clock()

# Sound effects
SHOOT_SOUND = None
EXPLOSION_SOUND = None
POWERUP_SOUND = None
try:
    shoot_path = os.path.join('assets', 'shoot.wav')
    explosion_path = os.path.join('assets', 'explosion.wav')
    powerup_path = os.path.join('assets', 'powerup.wav')
    if os.path.exists(shoot_path):
        SHOOT_SOUND = pygame.mixer.Sound(shoot_path)
    if os.path.exists(explosion_path):
        EXPLOSION_SOUND = pygame.mixer.Sound(explosion_path)
    if os.path.exists(powerup_path):
        POWERUP_SOUND = pygame.mixer.Sound(powerup_path)
except Exception:
    pass

# Background music
try:
    music_path = os.path.join('assets', 'music.ogg')
    if os.path.exists(music_path):
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)  # Loop forever
except Exception:
    pass

# Game objects

player = None
enemies = []
bullets = []
explosions = []
powerups = []
powerup_timer = 0
rapid_fire = False
rapid_timer = 0
shield = False
shield_timer = 0
lives = 3
invulnerable = 0

# Score
score = 0
font = pygame.font.SysFont(None, 36)

# Starfield background with color and twinkle
class Star:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(0, SCREEN_HEIGHT)
        self.radius = random.choice([1, 1, 2])
        self.base_brightness = random.randint(120, 255)
        self.color = random.choice([
            (self.base_brightness, self.base_brightness, self.base_brightness),
            (self.base_brightness, self.base_brightness, 255),
            (self.base_brightness, 255, self.base_brightness),
            (255, self.base_brightness, self.base_brightness),
        ])
        self.twinkle_speed = random.uniform(0.02, 0.08)
        self.twinkle_phase = random.uniform(0, 6.28)
    def update(self, frame):
        # Twinkle by modulating brightness
        twinkle = int(40 * (1 + math.sin(self.twinkle_phase + frame * self.twinkle_speed)))
        r = min(255, max(80, self.color[0] + twinkle))
        g = min(255, max(80, self.color[1] + twinkle))
        b = min(255, max(80, self.color[2] + twinkle))
        return (r, g, b)
    def move(self):
        self.y += 2
        if self.y > SCREEN_HEIGHT:
            self.x = random.randint(0, SCREEN_WIDTH)
            self.y = 0

# Starfield setup
stars = [Star() for _ in range(100)]
frame_count = 0

# HUD assets and font
HUD_FONT = pygame.font.SysFont('consolas', 32, bold=True)
LIFE_ICON = None
try:
    icon_path = os.path.join('assets', 'life_icon.png')
    if os.path.exists(icon_path):
        LIFE_ICON = pygame.image.load(icon_path).convert_alpha()
        LIFE_ICON = pygame.transform.scale(LIFE_ICON, (28, 18))
except Exception:
    LIFE_ICON = None

def reset_game_state():
    global player, enemies, bullets, explosions, powerups, powerup_timer, rapid_fire, rapid_timer, shield, shield_timer, lives, invulnerable, score, frame_count, game_over, game_win
    player = Player(SCREEN_WIDTH, SCREEN_HEIGHT)
    enemies = [Enemy(x, 50) for x in range(50, SCREEN_WIDTH - 50, 100)]
    bullets = []
    explosions = []
    powerups = []
    powerup_timer = 0
    rapid_fire = False
    rapid_timer = 0
    shield = False
    shield_timer = 0
    lives = 3
    invulnerable = 0
    score = 0
    frame_count = 0
    game_over = False
    game_win = False

reset_game_state()


# Intro screen
show_intro = True
while show_intro:
    screen.fill((10, 10, 30))
    title = HUD_FONT.render("SPACE INVADERS", True, (0,255,200))
    shadow = HUD_FONT.render("SPACE INVADERS", True, (0,0,0))
    screen.blit(shadow, (SCREEN_WIDTH//2 - title.get_width()//2 + 2, 102))
    screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 100))
    instr = HUD_FONT.render("Press any key to start", True, (255,255,255))
    screen.blit(instr, (SCREEN_WIDTH//2 - instr.get_width()//2, 220))
    controls = font.render("Arrows: Move   Space: Shoot   R: Restart   Q/Esc: Quit", True, (200,200,255))
    screen.blit(controls, (SCREEN_WIDTH//2 - controls.get_width()//2, 300))
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            show_intro = False

# Game loop
running = True
game_over = False
game_win = False
while running:
    if not game_over and not game_win:
        screen.fill(BLACK)
        frame_count += 1
        # Update and draw colorful, twinkling stars
        for star in stars:
            star.move()
            color = star.update(frame_count)
            pygame.draw.circle(screen, color, (star.x, int(star.y)), star.radius)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Power-up timers
        if rapid_fire:
            rapid_timer -= 1
            if rapid_timer <= 0:
                rapid_fire = False
        if shield:
            shield_timer -= 1
            if shield_timer <= 0:
                shield = False

        if invulnerable > 0:
            invulnerable -= 1

        # Player controls
        keys = pygame.key.get_pressed()
        can_shoot = rapid_fire or pygame.time.get_ticks() % 10 == 0
        if keys[pygame.K_LEFT]:
            player.move_left()
        if keys[pygame.K_RIGHT]:
            player.move_right()
        if keys[pygame.K_UP]:
            player.move_up()
        if keys[pygame.K_DOWN]:
            player.move_down()
        if keys[pygame.K_SPACE] and can_shoot:
            if len(bullets) < (10 if rapid_fire else 5):
                bullets.append(Bullet(player.x + player.width // 2, player.y))
                if SHOOT_SOUND:
                    SHOOT_SOUND.play()

        # Update bullets
        for bullet in bullets[:]:
            bullet.move()
            if bullet.y < 0:
                bullets.remove(bullet)

        # Update enemies
        for enemy in enemies:
            enemy.update()

        # Update explosions
        for explosion in explosions[:]:
            explosion.update()
            if not explosion.active:
                explosions.remove(explosion)

        # Update powerups
        for powerup in powerups[:]:
            powerup.move()
            if not powerup.active:
                powerups.remove(powerup)
            elif (player.x < powerup.x < player.x + player.width and
                  player.y < powerup.y < player.y + player.height):
                if POWERUP_SOUND:
                    POWERUP_SOUND.play()
                if powerup.type == 'rapid':
                    rapid_fire = True
                    rapid_timer = 300
                elif powerup.type == 'shield':
                    shield = True
                    shield_timer = 300
                elif powerup.type == 'life':
                    lives += 1
                powerups.remove(powerup)

        # Collision detection
        for bullet in bullets[:]:
            for enemy in enemies[:]:
                if bullet.collides_with(enemy):
                    bullets.remove(bullet)
                    explosions.append(Explosion(enemy.x + enemy.width // 2, enemy.y + enemy.height // 2))
                    if EXPLOSION_SOUND:
                        EXPLOSION_SOUND.play()
                    # 1 in 3 chance to spawn a powerup
                    if random.randint(1,3) == 1:
                        powerups.append(PowerUp(enemy.x + enemy.width // 2, enemy.y + enemy.height // 2))
                    enemies.remove(enemy)
                    score += 100
                    break

        # Enemy-player collision
        for enemy in enemies[:]:
            if (player.x < enemy.x + enemy.width and
                player.x + player.width > enemy.x and
                player.y < enemy.y + enemy.height and
                player.y + player.height > enemy.y):
                if not shield and invulnerable == 0:
                    lives -= 1
                    invulnerable = 90  # 1.5 seconds at 60 FPS
                    explosions.append(Explosion(player.x + player.width//2, player.y + player.height//2))
                    if EXPLOSION_SOUND:
                        EXPLOSION_SOUND.play()
                    if lives <= 0:
                        game_over = True
                # Optionally, remove the enemy on collision
                # enemies.remove(enemy)

        # Draw game objects
        player.draw(screen)
        for enemy in enemies:
            enemy.draw(screen)
        for bullet in bullets:
            bullet.draw(screen)
        for explosion in explosions:
            explosion.draw(screen)
        for powerup in powerups:
            powerup.draw(screen)

        # Draw score with shadow
        score_text = HUD_FONT.render(f"Score: {score}", True, (255,255,255))
        shadow = HUD_FONT.render(f"Score: {score}", True, (0,0,0))
        screen.blit(shadow, (12, 12))
        screen.blit(score_text, (10, 10))

        # Draw lives as icons or text
        if LIFE_ICON:
            for i in range(lives):
                screen.blit(LIFE_ICON, (10 + i*34, 50))
        else:
            life_text = HUD_FONT.render(f"Lives: {lives}", True, (0,255,0))
            shadow2 = HUD_FONT.render(f"Lives: {lives}", True, (0,0,0))
            screen.blit(shadow2, (12, 52))
            screen.blit(life_text, (10, 50))

        # Draw power-up status
        if rapid_fire:
            rapid_text = HUD_FONT.render("RAPID FIRE!", True, (0,200,255))
            screen.blit(rapid_text, (SCREEN_WIDTH-220, 10))
        if shield:
            shield_text = HUD_FONT.render("SHIELD!", True, (0,255,255))
            screen.blit(shield_text, (SCREEN_WIDTH-160, 50))

        # Draw shield effect and invulnerability blink
        if shield or (invulnerable > 0 and (frame_count//5)%2 == 0):
            pygame.draw.ellipse(screen, (0,255,255), (player.x-10, player.y-10, player.width+20, player.height+20), 3)

        # Check for game over
        if not enemies:
            game_win = True

    else:
        # Game Over/Win screen
        screen.fill((10, 10, 30))
        msg = "You Win!" if game_win else "Game Over!"
        msg_text = HUD_FONT.render(msg, True, (255, 255, 0))
        msg_shadow = HUD_FONT.render(msg, True, (0,0,0))
        screen.blit(msg_shadow, (SCREEN_WIDTH//2 - msg_text.get_width()//2 + 2, SCREEN_HEIGHT//2 - 52))
        screen.blit(msg_text, (SCREEN_WIDTH//2 - msg_text.get_width()//2, SCREEN_HEIGHT//2 - 54))
        restart_text = HUD_FONT.render("Press R to Restart or Q/Esc to Quit", True, (200, 200, 255))
        screen.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, SCREEN_HEIGHT//2 + 10))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game_state()
                if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()