import pygame
import sys
import math
import random

pygame.init()
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Top-Down Shooter")
clock = pygame.time.Clock()

# --- Game States ---
MENU = 0
PLAYING = 1
GAME_OVER = 2
game_state = MENU

# --- Player ---
player_pos = pygame.Vector2(WIDTH // 2, HEIGHT // 2)
player_speed = 5
player_size = 40
player_health = 100

# --- Bullet ---
bullets = []
bullet_speed = 15
shoot_cooldown = 0

# --- Enemies ---
enemies = []
enemy_size = 40
enemy_speed = 2
spawn_delay = 60
spawn_timer = 0

font = pygame.font.SysFont(None, 48)
small_font = pygame.font.SysFont(None, 32)

def reset_game():
    global player_pos, player_health, bullets, enemies, spawn_timer
    player_pos = pygame.Vector2(WIDTH // 2, HEIGHT // 2)
    player_health = 100
    bullets = []
    enemies = []
    spawn_timer = 0


def spawn_enemy():
    side = random.choice(["top","bottom","left","right"])
    if side == "top":    pos = [random.randint(0, WIDTH), -50]
    if side == "bottom": pos = [random.randint(0, WIDTH), HEIGHT+50]
    if side == "left":   pos = [-50, random.randint(0, HEIGHT)]
    if side == "right":  pos = [WIDTH+50, random.randint(0, HEIGHT)]
    enemies.append(pygame.Vector2(pos))


# ====================================================
# GAME LOOP
# ====================================================
while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    # ================= MENU SCREEN =================
    if game_state == MENU:
        screen.fill((20, 20, 20))
        title = font.render("TOP-DOWN SHOOTER", True, (255,255,255))
        play_text = small_font.render("Press SPACE to PLAY", True, (200,200,50))
        quit_text = small_font.render("Press ESC to QUIT", True, (200,50,50))

        screen.blit(title, (WIDTH//2 - 200, HEIGHT//3))
        screen.blit(play_text, (WIDTH//2 - 150, HEIGHT//2))
        screen.blit(quit_text, (WIDTH//2 - 130, HEIGHT//2 + 50))

        if keys[pygame.K_SPACE]:
            reset_game()
            game_state = PLAYING

        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()

        pygame.display.flip()
        clock.tick(60)
        continue

    # ================= GAME OVER SCREEN =================
    if game_state == GAME_OVER:
        screen.fill((0, 0, 0))
        game_over_text = font.render("GAME OVER", True, (255, 50, 50))
        retry_text = small_font.render("Press SPACE to RESTART", True, (255,255,255))

        screen.blit(game_over_text, (WIDTH//2 - 100, HEIGHT//2 - 20))
        screen.blit(retry_text, (WIDTH//2 - 160, HEIGHT//2 + 40))

        if keys[pygame.K_SPACE]:
            reset_game()
            game_state = PLAYING

        pygame.display.flip()
        clock.tick(60)
        continue

    # ================= GAMEPLAY =================

    # --- Player movement ---
    if keys[pygame.K_w]: player_pos.y -= player_speed
    if keys[pygame.K_s]: player_pos.y += player_speed
    if keys[pygame.K_a]: player_pos.x -= player_speed
    if keys[pygame.K_d]: player_pos.x += player_speed

    player_pos.x = max(player_size, min(WIDTH-player_size, player_pos.x))
    player_pos.y = max(player_size, min(HEIGHT-player_size, player_pos.y))

    # --- Shooting ---
    mouse_pressed = pygame.mouse.get_pressed()
    if mouse_pressed[0] and shoot_cooldown == 0:
        mx, my = pygame.mouse.get_pos()
        angle = math.atan2(my - player_pos.y, mx - player_pos.x)
        bullets.append([pygame.Vector2(player_pos), angle])
        shoot_cooldown = 10
    if shoot_cooldown > 0:
        shoot_cooldown -= 1

    # Spawn enemies
    spawn_timer += 1
    if spawn_timer >= spawn_delay:
        spawn_timer = 0
        spawn_enemy()

    # Bullets move
    for b in bullets:
        b[0].x += math.cos(b[1]) * bullet_speed
        b[0].y += math.sin(b[1]) * bullet_speed
    bullets = [b for b in bullets if 0 < b[0].x < WIDTH and 0 < b[0].y < HEIGHT]

    # Enemy move & hit player
    for e in enemies[:]:
        direction = (player_pos - e).normalize()
        e.x += direction.x * enemy_speed
        e.y += direction.y * enemy_speed

        if e.distance_to(player_pos) < player_size:
            enemies.remove(e)
            player_health -= 10
            if player_health <= 0:
                game_state = GAME_OVER

    # Bullet hits enemy
    for b in bullets[:]:
        for e in enemies[:]:
            if e.distance_to(b[0]) < enemy_size:
                bullets.remove(b)
                enemies.remove(e)
                break

    # --- DRAW GAME ---
    screen.fill((30, 30, 30))
    pygame.draw.circle(screen, (0, 200, 255), player_pos, player_size)

    for b in bullets:
        pygame.draw.circle(screen, (255,255,0), b[0], 6)

    for e in enemies:
        pygame.draw.rect(screen, (200,50,50), (*e, enemy_size, enemy_size))

    hp_text = small_font.render(f"HP: {player_health}", True, (255,255,255))
    screen.blit(hp_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)
