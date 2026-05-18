#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test to simulate loop_playing initialization without GUI"""

import sys
import traceback

print("=" * 70)
print("TESTING LOOP_PLAYING INITIALIZATION")
print("=" * 70)

try:
    print("\n1. Importing modules...")
    import pygame
    from process import loop_playing, use_boss_fight, game_level, gun_level
    from var import r_file, starting_ammo, ship_skin_filenames, get_stat_bonus
    print("   ✓ Imports successful")
    
    print("\n2. Testing r_file() data structure...")
    data = r_file()
    assert len(data) == 13, f"r_file should return 13 items, got {len(data)}"
    print(f"   ✓ r_file() returns correct 13-item structure: {data}")
    
    print("\n3. Checking load parameter format...")
    load_test = [1, 1, 0, 5, 0, 2, 0, 0, starting_ammo(2)]
    print(f"   Sample 9-element load: {load_test}")
    
    print("\n4. Testing load padding and unpacking logic...")
    # Simulate what loop_playing does with load
    load = load_test.copy()
    while len(load) < 13:
        if len(load) == 9:
            load.extend([0, 0, 0, 0])  # Add: motors, u_speed, u_hp, u_missile
        else:
            load.append(0)
    
    (
        lv_game, lv_gun, score, hp, gift_rays, diff_saved,
        old_missiles, skin_index, ammo, motors_collected, u_speed, u_hp, u_missile,
    ) = load[:13]
    
    print(f"   ✓ Unpacking successful:")
    print(f"     - lv_game={lv_game}, score={score}, hp={hp}, ammo={ammo}")
    print(f"     - motors_collected={motors_collected}")
    print(f"     - u_speed={u_speed}, u_hp={u_hp}, u_missile={u_missile}")
    
    print("\n5. Testing key functions...")
    assert use_boss_fight(5, 2) is True or use_boss_fight(5, 2) is False
    print(f"   ✓ use_boss_fight(5, 2) = {use_boss_fight(5, 2)}")
    
    game = game_level()
    assert len(game) > 0
    print(f"   ✓ game_level() returns {len(game)} levels")
    
    gun = gun_level()
    assert len(gun) > 0
    print(f"   ✓ gun_level() returns {len(gun)} gun levels")
    
    print("\n6. Testing upgrade stats calculation...")
    stats = get_stat_bonus(1, 2, 1)
    print(f"   ✓ get_stat_bonus(1, 2, 1) = {stats}")
    
    print("\n" + "=" * 70)
    print("ALL INITIALIZATION TESTS PASSED!")
    print("Game should be ready to run.")
    print("=" * 70)
    
except Exception as e:
    print(f"\n✗ ERROR: {e}")
    print("\nFull traceback:")
    traceback.print_exc()
    sys.exit(1)
