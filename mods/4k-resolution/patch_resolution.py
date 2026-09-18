#!/usr/bin/env python3
"""
Imperialism 2 Resolution Patcher
Patches the executable to support custom resolutions.

Usage:
    python patch_resolution.py --width 3840 --height 2160 --exe "Imperialism 2/Imperialism II.exe"
    python patch_resolution.py --restore --exe "Imperialism 2/Imperialism II.exe"
"""

import sys
import struct
import argparse
import shutil
from pathlib import Path

# Resolution constants in the executable
ORIGINAL_WIDTH = 800
ORIGINAL_HEIGHT = 600

def read_exe(exe_path):
    """Read the executable file."""
    with open(exe_path, 'rb') as f:
        return bytearray(f.read())

def write_exe(exe_path, data):
    """Write the executable file."""
    with open(exe_path, 'wb') as f:
        f.write(data)

def backup_exe(exe_path):
    """Create a backup of the original executable."""
    backup_path = Path(str(exe_path) + '.backup')
    if not backup_path.exists():
        shutil.copy2(exe_path, backup_path)
        print(f"Backup created: {backup_path}")
    return backup_path

def find_resolution_patterns(data, width, height):
    """Find all occurrences of resolution values in the binary."""
    # Little-endian 32-bit encoding
    width_bytes = struct.pack('<I', width)
    height_bytes = struct.pack('<I', height)
    
    # Find all instances of width
    width_offsets = []
    for i in range(len(data) - 4):
        if data[i:i+4] == width_bytes:
            width_offsets.append(i)
    
    # Find width-height pairs (height usually within 50 bytes after width)
    pairs = []
    for w_offset in width_offsets:
        for h_offset in range(w_offset + 4, min(w_offset + 50, len(data) - 4)):
            if data[h_offset:h_offset+4] == height_bytes:
                pairs.append((w_offset, h_offset))
                break
    
    return pairs

def patch_resolution(exe_path, new_width, new_height, restore=False):
    """Patch or restore the executable resolution."""
    exe_path = Path(exe_path)
    
    if not exe_path.exists():
        print(f"Error: {exe_path} not found")
        sys.exit(1)
    
    # Create backup on first patch
    backup_path = backup_exe(exe_path)
    
    if restore:
        # Restore from backup
        shutil.copy2(backup_path, exe_path)
        print(f"Restored original: {exe_path}")
        return
    
    data = read_exe(exe_path)
    
    # Find all resolution patterns (width, height pairs)
    pairs = find_resolution_patterns(data, ORIGINAL_WIDTH, ORIGINAL_HEIGHT)
    
    if not pairs:
        print("Error: Could not find resolution patterns in executable")
        sys.exit(1)
    
    print(f"Found {len(pairs)} resolution width-height pairs")
    
    # Encode new resolution in little-endian
    new_width_bytes = struct.pack('<I', new_width)
    new_height_bytes = struct.pack('<I', new_height)
    
    # Patch all occurrences
    for w_offset, h_offset in pairs:
        data[w_offset:w_offset+4] = new_width_bytes
        data[h_offset:h_offset+4] = new_height_bytes
    
    write_exe(exe_path, data)
    print(f"Patched: {new_width}x{new_height}")
    print(f"Original: {ORIGINAL_WIDTH}x{ORIGINAL_HEIGHT}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Patch Imperialism 2 resolution')
    parser.add_argument('--width', type=int, default=3840, help='Target width (default: 3840)')
    parser.add_argument('--height', type=int, default=2160, help='Target height (default: 2160)')
    parser.add_argument('--exe', required=True, help='Path to Imperialism II.exe')
    parser.add_argument('--restore', action='store_true', help='Restore original executable')
    
    args = parser.parse_args()
    
    patch_resolution(args.exe, args.width, args.height, args.restore)
