import os

import pygame

_ROOT = os.path.dirname(os.path.abspath(__file__))
_DATA = os.path.normpath(os.path.join(_ROOT, '..', 'Data'))

GIFT_DROP_RATE = 0.08
MAX_GIFTS_PER_STAGE = 2

def starting_ammo(difficulty):
    return 999999


def save_file_path():
    return os.path.join(_DATA, 'save', 'save.txt')


def highscores_file_path():
    return os.path.join(_DATA, 'save', 'highscores.txt')


def max_rays_per_shot():
    return 6


def _img_path(name):
    return os.path.join(_DATA, 'image', name)


def ship_skin_filenames():
    return [
        'spaceship.png',
        'spaceship_blue.png',
        'spaceship_green.png',
        'spaceship_red.png',
    ]


def all_img():
    return {
        'bg': _img_path('background.png'),
        'score': _img_path('score.png'),
        'hp': _img_path('hp.png'),
        'motor': _img_path('motor.png'),
        'player': _img_path('spaceship.png'),
        'chicken': _img_path('chicken.png'),
        'laser': _img_path('laser.png'),
        'egg': _img_path('egg.png'),
        'explode': _img_path('explode.png'),
        'gift': _img_path('gift.png'),
    }


def all_size():
    item_size = (50, 50)
    return {
        'bg': (1366, 768),
        'score_txt': 50,
        'hp_txt': 50,
        'hp': item_size,
        'score': item_size,
        'gift': item_size,
        'player': (60, 60),
        'chicken': (50, 50),
        'laser': (20, 40),
        'egg': (30, 40),
        'motor': (50, 50),
        'explode': (60, 60),
        'font': 50,
        'small_font': 25,
        'title': 100
    }


def all_music():
    dir_music = os.path.join(_DATA, 'music')
    return {
        'bg': os.path.join(dir_music, 'level1.ogg'),
        'shoot': os.path.join(dir_music, 'shoot.wav'),
        'explode_ck': os.path.join(dir_music, 'chicken.mp3'),
        'collision': os.path.join(dir_music, 'boom.wav'),
    }


def all_position():
    return {
        'bg': (0, 0),
        'score': (0, 0),
        'hp': (0, 60),
        'pause': (1250, 5),
        'main_menu': (500, 100)
    }


_FONTS = {}

def text(string='Unknown', size=50, color='Yellow', underline=False, bold=False, italic=False, smooth=True):
    font_path = os.path.join(_DATA, 'font', 'VT323-Regular.ttf')
    font_key = (size, bold, italic, underline)
    if font_key not in _FONTS:
        try:
            f = pygame.font.Font(font_path, size)
        except:
            f = pygame.font.SysFont('Arial', size)
        f.set_underline(underline)
        f.set_bold(bold)
        f.set_italic(italic)
        _FONTS[font_key] = f
    
    return _FONTS[font_key].render(string, smooth, color)


_IMG_CACHE = {}

def get_img(name_img='bg', name_size=None):
    if not name_size:
        name_size = name_img
    cache_key = (name_img, name_size)
    if cache_key not in _IMG_CACHE:
        img = all_img()
        size = all_size()
        x = pygame.image.load(img[name_img]).convert_alpha()
        _IMG_CACHE[cache_key] = pygame.transform.scale(x, size[name_size])
    return _IMG_CACHE[cache_key]


def make_player_ship(skin_index):

    w, h = all_size()['player']

    s = pygame.Surface((w, h), pygame.SRCALPHA)

    palettes = [
        ((50, 200, 255), (10, 100, 255), (200, 255, 255)),
        ((255, 100, 50), (200, 40, 10), (255, 220, 150)),
        ((100, 255, 150), (20, 180, 80), (200, 255, 220)),
        ((255, 100, 220), (180, 20, 120), (255, 200, 240)),
    ]

    main, dark, light = palettes[skin_index % len(palettes)]

    # Main Body Base
    pygame.draw.polygon(s, (80, 90, 100), [(w//2, 2), (w-8, h//2+5), (w//2, h-5), (8, h//2+5)])
    
    # Wings
    pygame.draw.polygon(s, dark, [(w//2, 10), (w-2, h-10), (w-12, h-4), (w//2, h-16)])
    pygame.draw.polygon(s, dark, [(w//2, 10), (2, h-10), (12, h-4), (w//2, h-16)])

    # Cockpit
    pygame.draw.polygon(s, main, [(w//2, 15), (w//2+12, h//2+10), (w//2-12, h//2+10)])
    pygame.draw.ellipse(s, (180, 230, 255, 200), (w//2-6, 18, 12, 18))

    # Engines
    pygame.draw.circle(s, (255, 150, 50), (w//2-8, h-5), 4)
    pygame.draw.circle(s, (255, 150, 50), (w//2+8, h-5), 4)
    pygame.draw.circle(s, (255, 255, 255), (w//2-8, h-3), 2)
    pygame.draw.circle(s, (255, 255, 255), (w//2+8, h-3), 2)

    # Laser blasters
    pygame.draw.line(s, light, (8, h//2+5), (8, 10), 2)
    pygame.draw.line(s, light, (w-8, h//2+5), (w-8, 10), 2)

    return s.convert_alpha()


def make_enemy_sprite(variant=0):

    w, h = all_size()['chicken']

    s = pygame.Surface((w, h), pygame.SRCALPHA)

    skins = [
        ((180, 80, 255), (100, 20, 200), (0, 255, 255)),
        ((255, 80, 110), (180, 20, 50), (255, 255, 0)),
        ((80, 200, 170), (20, 120, 90), (255, 0, 255)),
        ((255, 190, 60), (180, 100, 20), (0, 255, 0)),
    ]

    body, shadow, light = skins[variant % len(skins)]

    # Glass dome (more 3D)
    pygame.draw.ellipse(s, (150, 200, 255, 150), (w // 2 - 14, 5, 28, 24))
    pygame.draw.ellipse(s, (220, 240, 255, 200), (w // 2 - 8, 8, 12, 10))

    # UFO Body (metallic rings)
    pygame.draw.ellipse(s, (60, 60, 70), (2, 20, w - 4, 18))
    pygame.draw.ellipse(s, shadow, (4, 21, w - 8, 16))
    pygame.draw.ellipse(s, body, (6, 22, w - 12, 14))
    pygame.draw.ellipse(s, (200, 200, 200, 100), (8, 23, w - 16, 6))

    # Base dome
    pygame.draw.ellipse(s, (50, 50, 60), (w // 2 - 10, 32, 20, 8))

    # Lights (more detailed)
    pygame.draw.circle(s, light, (10, 29), 3)
    pygame.draw.circle(s, (255, 255, 255), (10, 29), 1)
    
    pygame.draw.circle(s, light, (w // 2, 32), 4)
    pygame.draw.circle(s, (255, 255, 255), (w // 2, 32), 2)
    
    pygame.draw.circle(s, light, (w - 10, 29), 3)
    pygame.draw.circle(s, (255, 255, 255), (w - 10, 29), 1)

    return s.convert_alpha()


def make_meteor_egg(big=False):

    w, h = (56, 72) if big else all_size()['egg']

    s = pygame.Surface((w, h), pygame.SRCALPHA)

    pygame.draw.ellipse(s, (140, 110, 95), (2, 4, w - 4, h - 8))

    pygame.draw.ellipse(s, (190, 170, 140), (4, 6, w - 8, h - 12))

    for ox, oy in [(8, 14), (w - 14, 20), (w // 2, h - 12)]:

        pygame.draw.circle(s, (100, 80, 70), (ox, oy), 4)

    return s.convert_alpha()


def load_ship_skin(index):

    return make_player_ship(index)


def load_ship_skin_png_fallback(index):

    names = ship_skin_filenames()

    idx = max(0, min(len(names) - 1, index))

    path = _img_path(names[idx])

    size = all_size()['player']

    if os.path.isfile(path):

        raw = pygame.image.load(path).convert_alpha()

        return pygame.transform.scale(raw, size)

    return make_player_ship(index)


def gift_placeholder_img():
    s = pygame.Surface(all_size()['gift'], pygame.SRCALPHA)
    pygame.draw.rect(s, (160, 82, 45), (6, 14, 38, 28))
    pygame.draw.rect(s, (218, 165, 32), (10, 8, 30, 12))
    pygame.draw.rect(s, (180, 40, 40), (14, 22, 22, 14))
    return s.convert_alpha()


def get_gift_img():
    path = all_img()['gift']
    if os.path.isfile(path):
        return get_img('gift')
    return gift_placeholder_img()


def menu_start():
    size = all_size()
    return [
        text('MENU CHÍNH', size['title'], 'Red'),
        text('Bắt đầu chơi', size['font'], 'Yellow', True),
        text('Bảng điểm', size['font'], 'Yellow', True),
        text('Phi thuyền', size['font'], 'Yellow', True),
        text('Cửa hàng', size['font'], 'Cyan', True),
        text('Hướng dẫn', size['font'], 'Yellow', True),
        text('Thoát game', size['font'], 'Yellow', True),
    ]


def menu_difficulty():
    size = all_size()
    return [
        text('ĐỘ KHÓ', size['title'], 'Red'),
        text('Dễ', size['font'], 'Green', True),
        text('Vừa', size['font'], 'Yellow', True),
        text('Khó', size['font'], 'Red', True),
        text('Quay lại', size['font'], 'White', True),
    ]


def menu_load():
    size = all_size()
    return [
        text('CHẾ ĐỘ CHƠI', size['title'], 'Red'),
        text('Tiếp tục', size['font'], 'Yellow', True),
        text('Chơi mới', size['font'], 'Yellow', True),
        text('Quay lại', size['font'], 'White', True),
    ]


def menu_pause():
    size = all_size()
    return [
        text('TẠM DỪNG', size['title'], 'Red'),
        text('Tiếp tục', size['font'], 'Yellow', True),
        text('Chơi lại', size['font'], 'Yellow', True),
        text('Thoát ra Menu', size['font'], 'White', True)
    ]


def player_inf(skin_index=0):

    pl = load_ship_skin(skin_index)

    explode = get_img('explode')

    return {
        'img': pl,
        'img_explode': explode,
        'rect': pl.get_rect(),
        'pos': [(600, 650)],
        'move': 5,
        'skin_index': skin_index,
    }

def w_file(
    lv_game,
    lv_gun,
    score,
    hp,
    gift_rays=0,
    difficulty=2,
    missiles=0,
    skin_index=0,
    ammo=None,
    feathers=0,
    u_speed=0,
    u_hp=0,
    u_missile=0,
    ultimate_energy=0,
):
    if ammo is None:
        ammo = starting_ammo(2)
    path = save_file_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    data = [
        f"{lv_game}\n", f"{lv_gun}\n", f"{score}\n", f"{hp}\n",
        f"{gift_rays}\n", f"{difficulty}\n", f"{missiles}\n",
        f"{skin_index}\n", f"{ammo}\n", f"{feathers}\n",
        f"{u_speed}\n", f"{u_hp}\n", f"{u_missile}\n",
        f"{ultimate_energy}\n"
    ]
    with open(path, 'w') as file:
        file.writelines(data)

def r_file():
    path = save_file_path()
    if not os.path.exists(path):
        d = [1, 1, 0, 5, 0, 2, 0, 0, starting_ammo(2), 0, 0, 0, 0]
        w_file(*d)
        return d
    x = []
    with open(path) as file:
        for line in file:
            line = line.strip()
            if line != '': x.append(int(line))
    # Migration/Padding
    while len(x) < 14:
        if len(x) == 9: x.extend([0, 0, 0, 0, 0]) # Add feathers & upgrades & ultimate
        elif len(x) == 13: x.append(0)
        else: x.append(0)
    return x

def upgrade_costs(level):
    # Tiered pricing: level 0 -> 50, 1 -> 250, 2 -> 550, 3 -> 950...
    return 50 + (level * 200) + (level**2 * 100)

def get_stat_bonus(u_speed, u_hp, u_missile):
    return {
        'speed_mult': 1.0 + (u_speed * 0.1),
        'max_hp_bonus': u_hp,
        'missile_cd_red': u_missile * 0.15
    }

def chicken_inf(enemy_variant=0):

    ck = make_enemy_sprite(enemy_variant)

    explode = get_img('explode')

    return {
        'img': ck,
        'img_explode': explode,
        'rect': ck.get_rect(),
        'pos': [],
        'direct': [],
        'pattern': [],
        'base_y': [],
        'time_offset': [],
    }


def laser_inf():
    ls = get_img('laser')
    return {
        'img': ls,
        'rect': ls.get_rect(),
        'pos': []
    }


def eg_inf():

    egg = make_meteor_egg(big=False)

    return {
        'img': egg,
        'rect': egg.get_rect(),
        'pos': [],
        'direct': [],
    }


def eg_inf_big():

    egg = make_meteor_egg(big=True)

    return {
        'img': egg,
        'rect': egg.get_rect(),
        'pos': [],
        'direct': [],
    }


def sc_inf():
    sc = get_img('score', 'egg')
    return {
        'img': sc,
        'rect': sc.get_rect(),
        'pos': []
    }


def gift_pickup_inf():
    g = get_gift_img()
    return {
        'img': g,
        'rect': g.get_rect(),
        'pos': [],
    }


def obj_default_playing():
    pos = all_position()
    size = all_size()
    return [
        [get_img('bg'), pos['bg']],
        [text('Pause(Esc)', size['small_font'], 'Gold'), pos['pause']],
        [
            text(
                'Trúng trứng: Giảm cấp tia | Chuột trái: Bắn | Chuột phải: Tên lửa đuổi',
                size['small_font'],
                'Gold',
            ),
            (560, 5),
        ],
    ]


def game_level():
    """Mỗi màn: [tốc_độ_trứng_ms, số_gà, dự_phòng, thời_gian_s, mốc_+HP, mốc_nâng_súng]."""
    return [
        [],
        [1500, 28, 1, 85, 10, 25],
        [1300, 32, 1, 78, 10, 55],
        [1150, 38, 1, 72, 12, 85],
        [1000, 42, 1, 68, 12, 115],
        [920, 36, 1, 65, 14, 145],
        [820, 40, 3, 110, 14, 175],
        [760, 44, 3, 100, 15, 195],
        [700, 48, 3, 95, 15, 215],
        [640, 52, 3, 90, 16, 235],
        [580, 56, 3, 85, 16, 255],
        [520, 60, 3, 80, 18, 275],
        [480, 52, 4, 75, 18, 295],
        [440, 56, 4, 72, 18, 310],
        [400, 60, 4, 68, 18, 325],
        [380, 54, 4, 64, 16, 340],
        [340, 58, 4, 60, 16, 360],
        [320, 62, 4, 56, 14, 380],
        [300, 56, 4, 52, 14, 400],
        [280, 60, 4, 48, 12, 420],
        [260, 64, 4, 45, 12, 440],
    ]


def gun_level():
    return [
        [],
        [1000, 1, 16, 10],
        [500, 1, 18, 25],
        [1000, 2, 20, 50],
        [800, 2, 22, 80],
        [500, 2, 24, 100],
        [1000, 3, 24, 120],
        [800, 3, 25, 150],
        [500, 3, 25, 200]
    ]
