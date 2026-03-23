"""
Helper tool to measure the screen area inside a device frame image.

Click the TOP-LEFT corner of the LCD screen area, then the BOTTOM-RIGHT corner.
The resulting rect (x, y, width, height) and DEVICE_OFFSET will be printed.

Usage:
    python tools/measure_screen_area.py [image_path]

Defaults to img/Device.png if no path is provided.
"""

import sys
import os

import pygame as pg

DEFAULT_DEVICE_IMG = os.path.join(os.path.dirname(__file__), "..", "img", "Device.png")


def main():
    image_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_DEVICE_IMG
    pg.init()
    # Load without convert_alpha first to get dimensions, then set mode, then convert
    device_raw = pg.image.load(image_path)
    w, h = device_raw.get_size()

    screen = pg.display.set_mode((w, h))
    device = device_raw.convert_alpha()
    pg.display.set_caption("Click top-left then bottom-right of the LCD screen area — ESC to quit")

    font = pg.font.SysFont(None, 24)
    clicks = []

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                running = False
            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                clicks.append(event.pos)
                if len(clicks) == 2:
                    x1, y1 = clicks[0]
                    x2, y2 = clicks[1]
                    rx, ry = min(x1, x2), min(y1, y2)
                    rw, rh = abs(x2 - x1), abs(y2 - y1)
                    print(f"\nScreen area rect : x={rx}, y={ry}, width={rw}, height={rh}")
                    print(f"DEVICE_OFFSET    : ({rx}, {ry})")
                    print(f"Screen size      : ({rw}, {rh})")
                    running = False

        screen.blit(device, (0, 0))

        for i, (cx, cy) in enumerate(clicks):
            pg.draw.circle(screen, (255, 0, 0), (cx, cy), 6)
            label = ["TOP-LEFT", "BOTTOM-RIGHT"][i]
            txt = font.render(f"{label} ({cx}, {cy})", True, (255, 0, 0))
            screen.blit(txt, (cx + 10, cy - 10))

        if len(clicks) == 0:
            msg = font.render("Click the TOP-LEFT corner of the LCD screen area", True, (255, 255, 0))
        elif len(clicks) == 1:
            msg = font.render("Now click the BOTTOM-RIGHT corner", True, (255, 255, 0))
        else:
            msg = font.render("Done!", True, (0, 255, 0))
        screen.blit(msg, (10, 10))

        mx, my = pg.mouse.get_pos()
        crosshair_color = (255, 255, 0)
        pg.draw.line(screen, crosshair_color, (mx - 10, my), (mx + 10, my), 1)
        pg.draw.line(screen, crosshair_color, (mx, my - 10), (mx, my + 10), 1)
        coord_txt = font.render(f"({mx}, {my})", True, crosshair_color)
        screen.blit(coord_txt, (mx + 14, my + 4))

        pg.display.flip()

    pg.quit()


if __name__ == "__main__":
    main()
