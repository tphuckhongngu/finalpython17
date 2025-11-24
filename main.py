import pygame
import sys
sys.stdout.reconfigure(encoding='utf-8')
import math
import random
import os
from maps import MapManager
from npc import NPC





# Khởi tạo Pygame
pygame.init()

# Cài đặt màn hình
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Top-Down Shooter - NPC Chuột + Dialog 3s")
clock = pygame.time.Clock()

# --- Game States ---
MENU = 0
PLAYING = 1
GAME_OVER = 2
game_state = MENU

# --- Load Player Animations ---
player_animations = {"down": [], "up": [], "left": [], "right": []}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
base_path = os.path.join(BASE_DIR, "player")

if not os.path.exists(base_path):
    print(f"Thư mục '{base_path}' không tồn tại!")
    pygame.quit()
    sys.exit()

for direction in player_animations:
    dir_path = os.path.join(base_path, direction)
    if not os.path.exists(dir_path):
        print(f"Thư mục '{dir_path}' không tồn tại!")
        continue
    for i in range(4):
        img_path = os.path.join(dir_path, f"{i}.png")
        if os.path.exists(img_path):
            try:
                img = pygame.image.load(img_path).convert_alpha()
                img = pygame.transform.scale(img, (80, 80))
                player_animations[direction].append(img)
            except Exception as e:
                print(f"Không tải được {img_path}: {e}")
                placeholder = pygame.Surface((80, 80))
                placeholder.fill((100, 100, 255))
                player_animations[direction].append(placeholder)
        else:
            placeholder = pygame.Surface((80, 80))
            placeholder.fill((255, 100, 100))
            player_animations[direction].append(placeholder)

for direction in player_animations:
    if not player_animations[direction]:
        placeholder = pygame.Surface((80, 80))
        placeholder.fill((150, 150, 150))
        player_animations[direction] = [placeholder] * 4

# --- Player ---
player_pos = pygame.Vector2(WIDTH // 2, HEIGHT // 2)
player_speed = 5
player_health = 100
current_direction = "down"
current_frame = 0
animation_cooldown = 0
ANIMATION_SPEED = 8

# --- Map Manager ---
map_path = os.path.join(BASE_DIR, "maps")
map_manager = MapManager(WIDTH, HEIGHT)
map_manager.load_all_maps(map_path)

# --- Bullet ---
bullets = []
bullet_speed = 15
shoot_cooldown = 0

# --- Enemies ---
enemies = []
enemy_size = 50
enemy_speed = 2
spawn_delay = 60
spawn_timer = 0
enemy_img = pygame.Surface((enemy_size, enemy_size), pygame.SRCALPHA)
pygame.draw.circle(enemy_img, (200, 50, 50), (enemy_size//2, enemy_size//2), enemy_size//2 - 5)

# --- Fonts ---
font = pygame.font.SysFont(None, 48)
small_font = pygame.font.SysFont(None, 32)

# --- NPC ---
npcs = []
dialog_active = False
dialog_text = ""
dialog_timer = 0
DIALOG_DURATION = 180  # 3 giây = 180 frame (60 FPS)

# --- Functions ---
def reset_game():
    global player_pos, player_health, bullets, enemies, spawn_timer
    global current_direction, current_frame, shoot_cooldown, npcs
    global dialog_active, dialog_timer

    player_pos = pygame.Vector2(WIDTH // 2, HEIGHT // 2)
    player_health = 100
    bullets = []
    enemies = []
    spawn_timer = 0
    current_direction = "down"
    current_frame = 0
    shoot_cooldown = 0
    npcs.clear()
    dialog_active = False
    dialog_timer = 0

    # Spawn 1 NPC
    npcs.append(NPC(300, HEIGHT // 2))

def spawn_enemy():
    side = random.choice(["top", "bottom", "left", "right"])
    if side == "top":
        pos = [random.randint(0, WIDTH), -enemy_size]
    elif side == "bottom":
        pos = [random.randint(0, WIDTH), HEIGHT + enemy_size]
    elif side == "left":
        pos = [-enemy_size, random.randint(0, HEIGHT)]
    elif side == "right":
        pos = [WIDTH + enemy_size, random.randint(0, HEIGHT)]
    enemies.append(pygame.Vector2(pos))

# ====================================================
# MAIN GAME LOOP
# ====================================================
while True:
    # --- Xử lý sự kiện ---
    mouse_clicked = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Chuột trái
                mouse_clicked = True

    keys = pygame.key.get_pressed()
    mouse_buttons = pygame.mouse.get_pressed()

    # ================= MENU SCREEN =================
    if game_state == MENU:
        screen.fill((20, 20, 20))
        title = font.render("TOP-DOWN SHOOTER", True, (255, 255, 255))
        play_text = small_font.render("Press SPACE to PLAY", True, (200, 200, 50))
        quit_text = small_font.render("Press ESC to QUIT", True, (200, 50, 50))

        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 3))
        screen.blit(play_text, (WIDTH // 2 - play_text.get_width() // 2, HEIGHT // 2))
        screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 2 + 50))

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
        retry_text = small_font.render("Press SPACE to RESTART", True, (255, 255, 255))

        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 40))
        screen.blit(retry_text, (WIDTH // 2 - retry_text.get_width() // 2, HEIGHT // 2 + 20))

        if keys[pygame.K_SPACE]:
            reset_game()
            game_state = PLAYING

        pygame.display.flip()
        clock.tick(60)
        continue

    # ================= GAMEPLAY =================
    # --- Player Movement & Animation ---
    move_x = move_y = 0
    if keys[pygame.K_w]: move_y -= player_speed
    if keys[pygame.K_s]: move_y += player_speed
    if keys[pygame.K_a]: move_x -= player_speed
    if keys[pygame.K_d]: move_x += player_speed

    moving = move_x != 0 or move_y != 0
    if moving:
        player_pos.x += move_x
        player_pos.y += move_y
        if abs(move_x) > abs(move_y):
            current_direction = "right" if move_x > 0 else "left"
        else:
            current_direction = "down" if move_y > 0 else "up"

        animation_cooldown += 1
        if animation_cooldown >= ANIMATION_SPEED:
            current_frame = (current_frame + 1) % 4
            animation_cooldown = 0
    else:
        current_frame = 0
        current_direction = "down"

    player_pos.x = max(40, min(WIDTH - 40, player_pos.x))
    player_pos.y = max(40, min(HEIGHT - 40, player_pos.y))

    # --- Shooting ---
    if mouse_buttons[0] and shoot_cooldown == 0:
        mx, my = pygame.mouse.get_pos()
        angle = math.atan2(my - player_pos.y, mx - player_pos.x)
        bullets.append([pygame.Vector2(player_pos), angle])
        shoot_cooldown = 10
    if shoot_cooldown > 0:
        shoot_cooldown -= 1

    # --- Spawn Enemies ---
    spawn_timer += 1
    if spawn_timer >= spawn_delay:
        spawn_timer = 0
        spawn_enemy()

    # --- Update Bullets ---
    for bullet in bullets[:]:
        bullet[0].x += math.cos(bullet[1]) * bullet_speed
        bullet[0].y += math.sin(bullet[1]) * bullet_speed
        if not (0 < bullet[0].x < WIDTH and 0 < bullet[0].y < HEIGHT):
            bullets.remove(bullet)

    # --- Update Enemies ---
    for enemy in enemies[:]:
        if player_pos.distance_to(enemy) > 0.1:
            direction = (player_pos - enemy).normalize()
            enemy.x += direction.x * enemy_speed
            enemy.y += direction.y * enemy_speed
        if enemy.distance_to(player_pos) < 40:
            enemies.remove(enemy)
            player_health -= 10
            if player_health <= 0:
                player_health = 0
                game_state = GAME_OVER

    # --- Bullet - Enemy Collision ---
    for bullet in bullets[:]:
        hit = False
        for enemy in enemies[:]:
            if enemy.distance_to(bullet[0]) < 40:
                if bullet in bullets:
                    bullets.remove(bullet)
                if enemy in enemies:
                    enemies.remove(enemy)
                hit = True
                break
        if hit:
            break

    # --- Update NPC Animation ---
    for npc in npcs:
        npc.update()

    # --- NPC Tương tác bằng chuột ---
    if mouse_clicked and not dialog_active:
        for npc in npcs:
            if npc.is_near(player_pos):
                dialog_active = True
                dialog_text = "Chào bạn! NPC đã nói!"
                dialog_timer = DIALOG_DURATION
                break

    # --- Cập nhật timer dialog ---
    if dialog_active:
        dialog_timer -= 1
        if dialog_timer <= 0:
            dialog_active = False

    # --- DRAW EVERYTHING ---
    map_manager.draw(screen)

    # Vẽ nhân vật
    current_img = player_animations[current_direction][current_frame]
    screen.blit(current_img, (player_pos.x - 40, player_pos.y - 40))

    # Vẽ đạn
    for bullet in bullets:
        pygame.draw.circle(screen, (255, 255, 0), (int(bullet[0].x), int(bullet[0].y)), 6)

    # Vẽ kẻ địch
    for enemy in enemies:
        screen.blit(enemy_img, (enemy.x - enemy_size // 2, enemy.y - enemy_size // 2))

    # Vẽ NPC
    for npc in npcs:
        npc.draw(screen)

    # Vẽ HP
    hp_text = small_font.render(f"HP: {player_health}", True, (255, 255, 255))
    screen.blit(hp_text, (10, 10))

    # Dialog NPC (biến mất sau 3s)
    if dialog_active and npcs:
        npc = npcs[0]
        dialog_surf = small_font.render(dialog_text, True, (255, 255, 200))
        bg_rect = pygame.Rect(npc.pos.x - 140, npc.pos.y - 120, 280, 60)
        pygame.draw.rect(screen, (0, 0, 50), bg_rect, border_radius=12)
        pygame.draw.rect(screen, (255, 255, 255), bg_rect, 3, border_radius=12)
        screen.blit(dialog_surf, (npc.pos.x - dialog_surf.get_width() // 2, npc.pos.y - 95))

    pygame.display.flip()
    clock.tick(60)