# enemy.py
import pygame
import math
import random

class Enemy(pygame.sprite.Sprite):
    def __init__(self, start_pos, size, speed, image):
        super().__init__()
        self.pos = pygame.Vector2(start_pos)
        self.size = size
        self.speed = speed
        self.image = image
        self.rect = self.image.get_rect(center=(int(self.pos.x), int(self.pos.y)))
        self.radius = size // 2

    def update(self, player_pos):
        """Cập nhật vị trí để di chuyển về phía người chơi."""
        if self.pos.distance_to(player_pos) > 0.1:
            direction = (player_pos - self.pos).normalize()
            self.pos.x += direction.x * self.speed
            self.pos.y += direction.y * self.speed
            self.rect.center = (int(self.pos.x), int(self.pos.y))

    def check_collision_with_player(self, player_pos, player_hit_radius=40):
        """Kiểm tra va chạm với người chơi."""
        return self.pos.distance_to(player_pos) < player_hit_radius

    def check_collision_with_bullet(self, bullet_pos, bullet_hit_radius=40):
        """Kiểm tra va chạm với đạn."""
        return self.pos.distance_to(bullet_pos) < bullet_hit_radius

    def draw(self, screen):
        """Vẽ kẻ địch lên màn hình. (Không cần thiết nếu dùng Group.draw())"""
        screen.blit(self.image, self.rect)