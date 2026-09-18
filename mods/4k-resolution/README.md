# Imperialism 2 - 4K Resolution Mod

This mod enables 4K (3840x2160) rendering for Imperialism 2, which was originally locked to 800x600.

## What it does
- Uses DxWnd (DirectX wrapper) to intercept and upscale the game
- Game logic runs at 800x600 internally (compatible)
- Graphics upscaled to 4K on output
- Pixel-perfect scaling preserves the retro look

## Installation
1. Download DxWnd from https://dxwnd.sourceforge.net/
2. Copy the DxWnd folder to this directory
3. Run `dxwnd.exe` to create a profile for `Imperialism II.exe`
4. Set output resolution to 3840x2160

## Building from this mod
See `imperialism2_4k.ini` for DxWnd configuration.

