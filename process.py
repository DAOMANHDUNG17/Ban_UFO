import math
import random
from sys import exit
from var import *
from particles import ParticleManager
import os
import pygame
import asyncio  # THÊM THƯ VIỆN NÀY DÀNH CHO WEB

# --- ÂM THANH (hỗ trợ tốt hơn trên web pygbag) ---
class DummySound:
    def play(self, *args, **kwargs): pass
    def set_volume(self, *args, **kwargs): pass
    def stop(self): pass

def load_music(path, vol):
    try:
        if not pygame.mixer.get_init():
            pygame.mixer.pre_init(44100, -16, 2, 512)
            pygame.mixer.init()
        sound = pygame.mixer.Sound(path)
        sound.set_volume(vol)
        return sound
    except Exception as e:
        print(f"[SOUND] Không load được {path}: {e}")
        return DummySound()

# =================================================

def create_game(name):
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.init()
    screen = pygame.display.set_mode((1366, 768))
    pygame.display.set_caption(name)
    try:
        icon_path = os.path.normpath(
            os.path.join(os.path.dirname(save_file_path()), '..', 'image', 'chicken.png')
        )
        if os.path.isfile(icon_path):
            icon = pygame.image.load(icon_path)
            try:
                icon = icon.convert_alpha()
            except Exception:
                pass
            pygame.display.set_icon(icon)
    except Exception as e:
        print(f"Icon load skipped: {e}")

    # Bắt đầu nhạc nền (trên web có thể bị chặn cho đến khi người dùng click lần đầu)
    bg = load_music(all_music()['bg'], 0.25)
    try:
        bg.play(-1)
    except:
        pass
    return screen


# ================= SAVE FILE =================

def read_highscores():
    path = highscores_file_path()
    if not os.path.exists(path):
        return []
    try:
        with open(path, 'r') as f:
            return sorted([int(line.strip()) for line in f if line.strip()], reverse=True)
    except:
        return []

def record_high_score(score):
    try:
        scores = read_highscores()
        scores.append(score)
        scores.sort(reverse=True)
        path = highscores_file_path()
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            for s in scores[:10]:
                f.write(f"{s}\n")
    except Exception as e:
        print(f"Error recording high score: {e}")

def add_pos_menu(obj_menu):
    sw = 1366 # Default screen width
    new_arr = [[obj_menu[0], (sw // 2 - obj_menu[0].get_width() // 2, 80)]]
    pos_y = 300
    for i in range(1, len(obj_menu)):
        new_arr.append([obj_menu[i], (sw // 2 - obj_menu[i].get_width() // 2, pos_y)])
        pos_y += 85
    return new_arr


async def create_menu(screen, menu, highlight_color=(255, 215, 0), shadow=False):
    obj = add_pos_menu(menu)
    bg = get_img('bg')
    signal = text('>>>', 50, 'White')
    fps = pygame.time.Clock()
    select = 1
    click_sound = load_music(all_music()['shoot'], 0.35)
    
    while True:
        fps.tick(30)
        screen.blit(bg, (0, 0))
        
        for idx, (surf, pos) in enumerate(obj):
            rect = pygame.Rect(pos[0]-20, pos[1]-10, surf.get_width()+40, surf.get_height()+20)
            
            if idx == select:
                scale = 1.0 + 0.05 * math.sin(pygame.time.get_ticks() * 0.01)
                item_surf = pygame.transform.rotozoom(surf, 0, scale)
                item_rect = item_surf.get_rect(center=(pos[0] + surf.get_width()//2, pos[1] + surf.get_height()//2))
                
                pygame.draw.rect(screen, highlight_color, rect, border_radius=18)
                if shadow:
                    shadow_rect = rect.move(4, 4)
                    pygame.draw.rect(screen, (0,0,0,80), shadow_rect, border_radius=18)
                screen.blit(item_surf, item_rect)
            else:
                pygame.draw.rect(screen, (0,0,0,60), rect, border_radius=18)
                screen.blit(surf, pos)
                
        screen.blit(signal, (obj[select][1][0] - 80, obj[select][1][1]))
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN and select < len(menu) - 1:
                    select += 1
                    click_sound.play()
                elif event.key == pygame.K_UP and select > 1:
                    select -= 1
                    click_sound.play()
                elif event.key == pygame.K_RETURN:
                    return select
        
        await asyncio.sleep(0)  # THÊM NHƯỜNG LUỒNG

async def highscores_menu(screen):
    bg = get_img('bg')
    fps = pygame.time.Clock()
    font_name = 'segoe ui,tahoma,arial'
    score_font = pygame.font.SysFont(font_name, 45, bold=True)
    title_font = pygame.font.SysFont(font_name, 100, bold=True)
    
    while True:
        fps.tick(30)
        screen.blit(bg, (0, 0))
        scores = read_highscores()
        
        title_surf = title_font.render('HIGH SCORES', True, (255, 0, 0))
        screen.blit(title_surf, (450, 80))
        
        y = 220
        for i, s in enumerate(scores[:10]):
            txt = score_font.render(f'{i + 1}. {s}', True, (255, 255, 0))
            screen.blit(txt, (520, y))
            y += 45
        if not scores:
            screen.blit(text('No scores yet', 40, 'Gray'), (520, 280))
        screen.blit(
            text('Press ENTER or ESC to return', 35, 'White'),
            (480, 680),
        )
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                    return
        
        await asyncio.sleep(0)

async def shop_menu(screen):
    bg = get_img('bg')
    fps = pygame.time.Clock()
    f_name = 'segoe ui,tahoma,arial'
    title_font = pygame.font.SysFont(f_name, 70, bold=True)
    item_font = pygame.font.SysFont(f_name, 30, bold=True)
    info_font = pygame.font.SysFont(f_name, 22)
    
    while True:
        fps.tick(30)
        data = r_file()
        motors = data[9]
        upgrades = [
            {'name': "TỐC ĐỘ ĐỘNG CƠ", 'lv': data[10], 'cost': upgrade_costs(data[10]), 'idx': 10, 'color': (0, 200, 255), 'desc': "Bay nhanh hơn & linh hoạt hơn"},
            {'name': "MÁU TỐI ĐA", 'lv': data[11], 'cost': upgrade_costs(data[11]), 'idx': 11, 'color': (255, 100, 100), 'desc': "Thêm máu tối đa và máu khởi đầu"},
            {'name': "HỒI TÊN LỬA", 'lv': data[12], 'cost': upgrade_costs(data[12]), 'idx': 12, 'color': (255, 200, 0), 'desc': "Nạp lại tên lửa nhanh hơn"}
        ]
        
        screen.blit(bg, (0, 0))
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))
        
        title = title_font.render('CỬA HÀNG NÂNG CẤP', True, (255, 255, 255))
        screen.blit(title, (screen.get_width()//2 - title.get_width()//2, 40))
        
        motor_txt = item_font.render(f"SỐ ĐỘNG CƠ HIỆN CÓ: {motors}", True, (255, 215, 0))
        screen.blit(motor_txt, (screen.get_width()//2 - motor_txt.get_width()//2, 120))
        
        mx, my = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()[0]
        
        for i, upg in enumerate(upgrades):
            rect = pygame.Rect(screen.get_width()//2 - 400, 180 + i * 140, 800, 120)
            is_hover = rect.collidepoint(mx, my)
            
            pygame.draw.rect(screen, (30, 30, 40), rect, border_radius=15)
            pygame.draw.rect(screen, (255, 255, 255) if is_hover else (100, 100, 100), rect, 2, border_radius=15)
            pygame.draw.rect(screen, upg['color'], (rect.x + 20, rect.y + 20, 80, 80), border_radius=10)
            
            name_surf = item_font.render(f"{upg['name']} (Cấp {upg['lv']}) - Giá: {upg['cost']}", True, (255, 255, 255))
            screen.blit(name_surf, (rect.x + 120, rect.y + 25))
            desc_surf = info_font.render(upg['desc'], True, (180, 180, 180))
            screen.blit(desc_surf, (rect.x + 120, rect.y + 65))
            
            btn_rect = pygame.Rect(rect.right - 180, rect.y + 35, 150, 50)
            btn_hover = btn_rect.collidepoint(mx, my)
            can_afford = motors >= upg['cost']
            
            btn_col = (0, 255, 100) if can_afford else (150, 50, 50)
            if btn_hover and can_afford: btn_col = (50, 255, 150)
            
            pygame.draw.rect(screen, btn_col, btn_rect, border_radius=10)
            if can_afford:
                buy_text = f"MUA: {upg['cost']}"
            else:
                buy_text = f"THIẾU: {upg['cost'] - motors}"
            
            buy_surf = item_font.render(buy_text, True, (0, 0, 0))
            screen.blit(buy_surf, (btn_rect.centerx - buy_surf.get_width()//2, btn_rect.centery - buy_surf.get_height()//2))
            
            if click and btn_hover and can_afford:
                data[9] -= upg['cost']
                data[upg['idx']] += 1
                w_file(*data)
                await asyncio.sleep(0.2)
        
        back_btn = pygame.Rect(screen.get_width()//2 - 100, 650, 200, 50)
        back_hover = back_btn.collidepoint(mx, my)
        pygame.draw.rect(screen, (200, 200, 200) if back_hover else (100, 100, 100), back_btn, border_radius=10)
        back_txt = item_font.render("QUAY LẠI", True, (0, 0, 0))
        screen.blit(back_txt, (back_btn.centerx - back_txt.get_width()//2, back_btn.centery - back_txt.get_height()//2))
        
        if (click and back_hover) or pygame.key.get_pressed()[pygame.K_ESCAPE]: return
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: close()
            
        await asyncio.sleep(0)

async def hangar_menu(screen):
    bg = get_img('bg')
    data = list(r_file())
    while len(data) < 8:
        data.append(0)
    if len(data) < 9:
        data.append(starting_ammo(data[5] if data[5] in (1, 2, 3) else 2))

    skin_i = data[7] if len(data) > 7 else 0
    names = ship_skin_filenames()
    n = len(names)
    fps = pygame.time.Clock()

    while True:
        fps.tick(30)
        screen.blit(bg, (0, 0))
        screen.blit(text('HANGAR', 100, 'Red'), (530, 70))
        preview = load_ship_skin(skin_i)
        px = (1366 - preview.get_width()) // 2
        py = 280
        screen.blit(preview, (px, py))

        label = names[skin_i].replace('.png', '').replace('_', ' ')
        screen.blit(text(label[:28], 38, 'Yellow'), (480, 520))
        screen.blit(
            text('LEFT / RIGHT: skin | ENTER: save | ESC: back', 32, 'White'),
            (340, 660),
        )

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    skin_i = (skin_i - 1) % n
                elif event.key == pygame.K_RIGHT:
                    skin_i = (skin_i + 1) % n
                elif event.key == pygame.K_RETURN:
                    data = list(r_file())
                    while len(data) < 9:
                        pad = starting_ammo(data[5] if len(data) > 5 and data[5] in (1, 2, 3) else 2)
                        data.append(pad)
                    data[7] = skin_i
                    w_file(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8])
                    return
                elif event.key == pygame.K_ESCAPE:
                    return

        await asyncio.sleep(0)


def missile_weapon_inf():
    s = pygame.Surface((26, 36), pygame.SRCALPHA)
    pygame.draw.polygon(s, (255, 200, 80), [(13, 0), (26, 36), (0, 36)])
    pygame.draw.circle(s, (255, 90, 40), (13, 14), 6)
    pygame.draw.polygon(s, (255, 240, 200), [(13, 4), (18, 14), (8, 14)])
    try:
        img = s.convert_alpha()
    except Exception:
        img = s
    return {'img': img, 'rect': img.get_rect(), 'items': []}

def nearest_chicken_center(mx, my, ck_inf):
    if not ck_inf['pos']:
        return None, None
    cw = ck_inf['img'].get_width()
    ch = ck_inf['img'].get_height()
    best_d = 1e12
    bx = None
    by = None
    for px, py in ck_inf['pos']:
        cx = px + cw / 2
        cy = py + ch / 2
        d = (cx - mx) ** 2 + (cy - my) ** 2
        if d < best_d:
            best_d = d
            bx, by = cx, cy
    return bx, by

def step_homing_missiles(missile_inf, speed, boss_mode, boss_hp, boss_pos, boss_img, ck_inf):
    for m in missile_inf['items']:
        mx, my = m['x'], m['y']
        tx = ty = None
        if boss_mode and boss_hp > 0 and boss_img is not None:
            tx = boss_pos[0] + boss_img.get_width() / 2
            ty = boss_pos[1] + boss_img.get_height() / 2
        else:
            tx, ty = nearest_chicken_center(mx, my, ck_inf)
            if tx is None:
                tx = mx
                ty = my - 260
        dx = tx - mx
        dy = ty - my
        dist = math.hypot(dx, dy)
        if dist < 1e-6:
            continue
        m['x'] += dx / dist * speed
        m['y'] += dy / dist * speed

def draw_hit_bursts(screen, bursts):
    for b in bursts[:]:
        bx, by = b['pos']
        t = b['ttl']
        rad = 10 + (22 - t)
        pygame.draw.circle(screen, (255, 220, 120), (int(bx), int(by)), min(rad, 48), 2)
        pygame.draw.circle(screen, (255, 140, 60), (int(bx), int(by)), min(rad // 2 + 4, 36))
        b['ttl'] -= 1
        if b['ttl'] <= 0:
            bursts.remove(b)

def cull_missiles(missile_inf, max_sz):
    missile_inf['items'] = [
        m for m in missile_inf['items']
        if -60 <= m['x'] <= max_sz[0] + 60
        and -80 <= m['y'] <= max_sz[1] + 60
    ]

def use_boss_fight(lv_game, difficulty):
    if difficulty == 1:
        return lv_game > 0 and lv_game % 10 == 0
    elif difficulty == 2:
        return lv_game > 0 and lv_game % 5 == 0
    else:
        return True

def roll_chicken_drop(gifts_spawned):
    r = random.random()
    if gifts_spawned < MAX_GIFTS_PER_STAGE and r < GIFT_DROP_RATE:
        return 'gift'
    r2 = random.random()
    if r2 < 0.5:
        return 'egg'
    return 'drumstick'


# ================= SYSTEM =================

def close():
    pygame.quit()
    exit()

def change_pos(tuple_1, tuple_2):
    return tuple(a + b for a, b in zip(tuple_1, tuple_2))

def add_event(id_event, timer):
    event_id = pygame.USEREVENT + id_event
    pygame.time.set_timer(event_id, int(timer))
    return event_id


# ================= COLLISION =================

def collision(inf_1, inf_2):
    for i in range(len(inf_1['pos'])):
        inf_1['rect'].topleft = inf_1['pos'][i]
        for j in range(len(inf_2['pos'])):
            inf_2['rect'].topleft = inf_2['pos'][j]
            if inf_1['rect'].colliderect(inf_2['rect']):
                return [i, j]
    return None


# ================= UI =================

def show_score_hp(screen, score, motors, hp, rays_per_shot=None, ammo=None, missiles=None):
    motor_img = get_img('motor')
    hp_img = get_img('hp')
    
    screen.blit(motor_img, (20, 5))
    motor_text = text(f"x{motors}", 50, 'Yellow')
    screen.blit(motor_text, (85, 5))
    
    screen.blit(hp_img, (20, 65))
    hp_text = text(f"x{hp}", 50, 'Brown')
    screen.blit(hp_text, (85, 65))

    if ammo is not None:
        atxt = text(f"Đạn: {ammo}", 40, 'White')
        screen.blit(atxt, (50, 130))
    if rays_per_shot is not None:
        ray_text = text(f"Số tia: {rays_per_shot}", 35, 'Cyan')
        screen.blit(ray_text, (50, 175))
    if missiles is not None:
        mtxt = text(f"Tên lửa: {missiles}", 35, 'Orange')
        screen.blit(mtxt, (50, 220))

def screen_show_mess(screen, string):
    screen.blit(get_img('bg'), (0, 0))
    screen.blit(text(string, 100, 'Red'), (500, 200))
    pygame.display.update()

def screen_playing(screen, obj, pl_inf, ck_inf, egg_inf, ls_inf, score_inf, gift_inf,
                   score, hp, time, rays_per_shot=None, boss_draw=None, missile_inf=None,
                   big_egg_inf=None, missiles_left=None, ammo=None, hit_bursts=None,
                   gift_rays_timer=0, shield_timer=0, ship_tilt=0, muzzle_flash=0,
                   ultimate_energy=0, feathers=0):

    for i, j in obj:
        screen.blit(i, j)

    if boss_draw is not None:
        bx, by = boss_draw['pos']
        screen.blit(boss_draw['img'], (bx, by))
        bw = boss_draw['img'].get_width()
        ratio = boss_draw['hp'] / max(1, boss_draw['max_hp'])
        pygame.draw.rect(screen, (90, 0, 0), (bx, by - 24, bw, 16))
        pygame.draw.rect(screen, (40, 220, 60), (bx, by - 24, int(bw * ratio), 16))

    for i in ls_inf['pos']:
        screen.blit(ls_inf['img'], i)

    if missile_inf is not None:
        for m in missile_inf['items']:
            screen.blit(missile_inf['img'], (int(m['x']), int(m['y'])))

    t = pygame.time.get_ticks()
    for i in range(len(ck_inf['pos'])):
        angle = (t * 0.1) % 360
        img = ck_inf['img']
        rotated_img = pygame.transform.rotate(img, angle)
        rect = rotated_img.get_rect(center=(ck_inf['pos'][i][0] + img.get_width()//2, ck_inf['pos'][i][1] + img.get_height()//2))
        screen.blit(rotated_img, rect.topleft)

    for i in egg_inf['pos']:
        screen.blit(egg_inf['img'], i)

    if big_egg_inf is not None:
        for i in big_egg_inf['pos']:
            screen.blit(big_egg_inf['img'], i)

    motor_img = get_img('motor')
    for i in range(len(score_inf['pos'])):
        screen.blit(motor_img, score_inf['pos'][i])

    for i in range(len(gift_inf['pos'])):
        pos = gift_inf['pos'][i]
        g_type = gift_inf['types'][i] if i < len(gift_inf['types']) else None
        
        if g_type == 'motor':
            screen.blit(motor_img, pos)
        else:
            screen.blit(gift_inf['img'], pos)
        
        if g_type:
            colors = {
                'rays': (0, 255, 255),
                'shield': (100, 200, 255),
                'ammo': (255, 255, 255),
                'hp': (255, 100, 100)
            }
            color = colors.get(g_type, (255, 255, 0))
            pygame.draw.circle(screen, color, (int(pos[0] + 25), int(pos[1] + 25)), 32, 3)

    if hit_bursts:
        draw_hit_bursts(screen, hit_bursts)

    show_score_hp(screen, score, feathers, hp, rays_per_shot, ammo, missiles_left)
    
    screen.blit(text(f"Động cơ (Tổng): {feathers}", 30, (255, 215, 0)), (50, 265))

    py_y = 305
    if shield_timer > 0:
        screen.blit(text(f"Bất tử: {shield_timer//60}s", 30, (100, 200, 255)), (50, py_y))
        py_y += 35

    energy_color = (255, 100, 255) if ultimate_energy < 100 else (255, 255, 0)
    pygame.draw.rect(screen, (50, 50, 50), (50, py_y + 10, 150, 15))
    pygame.draw.rect(screen, energy_color, (50, py_y + 10, 150 * (ultimate_energy/100), 15))
    screen.blit(text("CHIÊU CUỐI", 24, energy_color), (50, py_y + 28))
    if ultimate_energy >= 100:
        screen.blit(text("SẴN SÀNG! (SPACE)", 22, (255, 255, 255)), (50, py_y + 50))

    screen.blit(text(f"Thời gian: {time}", 30, 'Red'), (1100, 700))

    if shield_timer > 0:
        px, py = pl_inf['pos'][0]
        sw, sh = pl_inf['img'].get_size()
        if shield_timer > 120 or (pygame.time.get_ticks() // 200) % 2 == 0:
            pygame.draw.circle(screen, (100, 200, 255), (px + sw//2, py + sh//2), sw, 3)
            pygame.draw.circle(screen, (100, 200, 255), (px + sw//2, py + sh//2), sw - 5, 1)

    ship_img = pl_inf['img']
    if abs(ship_tilt) > 1:
        angle = -ship_tilt * 0.8
        angle = max(-25, min(25, angle))
        ship_img = pygame.transform.rotate(pl_inf['img'], angle)
    
    ship_rect = ship_img.get_rect(center=(pl_inf['pos'][0][0] + pl_inf['img'].get_width()//2, pl_inf['pos'][0][1] + pl_inf['img'].get_height()//2))
    screen.blit(ship_img, ship_rect)
    
    if muzzle_flash > 0:
        flash_pos = (pl_inf['pos'][0][0] + pl_inf['img'].get_width()//2, pl_inf['pos'][0][1] - 5)
        pygame.draw.circle(screen, (255, 255, 200), flash_pos, random.randint(8, 15))
        pygame.draw.circle(screen, (255, 255, 255), flash_pos, random.randint(4, 8))

    pygame.display.update()


# ================= CREATE OBJECT =================

def create_chicken(level, number_ck, ck_inf):
    distance = 80
    x = 100
    y = 0
    direct = False
    patterns = ['horizontal', 'sine', 'zigzag', 'circle']
    pattern = patterns[(level - 1) % len(patterns)] if level > 1 else 'horizontal'

    if level <= 3:
        ck_row = 8
    elif level <= 5:
        ck_row = 10
    else:
        ck_row = min(18, 12 + (level - 6) // 2)

    for i in range(number_ck):
        if i % ck_row == 0 and i > 0:
            if direct:
                x = 100
                direct = False
            else:
                x = 500
                direct = True
            y += 80
        else:
            if i > 0:
                x += distance
        ck_inf['pos'].append((x, y))
        ck_inf['direct'].append(direct)
        ck_inf['pattern'].append(pattern)
        ck_inf['base_y'].append(y)
        ck_inf['time_offset'].append(i * 15)

def _laser_shot_offsets(num_ray):
    patterns = {
        1: [(20, -20)],
        2: [(0, -20), (40, -20)],
        3: [(-20, -20), (20, -20), (60, -20)],
        4: [(-40, -20), (0, -20), (40, -20), (80, -20)],
        5: [(-50, -20), (-15, -20), (20, -20), (55, -20), (90, -20)],
        6: [(-60, -22), (-30, -22), (0, -22), (30, -22), (60, -22), (95, -22)],
    }
    n = max(1, min(num_ray, max_rays_per_shot()))
    return patterns.get(n, patterns[6])

def create_laser(num_ray, ls_inf, pl_inf, sound, offset_x=0):
    px, py = pl_inf['pos'][0]
    pw, ph = pl_inf['img'].get_size()
    px += offset_x
    if num_ray == 1:
        ls_inf['pos'].append((px + pw // 2 - 4, py))
    elif num_ray == 2:
        ls_inf['pos'].append((px + 5, py + 20))
        ls_inf['pos'].append((px + pw - 13, py + 20))
    elif num_ray == 3:
        ls_inf['pos'].append((px + 5, py + 20))
        ls_inf['pos'].append((px + pw // 2 - 4, py))
        ls_inf['pos'].append((px + pw - 13, py + 20))
    elif num_ray >= 4:
        ls_inf['pos'].append((px + 5, py + 20))
        ls_inf['pos'].append((px + pw // 2 - 4, py - 5))
        ls_inf['pos'].append((px + pw - 13, py + 20))
        ls_inf['pos'].append((px + pw // 2 - 4, py + 15))
        if num_ray >= 6:
            ls_inf['pos'].append((px - 10, py + 30))
            ls_inf['pos'].append((px + pw + 2, py + 30))
    sound.play()

def create_egg(level, egg_inf, ck_inf, boss_mode=False, boss_pos=None, big_egg_inf=None):
    if boss_mode and boss_pos is not None and big_egg_inf is not None:
        big_egg_inf['pos'].append(change_pos(boss_pos, (62, 175)))
        big_egg_inf['direct'].append(random.choice([True, False]))
        return
    if len(ck_inf['pos']) == 0: return
    temp = random.randint(0, len(ck_inf['pos']) - 1)
    egg_inf['pos'].append(change_pos(ck_inf['pos'][temp], (10, 50)))
    if level >= 4:
        egg_inf['direct'].append(ck_inf['direct'][temp])


# ================= MOVE =================

def move(speed, inf):
    for i in range(len(inf['pos'])):
        inf['pos'][i] = change_pos(inf['pos'][i], (0, speed))

def move_ck(inf, step=1):
    get_dir = {True: -step, False: step}
    t = pygame.time.get_ticks()
    for i in range(len(inf['pos'])):
        x, y = inf['pos'][i]
        base_y = inf['base_y'][i] if i < len(inf['base_y']) else y
        pattern = inf['pattern'][i] if i < len(inf['pattern']) else 'horizontal'
        offset = inf['time_offset'][i] if i < len(inf['time_offset']) else 0
        dx = get_dir[inf['direct'][i]]
        x += dx

        if pattern == 'sine':
            y = base_y + int(50 * math.sin((t + offset * 10) * 0.003))
        elif pattern == 'zigzag':
            y = base_y + int(40 * abs(math.sin((t + offset * 10) * 0.003)))
        elif pattern == 'circle':
            y = base_y + int(40 * math.sin((t + offset * 10) * 0.003))
            x += int(5 * math.cos((t + offset * 10) * 0.003))

        if x > 1360: x = 0
        elif x < 0: x = 1300
        inf['pos'][i] = (x, y)

def move_eggs(inf, fall_y=2, horiz=1):
    get_dir = {True: -horiz, False: horiz}
    for i in range(len(inf['pos'])):
        inf['pos'][i] = change_pos(inf['pos'][i], (get_dir[inf['direct'][i]], fall_y))


# ================= REMOVE OBJECT =================

def out_screen(inf, size_screen):
    new_pos = []
    new_types = []
    for i in range(len(inf['pos'])):
        pos = inf['pos'][i]
        if 0 <= pos[0] <= size_screen[0] and 0 <= pos[1] <= size_screen[1]:
            new_pos.append(pos)
            if 'types' in inf and i < len(inf['types']):
                new_types.append(inf['types'][i])
    inf['pos'] = new_pos
    if 'types' in inf:
        inf['types'] = new_types

def out_screen_egg(level, inf, size_screen):
    new_pos = []
    new_direct = []
    new_types = []
    for i in range(len(inf['pos'])):
        pos = inf['pos'][i]
        if -200 <= pos[0] <= size_screen[0] + 200 and -300 <= pos[1] <= size_screen[1] + 200:
            new_pos.append(pos)
            if 'direct' in inf and i < len(inf['direct']):
                new_direct.append(inf['direct'][i])
            if 'types' in inf and i < len(inf['types']):
                new_types.append(inf['types'][i])
    inf['pos'] = new_pos
    if 'direct' in inf: inf['direct'] = new_direct
    if 'types' in inf: inf['types'] = new_types


# ================= DIFFICULTY =================

def egg_interval_mult(difficulty):
    return {1: 1.45, 2: 1.0, 3: 0.72}[difficulty]

def count_mult(difficulty):
    return {1: 1.22, 2: 1.0, 3: 0.82}[difficulty]

def ck_speed_step(difficulty, lv_game):
    base = {1: 1, 2: 1, 3: 2}[difficulty]
    if lv_game > 3: base += max(0, (lv_game - 4) // 3)
    return base

def stage_ramp(lv_game):
    return 1.0 + (lv_game - 1) * 0.042

def egg_fall_speed(lv_game):
    return 2 + max(0, (lv_game - 1) // 4)


# ================= MAIN GAME =================

particle_manager = ParticleManager()
STAR_LAYERS = [
    {'color': (40, 40, 60), 'speed': 0.1, 'stars': [], 'size': 3}, 
    {'color': (120, 120, 150), 'speed': 0.3, 'stars': [], 'size': 1}, 
    {'color': (180, 180, 220), 'speed': 0.6, 'stars': [], 'size': 2}, 
    {'color': (255, 255, 255), 'speed': 1.2, 'stars': [], 'size': 2}, 
]

def init_star_layers(width, height, count=100):
    for i, layer in enumerate(STAR_LAYERS):
        layer['stars'] = []
        c = count // (i + 1)
        for _ in range(c):
            x = random.randint(0, width)
            y = random.randint(0, height)
            layer['stars'].append([x, y])

def draw_parallax_background(screen, width, height):
    for layer in STAR_LAYERS:
        for star in layer['stars']:
            pygame.draw.circle(screen, layer['color'], (int(star[0]), int(star[1])), layer['size'])
            star[1] += layer['speed']
            if star[1] > height:
                star[1] = 0
                star[0] = random.randint(0, width)

def health_bar(surface, x, y, hp, max_hp, width=200, height=20):
    ratio = max(0, hp) / max(1, max_hp)
    pygame.draw.rect(surface, (80, 0, 0), (x, y, width, height))
    pygame.draw.rect(surface, (200, 0, 0), (x, y, int(width * ratio), height))

def apply_screen_shake(offset, magnitude=5):
    return (random.randint(-magnitude, magnitude), random.randint(-magnitude, magnitude))


async def game_over_screen(screen, score):
    bg = get_img('bg')
    f_name = 'segoe ui,tahoma,arial'
    font_title = pygame.font.SysFont(f_name, 100, bold=True)
    font_msg = pygame.font.SysFont(f_name, 50)
    
    while True:
        screen.blit(bg, (0, 0))
        title = font_title.render("TRÒ CHƠI KẾT THÚC", True, (255, 0, 0))
        screen.blit(title, (screen.get_width()//2 - title.get_width()//2, 200))
        
        score_txt = font_msg.render(f"ĐIỂM CỦA BẠN: {score}", True, (255, 255, 255))
        screen.blit(score_txt, (screen.get_width()//2 - score_txt.get_width()//2, 350))
        
        hint = font_msg.render("Nhấn phím bất kỳ để quay lại", True, (200, 200, 200))
        screen.blit(hint, (screen.get_width()//2 - hint.get_width()//2, 500))
        
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: close()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        await asyncio.sleep(0)
                
def show_popup(screen, title, message):
    pass

def find_best_target(player_pos, ck_inf, boss_mode, boss_pos, boss_img=None):
    if boss_mode and boss_pos:
        bw = boss_img.get_width() if boss_img else 180
        bh = boss_img.get_height() if boss_img else 180
        return [boss_pos[0] + bw // 2, boss_pos[1] + bh // 2]
        
    if not ck_inf['pos']: return None
        
    closest_chicken = None
    min_distance = float('inf')
    px, py = player_pos
    for ch_pos in ck_inf['pos']:
        if not ch_pos: continue
        dist = math.hypot(ch_pos[0] - px, ch_pos[1] - py)
        if dist < min_distance:
            min_distance = dist
            closest_chicken = ch_pos
    return closest_chicken


async def loop_playing(screen, load_inf=None, difficulty=None, run_earned_motors=None, ultimate_energy=None, gift_rays=None):
    load = load_inf
    if load is None:
        prev = r_file()
        sk = prev[7] if len(prev) > 7 else 0
        d = difficulty if difficulty is not None else 2
        load = [1, 1, 0, 5, 0, d, 0, sk, starting_ammo(d)]
    elif len(load) == 4:
        load = load + [0, 2, 0, 0, starting_ammo(2)]
    elif len(load) == 6:
        load = load + [0, 0, starting_ammo(2)]
    elif len(load) == 8:
        load.append(starting_ammo(load[5] if load[5] in (1, 2, 3) else 2))

    while len(load) < 13:
        if len(load) == 9:
            load.extend([0, 0, 0, 0])
        else:
            load.append(0)
    
    (lv_game, lv_gun, score, hp, gift_rays, diff_saved, old_missiles,
     skin_index, ammo, motors_collected, u_speed, u_hp, u_missile) = load[:13]

    # Clean per-match earnings (chỉ xu nhặt được trong ván này)
    # Tuân thủ cấu trúc deploy: state run-time được truyền từ main.py session
    if run_earned_motors is not None:
        motors_collected = run_earned_motors
    else:
        motors_collected = 0  # an toàn cho trường hợp gọi cũ

    current_missiles_count = old_missiles

    if difficulty is not None:
        diff_saved = difficulty
        gift_rays = 0
        ammo = starting_ammo(difficulty)

    difficulty = diff_saved
    if difficulty not in (1, 2, 3): difficulty = 2

    boss_mode = use_boss_fight(lv_game, difficulty)
    meteor_mode = not boss_mode and lv_game > 0 and lv_game % 3 == 0

    num_ck = 1; num_create_ck = 2; max_time = 3; req_plus_hp = 4
    game = game_level()
    shoot_time = 0; ray_gun = 1; speed_gun = 2; req_score_gun = 3
    gun = gun_level()

    gift_rays = max(0, gift_rays)
    ammo = max(0, ammo)
    ns = len(ship_skin_filenames())
    skin_index = max(0, min(ns - 1, skin_index))

    if boss_mode: msg = f"BOSS — MÀN {lv_game}"
    elif meteor_mode: msg = f"MÀN THIÊN THẠCH {lv_game}"
    else: msg = f"MÀN {lv_game}"

    screen_show_mess(screen, msg)
    await asyncio.sleep(2)

    print(f"[GAME] Init start lv={lv_game} boss={boss_mode} meteor={meteor_mode}")
    fps = pygame.time.Clock()
    Max = screen.get_size()
    music = all_music()

    await asyncio.sleep(0)  # Yield cho trình duyệt

    pl_inf = player_inf(skin_index)
    ck_inf = chicken_inf()
    ls_inf = laser_inf()
    egg_inf = eg_inf()
    big_egg_inf = eg_inf_big()
    score_inf = sc_inf()
    gift_inf = gift_pickup_inf()
    gift_inf['types'] = []
    missile_inf = missile_weapon_inf()
    
    await asyncio.sleep(0)  # Yield cho trình duyệt sau khi tạo sprites
    print("[GAME] Sprites created")

    missiles = load[6] if 'load' in locals() else 0
    boss_hp = 0
    boss_max_hp = 0
    boss_pos = [Max[0] // 2 - 90, 110]
    boss_vx = 7
    boss_img = None

    if boss_mode:
        boss_img = pygame.transform.scale(make_enemy_sprite(2), (180, 180))
        bw = boss_img.get_width()
        boss_pos[0] = Max[0] // 2 - bw // 2
        boss_vx = 1.5 + lv_game * 0.5 + (1 if difficulty == 3 else 0)
        boss_hp = 30 + lv_game * 20 + (20 if difficulty == 3 else 0)
        boss_max_hp = boss_hp
    elif meteor_mode:
        pass
    else:
        create_chicken(lv_game, game[lv_game][num_ck], ck_inf)
        game[lv_game][num_create_ck] -= 1

    size_player = pl_inf['img'].get_size()
    init_star_layers(*screen.get_size(), count=80)
    shake_timer = 0
    
    player_target_pos = list(pl_inf['pos'][0])
    player_current_pos = list(pl_inf['pos'][0])

    await asyncio.sleep(0)  # Yield cho trình duyệt sau khi tạo level
    print("[GAME] Level objects created")
    
    u_data = r_file()
    stats = get_stat_bonus(u_data[10], u_data[11], u_data[12])
    hp = min(hp + stats['max_hp_bonus'], 5 + stats['max_hp_bonus'])
    
    invincibility_timer = 0
    level_up_msg_timer = 0
    muzzle_flash_timer = 0
    ultimate_energy = ultimate_energy if ultimate_energy is not None else 0
    ultimate_storm_timer = 0
    missile_timer = 0
    screen_shake = 0
    level_up_font = pygame.font.SysFont('Arial', 80, bold=True)
    
    gift_rays = gift_rays if gift_rays is not None else 0
    gift_rays_timer = 0  # vẫn giữ biến để không phá UI cũ, nhưng sẽ không dùng timer nữa
    shield_timer = 0
    shoot_cooldown = 0 

    # --- SỬ DỤNG LÁ CHẮN ÂM THANH TRONG LÚC CHƠI ---
    laser_sound = load_music(music['shoot'], 0.28)
    boom_sound = load_music(music['explode_ck'], 0.30)
    collision_sound = load_music(music['collision'], 0.25)

    ramp = stage_ramp(lv_game)
    egg_ms = int(game[lv_game][shoot_time] * egg_interval_mult(difficulty) / ramp)

    if boss_mode: egg_ms = max(180, int(egg_ms / 1.5))
    elif meteor_mode: egg_ms = max(200, int(egg_ms / 2))
    else: egg_ms = max(160, egg_ms)

    # Dùng frame counter thay vì pygame.time.set_timer (tương thích web hơn)
    _egg_frame_interval = max(1, int(egg_ms / 16.67))  # Chuyển ms sang số frame (60fps)
    _countdown_frame_interval = 60  # 1 giây = 60 frames
    _egg_frame_counter = 0
    _countdown_frame_counter = 0
    count = max(5, int(game[lv_game][max_time] * count_mult(difficulty) / ramp))
    if boss_mode: count = max(count, 48 + lv_game * 4)

    obj = obj_default_playing()
    plus_hp = False
    ck_step = ck_speed_step(difficulty, lv_game)
    egg_dy = egg_fall_speed(lv_game)
    egg_horiz = 1 + max(0, (lv_game - 4) // 5)
    big_fall = egg_dy + 5 + (5 if boss_mode else 0)
    big_hz = egg_horiz + (2 if boss_mode else 0)
    
    gifts_spawned_stage = 0
    hit_bursts = []

    await asyncio.sleep(0)  # Yield cho trình duyệt trước khi bắt đầu vòng lặp
    print("[GAME] Starting game loop")

    def rays_this_shot():
        base = gun[lv_gun][ray_gun]
        return min(max_rays_per_shot(), base + gift_rays)

    while True:
        fps.tick(60)
        boss_draw = None
        if boss_mode and boss_hp > 0 and boss_img is not None:
            boss_draw = {'hp': boss_hp, 'max_hp': boss_max_hp, 'pos': (boss_pos[0], boss_pos[1]), 'img': boss_img}

        offset = (0, 0)
        if shake_timer > 0:
            offset = apply_screen_shake(offset)
            shake_timer -= 1
        
        draw_parallax_background(screen, *screen.get_size())
        
        screen_playing(
            screen, obj, pl_inf, ck_inf, egg_inf, ls_inf, score_inf, gift_inf, score, hp, count,
            rays_this_shot(), boss_draw, missile_inf, big_egg_inf, current_missiles_count, ammo,
            hit_bursts, gift_rays_timer, shield_timer, (player_target_pos[0] - player_current_pos[0]),
            muzzle_flash_timer, ultimate_energy, motors_collected
        )
        
        if missile_timer > 0: missile_timer -= 1
        if muzzle_flash_timer > 0: muzzle_flash_timer -= 1
        if ultimate_storm_timer > 0:
            ultimate_storm_timer -= 1
            screen_shake = random.randint(2, 6)
            if ultimate_storm_timer % 3 == 0:
                create_laser(random.randint(2, 4), ls_inf, pl_inf, laser_sound, offset_x=random.randint(-200, 200))
        # gift_rays không còn dùng timer nữa (theo yêu cầu mới)
        
        if shield_timer > 0: shield_timer -= 1
        
        if level_up_msg_timer > 0:
            level_up_msg_timer -= 1
            msg_surf = level_up_font.render("WEAPON UPGRADED!", True, (0, 255, 255))
            msg_rect = msg_surf.get_rect(center=(screen.get_width()//2, screen.get_height()//2 - 100))
            s_val = 1.0 + 0.1 * math.sin(pygame.time.get_ticks() * 0.01)
            scaled_msg = pygame.transform.rotozoom(msg_surf, 0, s_val)
            screen.blit(scaled_msg, scaled_msg.get_rect(center=msg_rect.center))
            
        if invincibility_timer > 0:
            invincibility_timer -= 1
            
        health_bar(screen, 50, 10, hp, 5 + stats['max_hp_bonus'], width=150, height=15)
        dt = fps.get_time() / 1000.0
        particle_manager.update(dt)
        particle_manager.draw(screen)

        if pygame.mouse.get_pressed()[0]:
            if shoot_cooldown <= 0 and ammo > 0:
                create_laser(rays_this_shot(), ls_inf, pl_inf, laser_sound)
                muzzle_flash_timer = 3
                shoot_cooldown = 10
        
        if shoot_cooldown > 0: shoot_cooldown -= 1

        # Frame-based timer thay cho USEREVENT (tương thích web)
        _egg_frame_counter += 1
        _countdown_frame_counter += 1

        if _egg_frame_counter >= _egg_frame_interval:
            _egg_frame_counter = 0
            if meteor_mode:
                for _ in range(random.randint(1, 2)):
                    bx = random.choice([random.randint(0, Max[0]), -50, Max[0] + 50])
                    by = random.randint(-150, -50)
                    big_egg_inf['pos'].append((bx, by))
                    big_egg_inf['direct'].append(bx > Max[0] // 2)
            else:
                create_egg(lv_game, egg_inf, ck_inf, boss_mode, tuple(boss_pos) if boss_mode else None, big_egg_inf)

        if _countdown_frame_counter >= _countdown_frame_interval:
            _countdown_frame_counter = 0
            count -= 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT: close()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3: 
                    if current_missiles_count > 0:
                        mx_pos = pl_inf['pos'][0][0] if isinstance(pl_inf['pos'][0], tuple) else pl_inf['pos'][0]
                        my_pos = pl_inf['pos'][0][1] if isinstance(pl_inf['pos'][0], tuple) else pl_inf['pos'][1]
                        pw = pl_inf['img'].get_width()
                        half_w_missile = pw // 2
                        missile_inf['items'].append({'x': mx_pos + half_w_missile, 'y': my_pos})
                        current_missiles_count -= 1
                        laser_sound.play()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    choose = await create_menu(screen, menu_pause())
                    if choose == 2: break
                    elif choose == 3:
                        current_missiles_count = 0
                        w_file(1, 1, 0, 5, 0, difficulty, 0, skin_index, starting_ammo(difficulty), u_data[9], u_speed, u_hp, u_missile)
                        return (False, motors_collected, ultimate_energy, gift_rays)
                elif event.key == pygame.K_SPACE and ultimate_energy >= 100:
                    ultimate_energy = 0
                    ultimate_storm_timer = 240
                    screen_shake = 30
                    screen_show_mess(screen, "ULTIMATE! LASER STORM ACTIVATED!")
                    await asyncio.sleep(0.5)

        stage_clear = False
        if boss_mode:
            if boss_hp <= 0:
                stage_clear = True
                motors_collected += 50
        elif meteor_mode:
            if count <= 0: stage_clear = True
        else:
            if len(ck_inf['pos']) == 0 and len(score_inf['pos']) == 0 and len(gift_inf['pos']) == 0:
                stage_clear = True

        if stage_clear:
            if boss_mode:
                screen_show_mess(screen, "CHIẾN THẮNG BOSS! CHÚC MỪNG BẠN!")
                await asyncio.sleep(3)
            else:
                screen_show_mess(screen, f"HOÀN THÀNH MÀN {lv_game}!")
                await asyncio.sleep(1.5)

            lv_game += 1
            ammo += (25 + lv_game * 5)
            w_file(lv_game, lv_gun, score, hp, gift_rays, difficulty, current_missiles_count, skin_index, ammo, u_data[9], u_data[10], u_data[11], u_data[12])
            return (True, motors_collected, ultimate_energy, gift_rays)

        if (not meteor_mode and count <= 0) or hp <= 0:
            screen_show_mess(screen, 'YOU LOSE')
            await asyncio.sleep(3)
            record_high_score(score)
            w_file(1, 1, 0, 5, 0, 2, 0, skin_index, starting_ammo(2), u_data[9], u_data[10], u_data[11], u_data[12])
            return (False, motors_collected, ultimate_energy, gift_rays)

        if lv_gun < len(gun) - 1 and score >= gun[lv_gun][req_score_gun]:
            lv_gun += 1
            level_up_msg_timer = 120
            collision_sound.play()

        if boss_mode and boss_hp > 0 and boss_img is not None:
            bw = boss_img.get_width()
            boss_pos[0] += boss_vx
            if boss_pos[0] < 35 or boss_pos[0] > Max[0] - bw - 35: boss_vx *= -1
            boss_pos[1] = 84 + int(52 * math.sin(pygame.time.get_ticks() * 0.0028))
            
        if not boss_mode:
            if lv_game > 3:
                move_ck(ck_inf, ck_step)
                move_eggs(egg_inf, egg_dy, egg_horiz)
            else: move(egg_dy, egg_inf)
            
        move_eggs(big_egg_inf, big_fall, big_hz)
        move(-gun[lv_gun][speed_gun], ls_inf)
        cull_missiles(missile_inf, Max)
        move(1, score_inf)
        move(1, gift_inf)
        out_screen(ls_inf, Max)
        out_screen(score_inf, Max)
        out_screen(gift_inf, Max)
        out_screen_egg(lv_game, egg_inf, Max)
        out_screen_egg(lv_game, big_egg_inf, Max)

        if boss_mode and boss_hp > 0 and boss_img is not None:
            br = pygame.Rect(boss_pos[0], boss_pos[1], boss_img.get_width(), boss_img.get_height())
            for li in range(len(ls_inf['pos']) - 1, -1, -1):
                ls_inf['rect'].topleft = ls_inf['pos'][li]
                if ls_inf['rect'].colliderect(br):
                    boom_sound.play()
                    ck_pos = (boss_pos[0] + bw // 2, boss_pos[1] + boss_img.get_height() // 2)
                    particle_manager.emit(ck_pos, color=(255, 180, 0), max_radius=30, lifetime=0.4, count=8)
                    shake_timer = 3
                    boss_hp -= 1
                    particle_manager.emit((boss_pos[0] + bw // 2, boss_pos[1] + boss_img.get_height() // 2), color=(255, 100, 0), max_radius=40, lifetime=0.6, count=12)
                    shake_timer = 5
                    ls_inf['pos'].pop(li)
                    if boss_hp <= 0: break
        else:
            check = collision(ls_inf, ck_inf)
            if check is not None:
                boom_sound.play()
                ci = check[1]
                ck_pos = ck_inf['pos'][ci]
                ck_dir = ck_inf['direct'][ci] if lv_game > 3 else False
                kind = roll_chicken_drop(gifts_spawned_stage)
                particle_manager.emit((ck_pos[0]+25, ck_pos[1]+25), color=(255, 220, 80), max_radius=22, lifetime=0.5, count=10)
                if kind == 'gift':
                    gifts_spawned_stage += 1
                    gift_inf['pos'].append(ck_pos)
                    gift_inf['types'].append(random.choice(['rays', 'shield', 'ammo', 'hp']))
                elif kind == 'drumstick':
                    gift_inf['pos'].append(ck_pos)
                    gift_inf['types'].append('motor')
                    particle_manager.emit(ck_pos, color=(255, 215, 0), count=5)
                elif kind == 'egg':
                    egg_inf['pos'].append(change_pos(ck_pos, (10, 50)))
                    if lv_game > 3: egg_inf['direct'].append(ck_dir)
                else: score_inf['pos'].append(ck_pos)
                ls_inf['pos'].pop(check[0])
                ck_inf['pos'].pop(ci)
                if lv_game > 3: ck_inf['direct'].pop(ci)
            else:
                check_meteor = collision(ls_inf, big_egg_inf)
                if check_meteor is not None:
                    mi = check_meteor[1]
                    m_pos = big_egg_inf['pos'][mi]
                    particle_manager.emit(m_pos, color=(150, 150, 150), count=12)
                    big_egg_inf['pos'].pop(mi)
                    big_egg_inf['direct'].pop(mi)
                    ls_inf['pos'].pop(check_meteor[0])
                    boom_sound.play()
                    if random.random() < GIFT_DROP_RATE:
                        gift_inf['pos'].append(m_pos)
                        gift_inf['types'].append(random.choice(['rays', 'shield', 'ammo', 'hp']))

        if missile_inf['items']:
            for mi in range(len(missile_inf['items']) - 1, -1, -1):
                m = missile_inf['items'][mi]
                missile_inf['rect'].topleft = (int(m['x']), int(m['y']))
                if boss_mode and boss_hp > 0 and boss_img is not None:
                    br = pygame.Rect(boss_pos[0], boss_pos[1], boss_img.get_width(), boss_img.get_height())
                    if missile_inf['rect'].colliderect(br):
                        boom_sound.play()
                        boss_hp -= 55
                        missile_inf['items'].pop(mi)
                        continue
                target = find_best_target(pl_inf['pos'], ck_inf, boss_mode, boss_pos, boss_img)
                if target:
                    dx = target[0] - m['x']
                    dy = target[1] - m['y']
                    distance = math.hypot(dx, dy)
                    if distance > 0:
                        missile_speed = 13 
                        m['x'] += (dx / distance) * missile_speed
                        m['y'] += (dy / distance) * missile_speed
                else: m['y'] -= 13

                hit_mi = None
                for b_i in range(len(big_egg_inf['pos'])):
                    big_egg_inf['rect'].topleft = big_egg_inf['pos'][b_i]
                    if missile_inf['rect'].colliderect(big_egg_inf['rect']):
                        hit_mi = b_i
                        break
                if hit_mi is not None:
                    boom_sound.play()
                    m_pos = big_egg_inf['pos'][hit_mi]
                    particle_manager.emit(m_pos, color=(150, 150, 150), count=20)
                    big_egg_inf['pos'].pop(hit_mi)
                    big_egg_inf['direct'].pop(hit_mi)
                    missile_inf['items'].pop(mi)
                    ultimate_energy = min(100, ultimate_energy + 10)
                    motors_collected += 8 
                    if motors_collected > 0 and motors_collected % 50 == 0: current_missiles_count += 1
                    if random.random() < GIFT_DROP_RATE:
                        gift_inf['pos'].append(m_pos)
                        gift_inf['types'].append(random.choice(['rays', 'shield', 'ammo', 'hp']))
                    continue

                hit_ci = None
                for ci in range(len(ck_inf['pos'])):
                    ck_inf['rect'].topleft = ck_inf['pos'][ci]
                    if missile_inf['rect'].colliderect(ck_inf['rect']):
                        hit_ci = ci
                        break

                if hit_ci is not None:
                    boom_sound.play()
                    ck_pos = ck_inf['pos'][hit_ci]
                    ck_dir = (ck_inf['direct'][hit_ci] if lv_game > 3 else False)
                    kind = roll_chicken_drop(gifts_spawned_stage)
                    if kind == 'gift':
                        gifts_spawned_stage += 1
                        gift_inf['pos'].append(ck_pos)
                        gift_inf['types'].append(random.choice(['rays', 'shield', 'ammo', 'hp']))
                    elif kind == 'egg':
                        egg_inf['pos'].append(change_pos(ck_pos, (10, 50)))
                        if lv_game > 3: egg_inf['direct'].append(ck_dir)
                    else: score_inf['pos'].append(ck_pos)
                    ck_inf['pos'].pop(hit_ci)
                    if lv_game > 3: ck_inf['direct'].pop(hit_ci)
                    missile_inf['items'].pop(mi)

        check = collision(egg_inf, pl_inf)
        if check is not None:
            collision_sound.play()
            ex, ey = egg_inf['pos'][check[0]]
            ew = egg_inf['img'].get_width()
            eh = egg_inf['img'].get_height()
            hit_bursts.append({'pos': (ex + ew // 2, ey + eh // 2), 'ttl': 22})
            egg_inf['pos'].pop(check[0])
            if lv_game > 3: egg_inf['direct'].pop(check[0])
            ammo = max(0, ammo - EGG_AMMO_LOSS)
            if invincibility_timer <= 0 and shield_timer <= 0:
                hp -= 1
                if gift_rays > 0:
                    gift_rays -= 1
                invincibility_timer = 60 
                shake_timer = 10
                particle_manager.emit(pl_inf['pos'][0], color=(255, 0, 0), count=15)

        check = collision(big_egg_inf, pl_inf)
        if check is not None:
            collision_sound.play()
            ex, ey = big_egg_inf['pos'][check[0]]
            ew = big_egg_inf['img'].get_width()
            eh = big_egg_inf['img'].get_height()
            hit_bursts.append({'pos': (ex + ew // 2, ey + eh // 2), 'ttl': 26})
            big_egg_inf['pos'].pop(check[0])
            big_egg_inf['direct'].pop(check[0])
            ammo = max(0, ammo - BIG_EGG_AMMO_LOSS)
            if invincibility_timer <= 0 and shield_timer <= 0:
                hp -= 2
                if gift_rays > 0:
                    gift_rays -= 1
                invincibility_timer = 90
                shake_timer = 15
                particle_manager.emit(pl_inf['pos'][0], color=(255, 50, 0), count=20)

        check = collision(score_inf, pl_inf)
        if check is not None:
            score_inf['pos'].pop(check[0])
            old_s = score
            score += 1
            if score // 50 > old_s // 50: missiles += 1
            plus_hp = False

        check = collision(gift_inf, pl_inf)
        if check is not None:
            g_idx = check[0]
            g_type = gift_inf['types'][g_idx]
            gift_inf['pos'].pop(g_idx)
            gift_inf['types'].pop(g_idx)
            if g_type == 'rays':
                gift_rays = min(6, gift_rays + 1)  # permanent up to max 6
                particle_manager.emit(pl_inf['pos'][0], color=(0, 255, 255), count=15)
            elif g_type == 'shield':
                shield_timer += 480
                particle_manager.emit(pl_inf['pos'][0], color=(100, 200, 255), count=15)
            elif g_type == 'ammo':
                ammo += GIFT_AMMO_BONUS
                particle_manager.emit(pl_inf['pos'][0], color=(255, 255, 255), count=15)
            elif g_type == 'hp':
                hp += 1
                particle_manager.emit(pl_inf['pos'][0], color=(255, 100, 100), count=15)
            elif g_type == 'motor':
                motors_collected += 1
                ultimate_energy = min(100, ultimate_energy + 2)
                particle_manager.emit(pl_inf['pos'][0], color=(255, 215, 0), count=15)
                if motors_collected > 0 and motors_collected % 50 == 0: current_missiles_count += 1
            collision_sound.play()

        if score % game[lv_game][req_plus_hp] == 0 and score != 0 and plus_hp is False:
            hp += 1
            plus_hp = True

        mx, my = pygame.mouse.get_pos()
        pw, ph = size_player
        half_w = pw // 2
        half_h = ph // 2
        nx = max(0, min(Max[0] - pw, mx - half_w))
        ny = max(0, min(Max[1] - ph, my - half_h))
        
        player_target_pos = [nx, ny]
        move_speed = 0.5 * stats['speed_mult']
        player_current_pos[0] += (player_target_pos[0] - player_current_pos[0]) * move_speed
        player_current_pos[1] += (player_target_pos[1] - player_current_pos[1]) * move_speed
        pl_inf['pos'][0] = (int(player_current_pos[0]), int(player_current_pos[1]))

        if hp <= 0:
            current_missiles_count = 0
            w_file(1, 1, 0, 5, 0, difficulty, 0, skin_index, starting_ammo(difficulty), u_data[9], u_data[10], u_data[11], u_data[12])
            screen_show_mess(screen, 'GAME OVER - Tên lửa đuổi trận sau sẽ tính lại')
            await asyncio.sleep(2)
            return (False, motors_collected, ultimate_energy, gift_rays)

        await asyncio.sleep(0) 

    if load[0] < len(game):
        return (True, motors_collected, ultimate_energy, gift_rays) 
    else:
        screen_show_mess(screen, 'YOU WIN! Chúc mừng bạn đã hoàn thành game!')
        await asyncio.sleep(3)
        record_high_score(score)
        w_file(1, 1, 0, 5, 0, 2, 0, skin_index, starting_ammo(2), u_data[9], u_data[10], u_data[11], u_data[12])
        return (False, motors_collected, ultimate_energy, gift_rays)