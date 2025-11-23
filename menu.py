#!/usr/bin/env python3
"""
Chiến Binh Chống Rác Thải - Màn hình menu & demo gameplay console
Tác giả: ...
Mô tả: Một chương trình Python chạy trên terminal mô phỏng menu dựa theo cốt truyện.
- Ngôn ngữ: Tiếng Việt
- Chạy: python3 menu.py
"""

import random
import sys
import time

# ---------- Dữ liệu trò chơi mẫu ----------
areas = {
    'Thành phố đổ nát': {'pollution': 90, 'cleared': False},
    'Bờ biển dầu loang': {'pollution': 95, 'cleared': False},
    'Rừng cháy trụi': {'pollution': 85, 'cleared': False},
    'Hang động cổ': {'pollution': 60, 'cleared': False},
}

player = {
    'name': 'Chiến Binh',
    'age': 16,
    'hp': 100,
    'power': 'Sức mạnh Phân Loại',
    'inventory': {'hữu cơ': 0, 'tái chế': 0, 'độc hại': 0, 'vũ khí': []},
}

environment_level = 0  # điểm mô tả mức hồi sinh môi trường (tăng khi dọn dẹp)

# ---------- Hỗ trợ hiển thị ----------
def slow_print(text, delay=0.02):
    for ch in text:
        print(ch, end='', flush=True)
        time.sleep(delay)
    print()


def header():
    print('=' * 60)
    print('CHIẾN BINH CHỐNG RÁC THẢI'.center(60))
    print('Năm: 2077  —  Trái Đất sau thảm họa'.center(60))
    print('=' * 60)


# ---------- Menu chính ----------

def main_menu():
    while True:
        header()
        print('1) Bắt đầu hành trình')
        print('2) Hướng dẫn (cách chơi)')
        print('3) Trạng thái nhân vật & vùng')
        print('4) Thử phân loại rác (minigame)')
        print('5) Thoát')
        choice = input('\nChọn (1-5): ').strip()
        if choice == '1':
            start_journey()
        elif choice == '2':
            instructions()
        elif choice == '3':
            status()
        elif choice == '4':
            classify_minigame()
        elif choice == '5':
            slow_print('Tạm biệt — hãy bảo vệ Trái Đất nhé!')
            sys.exit(0)
        else:
            print('Lựa chọn không hợp lệ. Thử lại.')
        input('\nNhấn Enter để quay lại menu...')


# ---------- Hướng dẫn ----------

def instructions():
    header()
    slow_print('''
Cốt truyện tóm tắt: Bạn là chàng trai 16 tuổi thức dậy trong năm 2077. Trái Đất bị ô nhiễm nặng, quái vật rác xuất hiện.
Bạn khám phá, thu thập rác và sử dụng "Máy Tái Tạo Xanh" để phân loại rác:
- Hữu cơ: chế tạo phân bón để trồng cây, tạo hàng rào sống.
- Tái chế: chế ra vũ khí và khiên từ kim loại, nhựa, giấy.
- Độc hại: trung hòa để tiêu diệt quái vật mạnh.

Mục tiêu: Dọn sạch các khu vực, giảm mức ô nhiễm và hồi sinh môi trường.
''')


# ---------- Trạng thái ----------

def status():
    header()
    print(f"Tên: {player['name']}  |  Tuổi: {player['age']}  |  HP: {player['hp']}")
    print('Sức mạnh:', player['power'])
    print('\nKho đồ:')
    for k, v in player['inventory'].items():
        print(f" - {k}: {v}")
    print('\nCác khu vực:')
    for name, info in areas.items():
        status = 'Đã sạch' if info['cleared'] else f"Ô nhiễm {info['pollution']}%"
        print(f" - {name}: {status}")
    print(f'\nMức hồi sinh môi trường: {environment_level}%')


# ---------- Bắt đầu hành trình (chọn khu vực, khám phá) ----------

def start_journey():
    global environment_level
    header()
    slow_print('Bạn bước ra khỏi buồng ngủ đông. Hành trình bảo vệ Trái Đất bắt đầu...')
    while True:
        print('\nChọn khu vực để thám hiểm:')
        for i, name in enumerate(areas.keys(), 1):
            print(f"{i}) {name}")
        print(f"{len(areas)+1}) Quay lại menu chính")
        choice = input('\nChọn: ').strip()
        try:
            choice = int(choice)
        except ValueError:
            print('Nhập số hợp lệ.')
            continue
        if choice == len(areas)+1:
            break
        if 1 <= choice <= len(areas):
            area_name = list(areas.keys())[choice-1]
            explore_area(area_name)
        else:
            print('Lựa chọn không hợp lệ.')


# ---------- Thám hiểm khu vực ----------

def explore_area(name):
    global environment_level
    info = areas[name]
    header()
    slow_print(f'--- Đang thám hiểm: {name} ---')
    slow_print(f'Ô nhiễm hiện tại: {info["pollution"]}%')

    # Nguy cơ gặp quái vật
    encounter_chance = min(80, info['pollution'] // 2 + 10)
    if random.randint(1, 100) <= encounter_chance:
        slow_print('Bạn gặp một con Quái Vật Rác!')
        combat(name)
    else:
        slow_print('Khu vực tạm thời yên tĩnh. Bạn tìm thấy rác để phân loại.')
        found = random.choices(['hữu cơ', 'tái chế', 'độc hại'], weights=[50, 35, 15])[0]
        quantity = random.randint(1, 4)
        player['inventory'][found] += quantity
        slow_print(f'Bạn thu thập được {quantity} đơn vị rác loại "{found}".')

    # Nếu đủ tài nguyên, dọn dẹp giảm ô nhiễm
    if player['inventory']['hữu cơ'] >= 3 and player['inventory']['tái chế'] >= 2:
        slow_print('Bạn có thể kích hoạt Nâng Cấp Môi Trường tại đây (dùng tài nguyên).')
        use = input('Bạn muốn sử dụng tài nguyên để phục hồi khu vực này không? (y/n): ').strip().lower()
        if use == 'y':
            player['inventory']['hữu cơ'] -= 3
            player['inventory']['tái chế'] -= 2
            healed = random.randint(10, 30)
            info['pollution'] = max(0, info['pollution'] - healed)
            environment_level = min(100, environment_level + healed//2)
            slow_print(f'Bạn hồi sinh khu vực, ô nhiễm giảm {healed}%!')
            if info['pollution'] == 0:
                info['cleared'] = True
                slow_print('Khu vực đã hoàn toàn sạch! Cây cối bắt đầu mọc lại.')


# ---------- Chiến đấu đơn giản ----------

def combat(area_name):
    monster_hp = random.randint(20, 60)
    slow_print(f'Quái vật có HP = {monster_hp}')
    while monster_hp > 0 and player['hp'] > 0:
        print('\nHành động:')
        print('1) Phân loại rác (lấy nguyên liệu, tấn công nhẹ)')
        print('2) Sử dụng phân bón (trồng cây chắn đường)')
        print('3) Sử dụng độc hại (tấn công mạnh, tiêu diệt quái vật)')
        print('4) Rút lui')
        act = input('Chọn hành động (1-4): ').strip()
        if act == '1':
            dmg = random.randint(4, 12)
            monster_hp -= dmg
            gain = random.choice(['hữu cơ', 'tái chế'])
            player['inventory'][gain] += 1
            slow_print(f'Bạn phân loại và tấn công, gây {dmg} sát thương, nhận +1 {gain}.')
        elif act == '2':
            if player['inventory']['hữu cơ'] >= 2:
                player['inventory']['hữu cơ'] -= 2
                slow_print('Bạn bón phân, trồng cây làm hàng rào. Quái vật bị làm chậm.')
                # làm giảm cơ hội quái tấn công mạnh
                continue
            else:
                slow_print('Không đủ rác hữu cơ để làm phân bón.')
                continue
        elif act == '3':
            if player['inventory']['độc hại'] >= 1:
                player['inventory']['độc hại'] -= 1
                dmg = random.randint(18, 35)
                monster_hp -= dmg
                slow_print(f'Bạn dùng chất trung hòa, gây {dmg} sát thương mạnh!')
            else:
                slow_print('Bạn chưa có chất độc hại để trung hòa.')
                continue
        elif act == '4':
            chance = random.randint(1, 100)
            if chance <= 60:
                slow_print('Bạn rút lui an toàn về chỗ trú ẩn.')
                return
            else:
                slow_print('Rút lui thất bại!')
        else:
            slow_print('Lựa chọn không hợp lệ.')
            continue

        # Monster retaliates
        if monster_hp > 0:
            m_dmg = random.randint(5, 18)
            player['hp'] -= m_dmg
            slow_print(f'Quái vật phản công, bạn mất {m_dmg} HP. (HP hiện tại: {player["hp"]})')
            if player['hp'] <= 0:
                slow_print('Bạn bị đánh bại... Trò chơi kết thúc.')
                sys.exit(0)

    if monster_hp <= 0:
        slow_print('Bạn đã tiêu diệt quái vật!')
        # Rơi ra tài nguyên
        drops = random.choices(['hữu cơ', 'tái chế', 'độc hại'], weights=[40, 40, 20], k=2)
        for d in drops:
            player['inventory'][d] += 1
        slow_print('Bạn thu được: ' + ', '.join(drops))
        # Giảm ô nhiễm khu vực nhẹ
        areas[area_name]['pollution'] = max(0, areas[area_name]['pollution'] - random.randint(5, 15))


# ---------- Minigame phân loại rác ----------

def classify_minigame():
    header()
    slow_print('Minigame: Phân loại rác! Gợi ý: "hữu cơ" cho rác phân hủy, "tái chế" cho kim loại/nhựa/giấy, "độc hại" cho hóa chất.')
    score = 0
    for i in range(5):
        item = random.choice([
            ('vỏ trái cây', 'hữu cơ'),
            ('chai nhựa', 'tái chế'),
            ('pin cũ', 'độc hại'),
            ('giấy báo', 'tái chế'),
            ('vỏ trứng', 'hữu cơ'),
            ('hộp sơn', 'độc hại'),
        ])
        print(f'Vật phẩm {i+1}: {item[0]}')
        ans = input('Bạn phân loại là: ').strip().lower()
        if ans == item[1]:
            slow_print('Chính xác!')
            score += 1
            player['inventory'][item[1]] += 1
        else:
            slow_print(f'Sai. Đúng là: {item[1]}')
    slow_print(f'Kết thúc minigame - Điểm: {score}/5')


# ---------- Bắt đầu chương trình ----------

if __name__ == '__main__':
    try:
        main_menu()
    except KeyboardInterrupt:
        slow_print('\nThoát chương trình. Hẹn gặp lại!')
