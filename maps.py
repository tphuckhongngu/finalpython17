# maps.py
import pygame
import os

class MapManager:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.maps = {}  # Lưu tất cả maps: {"map1": img, "map2": img}
        self.current_map = None
        self.current_map_name = None
        
    def load_all_maps(self, maps_folder="maps"):
        """Load tất cả file ảnh trong thư mục maps/"""
        if not os.path.exists(maps_folder):
            print(f"❌ Thư mục '{maps_folder}' không tồn tại!")
            return
            
        map_files = [f for f in os.listdir(maps_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        for file in map_files:
            map_name = os.path.splitext(file)[0]  # Tên map = tên file (không .png)
            map_path = os.path.join(maps_folder, file)
            
            try:
                img = pygame.image.load(map_path).convert()
                img = pygame.transform.scale(img, (self.width, self.height))
                self.maps[map_name] = img
                print(f"✅ Loaded map: {map_name}")
            except Exception as e:
                print(f"❌ Lỗi load {file}: {e}")
        
        if self.maps:
            self.set_map(list(self.maps.keys())[0])  # Tự load map đầu tiên
    
    def set_map(self, map_name):
        """Chuyển sang map khác"""
        if map_name in self.maps:
            self.current_map = self.maps[map_name]
            self.current_map_name = map_name
            print(f"🎮 Chuyển sang map: {map_name}")
        else:
            print(f"❌ Không tìm thấy map: {map_name}")
    
    def draw(self, screen):
        """Vẽ map hiện tại"""
        if self.current_map:
            screen.blit(self.current_map, (0, 0))
        else:
            screen.fill((30, 30, 30))  # Nền xám mặc định
    
    def get_current_map_name(self):
        return self.current_map_name
    
    def list_maps(self):
        """Liệt kê tất cả maps"""
        return list(self.maps.keys())