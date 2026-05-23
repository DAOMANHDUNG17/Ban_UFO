#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test script to check imports and initial function calls without running full game"""

import sys
import traceback

print("=" * 60)
print("TESTING IMPORTS AND INITIAL FUNCTION CALLS")
print("=" * 60)

try:
    print("\n1. Testing process.py import...")
    import process
    print("   ✓ process.py imported successfully")
    
    print("\n2. Testing var.py imports...")
    from var import r_file, w_file, starting_ammo
    print("   ✓ var.py functions imported")
    
    print("\n3. Testing r_file() function...")
    data = r_file()
    print(f"   ✓ r_file() returned {len(data)} items: {data}")
    
    print("\n4. Testing loop_playing function exists...")
    assert hasattr(process, 'loop_playing')
    print("   ✓ loop_playing function exists")
    
    print("\n5. Testing find_best_target function...")
    assert hasattr(process, 'find_best_target')
    print("   ✓ find_best_target function exists")
    
    print("\n6. Testing show_popup function...")
    assert hasattr(process, 'show_popup')
    print("   ✓ show_popup function exists")
    
    print("\n7. Testing key variables/constants...")
    from var import game_level, gun_level, max_rays_per_shot
    game = game_level()
    gun = gun_level()
    print(f"   ✓ game_level has {len(game)} levels")
    print(f"   ✓ gun_level has {len(gun)} levels")
    print(f"   ✓ max_rays_per_shot = {max_rays_per_shot()}")
    
    print("\n" + "=" * 60)
    print("ALL TESTS PASSED!")
    print("=" * 60)
    
except Exception as e:
    print(f"\n✗ ERROR: {e}")
    print("\nFull traceback:")
    traceback.print_exc()
    sys.exit(1)
