"""
Scenario Tool — interactive game state loader with step-through debugging.

Usage:
    python tools/scenario_tool.py [scenario.json] [--save-on-quit FILE]

Controls:
    Arrow keys  Queue move (step mode)
    S           Step one frame (step mode)
    T           Toggle step mode on/off
    R           Reload scenario from JSON file
    W           Save current state snapshot to a timestamped JSON file
    ESC         Quit (saves to --save-on-quit path if specified)
"""

import argparse
import json
import os
import sys
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
os.chdir(ROOT)

import pygame as pg

from main import App
from scenario import dump_state, load_scenario
from settings import FPS


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _key_to_move(key):
    return {
        pg.K_LEFT:  "LEFT",
        pg.K_RIGHT: "RIGHT",
        pg.K_UP:    "UP",
        pg.K_DOWN:  "DOWN",
        pg.K_SPACE: "JUMP",
    }.get(key)


def _save_snapshot(game, path=None):
    state = dump_state(game)
    if path is None:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = os.path.join("tools", "scenarios", "snapshots", f"snapshot_{ts}.json")
    with open(path, "w") as f:
        json.dump(state, f, indent=2)
    print(f"[scenario_tool] saved → {path}")


def _croco_positions(game):
    return [
        c.sprite_position.position_name
        for c in game.crocos
        if not c.is_killed and c.sprite_position is not None
    ]


def _bird_positions(game):
    return [
        b.sprite_position.position_name
        for b in game.birds
        if not b.is_killed and b.sprite_position is not None
    ]


def _draw_hud(screen, game, step_mode, frame_count, queued_move):
    p = game.player
    n = game.nut
    k = game.key
    cage = game.cage

    player_pos = p.sprite_position.position_name if p.sprite_position else "None"
    nut_pos = n.sprite_position.position_name if n.sprite_position else "None"
    key_pos = k.sprite_position.position_name if k.sprite_position else "None"
    key_grab = " [GRAB]" if k.is_grabable else ""

    croco_list = "  ".join(_croco_positions(game)) or "(none)"
    bird_list = "  ".join(_bird_positions(game)) or "(none)"

    step_label = "ON (T=toggle)" if step_mode else "OFF"

    lines = [
        f"Frame: {frame_count}       Step: {step_label}",
        f"Player: {player_pos}      Dying: {p.is_dying}",
        f"Crocos: {croco_list}",
        f"Birds:  {bird_list}",
        f"Key: {key_pos}{key_grab}    Nut: {nut_pos}",
        f"Cage: {cage.remaining_cage}/4   Score: {game.score.score} (+{game.score._pending})",
        f"Lives lost: {game.number_of_life}",
        f"Queued: {queued_move or 'none'}",
        "S=step R=reload W=write ESC=quit",
    ]

    font = pg.font.SysFont("monospace", 13)
    pad = 4
    line_h = 16
    bg_w = 310
    bg_h = len(lines) * line_h + pad * 2
    bg_surf = pg.Surface((bg_w, bg_h), pg.SRCALPHA)
    bg_surf.fill((0, 0, 0, 160))
    screen.blit(bg_surf, (4, 4))

    for i, line in enumerate(lines):
        surf = font.render(line, True, (255, 255, 0))
        screen.blit(surf, (pad + 4, pad + 4 + i * line_h))


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="PyDonkeyKongJr Scenario Tool")
    parser.add_argument(
        "scenario",
        nargs="?",
        default=os.path.join("tools", "scenarios", "default.json"),
        help="Path to scenario JSON file",
    )
    parser.add_argument(
        "--save-on-quit",
        metavar="FILE",
        help="Dump state to FILE when ESC is pressed",
    )
    args = parser.parse_args()

    with open(args.scenario) as f:
        scenario_data = json.load(f)

    app = App()
    load_scenario(app.game, scenario_data)

    step_mode = scenario_data.get("step_mode", False)
    queued_move = None
    frame_count = 0

    while True:
        app.game.player_move = None

        for event in pg.event.get():
            if event.type == pg.QUIT:
                _save_snapshot(app.game, args.save_on_quit)
                pg.quit()
                sys.exit()

            if event.type != pg.KEYDOWN:
                continue
            elif event.key == pg.K_ESCAPE:
                _save_snapshot(app.game, args.save_on_quit)
                pg.quit()
                sys.exit()

            elif event.key == pg.K_t:
                step_mode = not step_mode
                queued_move = None

            elif event.key == pg.K_r:
                with open(args.scenario) as f:
                    scenario_data = json.load(f)
                load_scenario(app.game, scenario_data)
                step_mode = scenario_data.get("step_mode", False)
                queued_move = None
                frame_count = 0

            elif event.key == pg.K_w:
                _save_snapshot(app.game)

            elif step_mode:
                if event.key == pg.K_s:
                    # Advance exactly one frame, consuming the queued move
                    app.game.player_move = queued_move
                    queued_move = None
                    app.game.update()
                    frame_count += 1
                else:
                    move = _key_to_move(event.key)
                    if move:
                        queued_move = move

            else:
                move = _key_to_move(event.key)
                if move:
                    app.game.player_move = move

        if not step_mode:
            app.game.update()
            frame_count += 1
            app.clock.tick(FPS)

        # Draw game then overlay HUD on top
        app.game.draw()
        _draw_hud(app.screen, app.game, step_mode, frame_count, queued_move)
        pg.display.flip()


if __name__ == "__main__":
    main()
