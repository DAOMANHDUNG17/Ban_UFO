from process import (
    close,
    create_game,
    create_menu,
    hangar_menu,
    highscores_menu,
    loop_playing,
    r_file,
    w_file,
)
from var import (
    menu_difficulty,
    menu_load,
    menu_start,
    save_file_path,
    starting_ammo,
)
import os


def main():
    screen = create_game('ChickenInvader')
    while True:
        select_start = create_menu(screen, menu_start())
        if select_start == 1:
            diff_sel = create_menu(screen, menu_difficulty())
            difficulty = diff_sel
            prev = r_file()
            sk = prev[7] if len(prev) > 7 else 0
            if os.path.exists(save_file_path()):
                select_load = create_menu(screen, menu_load())
                if select_load == 1:
                    load_inf = r_file()
                    loop_playing(screen, load_inf)
                elif select_load == 2:
                    w_file(
                        1,
                        1,
                        0,
                        5,
                        0,
                        difficulty,
                        0,
                        sk,
                        starting_ammo(difficulty),
                    )
                    loop_playing(screen, None, difficulty)
            else:
                loop_playing(screen, None, difficulty)
        elif select_start == 2:
            highscores_menu(screen)
        elif select_start == 3:
            hangar_menu(screen)
        elif select_start == 4:
            close()


if __name__ == "__main__":
    main()
