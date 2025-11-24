# npc.py
import pygame
import os
import sys

class NPC:
    def __init__(self, x, y, size=60):
        self.pos = pygame.Vector2(x, y)
        self.size = size
        self.image_list = []
        self.current_image = 0
        self.image_timer = 0
        self.IMAGE_DELAY = 60
        self.load_images()
    
    def load_images(self):
        base_path = os.path.join(os.path.dirname(__file__), "npc")
        image_names = ["down", "up", "left", "right"]  # ← Dùng .png
        for name in image_names:
            img_path = os.path.join(base_path, f"{name}.png")  # ← .png
            if not os.path.exists(img_path):
                print(f"THIẾU ẢNH: {img_path}")
                print("→ Đặt 4 file: down.png, up.png, left.png, right.png vào thư mục 'npc/'")
                pygame.quit()
                sys.exit()
            try:
                img = pygame.image.load(img_path).convert_alpha()
                img = pygame.transform.scale(img, (self.size, self.size))
                self.image_list.append(img)
                print(f"Loaded NPC {name}.png")
            except Exception as e:
                print(f"LỖI LOAD {img_path}: {e}")
                pygame.quit()
                sys.exit()
    
    def update(self):
        self.image_timer += 1
        if self.image_timer >= self.IMAGE_DELAY:
            self.current_image = (self.current_image + 1) % 4
            self.image_timer = 0
    
    def draw(self, screen):
        img = self.image_list[self.current_image]
        screen.blit(img, (self.pos.x - self.size//2, self.pos.y - self.size//2))
    
    def get_rect(self):
        return pygame.Rect(self.pos.x - self.size//2, self.pos.y - self.size//2, self.size, self.size)
    
    def is_near(self, player_pos):
        return player_pos.distance_to(self.pos) < 150