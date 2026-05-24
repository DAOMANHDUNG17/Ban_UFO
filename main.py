import pygame
import asyncio
import os
import sys

if sys.platform == 'emscripten':
    import platform as _platform
    import traceback as _tb
    def custom_excepthook(exc_type, exc_value, exc_tb):
        try:
            err_msg = "".join(_tb.format_exception(exc_type, exc_value, exc_tb))
            print(f"[PYTHON ERROR] {err_msg}")
            try:
                _platform.window.console.error(f"Python Error:\n{err_msg}")
            except Exception:
                pass
        except Exception:
            pass
        sys.__excepthook__(exc_type, exc_value, exc_tb)
    sys.excepthook = custom_excepthook

from process import (
    close,
    create_game,
    create_menu,
    hangar_menu,
    loop_playing,
    r_file,
    w_file,
    highscores_menu,
    shop_menu,
)
from var import (
    menu_difficulty,
    menu_load,
    menu_start,
    save_file_path,
    starting_ammo,
    get_img,
    text,
)

# Hiệu ứng chuyển cảnh fade in/out
async def fade_in(screen, color=(0,0,0), speed=10):
    fade = pygame.Surface(screen.get_size())
    fade.fill(color)
    for alpha in range(255, -1, -speed):
        fade.set_alpha(alpha)
        screen.blit(fade, (0,0))
        pygame.display.update()
        await asyncio.sleep(0.005) # Thay thế delay(5) bằng sleep để không chặn trình duyệt

async def fade_out(screen, color=(0,0,0), speed=10):
    fade = pygame.Surface(screen.get_size())
    fade.fill(color)
    for alpha in range(0, 256, speed):
        fade.set_alpha(alpha)
        screen.blit(fade, (0,0))
        pygame.display.update()
        await asyncio.sleep(0.005)

# Popup thông báo
async def show_popup(screen, title, message, color='Gold', size=60):
    bg = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    bg.fill((0,0,0,180))
    screen.blit(bg, (0,0))
    # Use Segoe UI or Tahoma for better Vietnamese support on Windows
    font_name = 'segoe ui,tahoma,arial'
    font = pygame.font.SysFont(font_name, size, bold=True)
    title_surf = font.render(title, True, color)
    msg_font = pygame.font.SysFont(font_name, 36)
    msg_surf = msg_font.render(message, True, 'White')
    screen.blit(title_surf, (screen.get_width()//2-title_surf.get_width()//2, 200))
    screen.blit(msg_surf, (screen.get_width()//2-msg_surf.get_width()//2, 320))
    pygame.display.update()
    await asyncio.sleep(1.8) # Thay vì delay(1800), ta cho trình duyệt chờ 1.8 giây

# Hướng dẫn chơi
async def show_how_to_play(screen):
    bg = get_img('bg')
    fps = pygame.time.Clock()
    font_name = 'segoe ui,tahoma,arial'
    font_title = pygame.font.SysFont(font_name, 80, bold=True)
    font_msg = pygame.font.SysFont(font_name, 32)
    
    lines = [
        'HƯỚNG DẪN CHƠI',
        '----------------------',
        '• Di chuyển chuột để điều khiển tàu.',
        '• Chuột trái: Bắn tia Laser.',
        '• Chuột phải: Bắn Tên lửa tầm nhiệt.',
        '• ESC: Tạm dừng trò chơi.',
        '',
        'CÁC LOẠI PHẦN THƯỞNG (Gifts):',
        '• Vòng Xanh Cyan: Tăng tia đạn (10 giây - Có cộng dồn).',
        '• Vòng Xanh Dương: Giáp bảo vệ bất tử (8 giây - Có cộng dồn).',
        '• Vòng Trắng: Hồi 50 viên đạn.',
        '• Vòng Đỏ: Hồi 1 Máu (HP).',
        '',
        'Nhấn phím bất kỳ để quay lại...'
    ]
    
    while True:
        fps.tick(30)
        screen.blit(bg, (0, 0))
        y = 100
        for i, line in enumerate(lines):
            color = 'White'
            if i == 0: color = 'Gold'
            elif 'CÁC LOẠI PHẦN THƯỞNG' in line: color = 'Yellow'
            
            surf = font_msg.render(line, True, color)
            if i == 0:
                surf = font_title.render(line, True, 'Gold')
                
            screen.blit(surf, (screen.get_width()//2 - surf.get_width()//2, y))
            y += 45 if i != 0 else 90
            
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                return
                
        # Phải có dòng này trong bất kỳ vòng lặp while True nào
        await asyncio.sleep(0) 

async def main():
    screen = create_game('ChickenInvader')
    await fade_in(screen)
    while True:
        select_start = await create_menu(screen, menu_start(), highlight_color=(255, 215, 0), shadow=True)
        if select_start == 1:
            diff_sel = await create_menu(screen, menu_difficulty(), highlight_color=(0, 255, 255), shadow=True)
            if diff_sel == 4: # 'Back' button in difficulty menu
                continue
            
            difficulty = diff_sel
            if os.path.exists(save_file_path()):
                select_load = await create_menu(screen, menu_load(), highlight_color=(0, 255, 0), shadow=True)
                if select_load == 3: # 'Back' button in load menu
                    continue
                
                if select_load == 1: # Previous Level
                    await fade_out(screen)
                    while True:
                        if not await loop_playing(screen, r_file()): break
                        await asyncio.sleep(0)
                else: # New Game (select_load == 2)
                    prev = r_file()
                    sk = prev[7] if len(prev) > 7 else 0
                    w_file(1, 1, 0, 5, 0, difficulty, 0, sk, starting_ammo(difficulty))
                    await fade_out(screen)
                    while True:
                        if not await loop_playing(screen, r_file()): break
                        await asyncio.sleep(0)
            else:
                await fade_out(screen)
                w_file(1, 1, 0, 5, 0, difficulty, 0, 0, starting_ammo(difficulty))
                while True:
                    if not await loop_playing(screen, r_file()): break
                    await asyncio.sleep(0)
        elif select_start == 2:
            await show_popup(screen, 'HIGHSCORES', 'Top 10 điểm cao nhất sẽ được lưu lại!')
            await highscores_menu(screen)
        elif select_start == 3:
            await hangar_menu(screen)
        elif select_start == 4:
            await shop_menu(screen)
        elif select_start == 5:
            await show_how_to_play(screen)
        elif select_start == 6:
            close()
            
        await asyncio.sleep(0)

if __name__ == "__main__":
    asyncio.run(main())