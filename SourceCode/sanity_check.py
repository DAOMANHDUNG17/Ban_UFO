#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Sanity check for process.py variables"""

import sys

# Check that all critical variables are accessible
code_check = """
import pygame
from process import loop_playing
from var import r_file

# Simulate the start of loop_playing without actually running GUI
load_inf = r_file()
print(f"Load data: {load_inf}")

# Check that key functions exist
from process import (
    show_popup, find_best_target, create_game, create_menu,
    screen_playing, player_inf, chicken_inf, laser_inf,
    eg_inf, eg_inf_big, sc_inf, gift_pickup_inf, missile_weapon_inf,
    use_boss_fight, game_level, gun_level, obj_default_playing,
    draw_parallax_background, health_bar
)

print("✓ All key functions imported successfully")

# Quick syntax check for the game level data
from var import game_level, gun_level
game = game_level()
gun = gun_level()
print(f"✓ Game has {len(game)} levels, Gun has {len(gun)} levels")

print("✓ SANITY CHECK PASSED - Ready to run game")
"""

try:
    exec(code_check)
except Exception as e:
    print(f"✗ Sanity check failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
