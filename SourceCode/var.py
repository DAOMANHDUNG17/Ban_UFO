import os

import pygame

_ROOT = os.path.dirname(os.path.abspath(__file__))
_DATA = os.path.normpath(os.path.join(_ROOT, '..', 'Data'))

GIFT_DROP_RATE = 0.05
MAX_GIFTS_PER_STAGE = 2

EGG_AMMO_LOSS = 8
BIG_EGG_AMMO_LOSS = 14
GIFT_AMMO_BONUS = 28


def starting_ammo(difficulty):
    return {1: 120, 2: 90, 3: 65}[difficulty]


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


def text(string='Unknown', size=50, color='Yellow', underline=False, bold=False, italic=False, smooth=True):
    font_path = os.path.join(_DATA, 'font', 'VT323-Regular.ttf')
    x = pygame.font.Font(font_path, size)
    x.set_underline(underline)
    x.set_bold(bold)
    x.set_italic(italic)
    return x.render(string, smooth, color).convert_alpha()


def get_img(name_img='bg', name_size=None):
    if not name_size:
        name_size = name_img
    img = all_img()
    size = all_size()
    x = pygame.image.load(img[name_img]).convert_alpha()
    return pygame.transform.scale(x, size[name_size])


def make_player_ship(skin_index):

    w, h = all_size()['player']

    s = pygame.Surface((w, h), pygame.SRCALPHA)

    palettes = [
        ((90, 200, 255), (40, 120, 255), (220, 245, 255)),
        ((255, 140, 90), (200, 70, 40), (255, 230, 200)),
        ((120, 255, 160), (40, 180, 90), (230, 255, 235)),
        ((255, 110, 200), (180, 40, 140), (255, 220, 245)),
    ]

    main, dark, light = palettes[skin_index % len(palettes)]

    pts = [
        (w // 2, 4),
        (w - 6, h - 14),
        (w // 2 + 10, h - 4),
        (w // 2 - 10, h - 4),
        (6, h - 14),
    ]

    pygame.draw.polygon(s, dark, pts)

    pygame.draw.polygon(
        s,
        main,
        [
            (w // 2, 10),
            (w - 12, h - 18),
            (w // 2 + 6, h - 10),
            (w // 2 - 6, h - 10),
            (12, h - 18),
        ],
    )

    pygame.draw.line(s, light, (w // 2, 12), (w // 2, h - 16), 2)

    pygame.draw.circle(s, (255, 255, 255, 200), (w // 2, h // 2 + 4), 4)

    return s.convert_alpha()


def make_enemy_sprite(variant=0):

    w, h = all_size()['chicken']

    s = pygame.Surface((w, h), pygame.SRCALPHA)

    skins = [
        ((190, 90, 255), (120, 40, 200)),
        ((255, 95, 130), (200, 40, 70)),
        ((90, 220, 190), (30, 140, 110)),
        ((255, 210, 80), (200, 120, 30)),
    ]

    body, shadow = skins[variant % len(skins)]

    pygame.draw.ellipse(s, shadow, (5, 10, w - 10, h - 14))

    pygame.draw.ellipse(s, body, (7, 8, w - 14, h - 16))

    pygame.draw.circle(s, (30, 30, 45), (w // 2 - 11, 22), 6)

    pygame.draw.circle(s, (240, 245, 255), (w // 2 - 11, 22), 3)

    pygame.draw.circle(s, (30, 30, 45), (w // 2 + 11, 22), 6)

    pygame.draw.circle(s, (240, 245, 255), (w // 2 + 11, 22), 3)

    pygame.draw.arc(s, (60, 30, 80), (12, 26, w - 24, 14), 3.6, 5.9, 3)

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
        text('MAIN MENU', size['title'], 'Red'),
        text('Play Game', size['font'], 'Yellow', True),
        text('High Scores', size['font'], 'Yellow', True),
        text('Hangar', size['font'], 'Yellow', True),
        text('Exit', size['font'], 'Yellow', True),
    ]


def menu_difficulty():
    size = all_size()
    return [
        text('DIFFICULTY', size['title'], 'Red'),
        text('Easy', size['font'], 'Yellow', True),
        text('Medium', size['font'], 'Yellow', True),
        text('Hard', size['font'], 'Yellow', True),
    ]


def menu_load():
    size = all_size()
    return [
        text('LOAD LEVEL', size['title'], 'Red'),
        text('Previous Level', size['font'], 'Yellow', True),
        text('New Game', size['font'], 'Yellow', True)
    ]


def menu_pause():
    size = all_size()
    return [
        text('PAUSE GAME', size['title'], 'Red'),
        text('Resume', size['font'], 'Yellow', True),
        text('Reload', size['font'], 'Yellow', True)
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


def chicken_inf(enemy_variant=0):

    ck = make_enemy_sprite(enemy_variant)

    explode = get_img('explode')

    return {
        'img': ck,
        'img_explode': explode,
        'rect': ck.get_rect(),
        'pos': [],
        'direct': [],
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
        [get_img('score'), pos['score']],
        [get_img('hp'), pos['hp']],
        [text('Pause(Esc)', size['small_font'], 'Gold'), pos['pause']],
        [
            text(
                'Dan: trung lam mat dan | Trai: ban | Phai: ten lua duoi',
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
        [1000, 1, 8, 10],
        [500, 1, 8, 25],
        [1000, 2, 10, 50],
        [800, 2, 10, 80],
        [500, 2, 10, 100],
        [1000, 3, 10, 120],
        [800, 3, 10, 150],
        [500, 3, 10, 200]
    ]
