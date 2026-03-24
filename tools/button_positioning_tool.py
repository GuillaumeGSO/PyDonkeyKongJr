"""
Interactive tool to calibrate touch button positions on the device frame.

Shows Device.png at its natural resolution. Each button is shown as a labeled
circle. Nudge the selected button with arrow keys, then save with S or ESC.

Usage:
    python tools/button_positioning_tool.py

Controls:
    1-5        Select button (UP, DOWN, LEFT, RIGHT, JUMP)
    Click      Select nearest button
    Arrow keys Nudge selected button 1 px
    S          Save positions to positions/ButtonPositions.json
    ESC        Save and quit
"""

import json
import os
import sys

import pygame as pg

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
os.chdir(ROOT)

from settings import DEVICE_SCREEN_RAW, TOUCH_BUTTON_RADIUS

POSITIONS_FILE = os.path.join("positions", "ButtonPositions.json")
DEVICE_IMG = os.path.join("img", "Device.png")

BUTTON_ORDER = ["UP", "DOWN", "LEFT", "RIGHT", "JUMP"]

BUTTON_COLORS = {
    "UP":    (80, 180, 80),
    "DOWN":  (80, 180, 80),
    "LEFT":  (80, 180, 80),
    "RIGHT": (80, 180, 80),
    "JUMP":  (200, 80, 200),
}


def load_positions():
    if os.path.isfile(POSITIONS_FILE):
        with open(POSITIONS_FILE) as f:
            data = json.load(f)
        return {k: list(v) for k, v in data.items()}
    # Defaults if file missing
    return {
        "UP": [116, 350],
        "DOWN": [117, 434],
        "LEFT": [71, 393],
        "RIGHT": [160, 393],
        "JUMP": [819, 388]
    }


def save_positions(positions):
    with open(POSITIONS_FILE, "w") as f:
        f.write("{\n")
        items = list(positions.items())
        for i, (name, (x, y)) in enumerate(items):
            comma = "," if i < len(items) - 1 else ""
            f.write(f'  "{name}": [{x}, {y}]{comma}\n')
        f.write("}\n")
    print(f"Saved to {POSITIONS_FILE}")


def main():
    pg.init()
    device_raw = pg.image.load(DEVICE_IMG)
    w, h = device_raw.get_size()
    screen = pg.display.set_mode((w, h))
    pg.display.set_caption("Button Positioning — Arrow keys move | 1-5 select | S save | ESC save & quit")
    device = device_raw.convert_alpha()

    font = pg.font.SysFont(None, 22)
    font_label = pg.font.SysFont(None, 18)

    positions = load_positions()
    selected = 0  # index into BUTTON_ORDER

    # Draw the screen area outline so it's clear what's the game vs. device zone
    raw_x, raw_y, raw_w, raw_h = DEVICE_SCREEN_RAW
    screen_rect = pg.Rect(raw_x, raw_y, raw_w, raw_h)

    clock = pg.time.Clock()
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    save_positions(positions)
                    running = False
                elif event.key == pg.K_s:
                    save_positions(positions)
                elif event.key in (pg.K_1, pg.K_2, pg.K_3, pg.K_4, pg.K_5):
                    selected = event.key - pg.K_1
                elif event.key == pg.K_UP:
                    positions[BUTTON_ORDER[selected]][1] -= 1
                elif event.key == pg.K_DOWN:
                    positions[BUTTON_ORDER[selected]][1] += 1
                elif event.key == pg.K_LEFT:
                    positions[BUTTON_ORDER[selected]][0] -= 1
                elif event.key == pg.K_RIGHT:
                    positions[BUTTON_ORDER[selected]][0] += 1
            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                # Select nearest button
                best_i, best_d = 0, float("inf")
                for i, name in enumerate(BUTTON_ORDER):
                    bx, by = positions[name]
                    d = (mx - bx) ** 2 + (my - by) ** 2
                    if d < best_d:
                        best_d, best_i = d, i
                selected = best_i

        screen.blit(device, (0, 0))

        # Outline the game screen area
        pg.draw.rect(screen, (255, 255, 0), screen_rect, 2)

        # Draw buttons
        for i, name in enumerate(BUTTON_ORDER):
            bx, by = positions[name]
            color = BUTTON_COLORS[name]
            pg.draw.circle(screen, color, (bx, by), TOUCH_BUTTON_RADIUS)
            if i == selected:
                pg.draw.circle(screen, (255, 255, 255), (bx, by), TOUCH_BUTTON_RADIUS + 3, 3)
            lbl = font_label.render(name, True, (255, 255, 255))
            screen.blit(lbl, (bx - lbl.get_width() // 2, by - lbl.get_height() // 2))

        # Status bar
        sel_name = BUTTON_ORDER[selected]
        bx, by = positions[sel_name]
        status = font.render(
            f"[{selected+1}] {sel_name}  ({bx}, {by})  — S: save  ESC: save & quit",
            True, (255, 255, 0)
        )
        pg.draw.rect(screen, (0, 0, 0), (0, h - 28, w, 28))
        screen.blit(status, (8, h - 22))

        pg.display.flip()
        clock.tick(30)

    pg.quit()


if __name__ == "__main__":
    main()
