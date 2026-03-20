"""
Pytest configuration for PyDonkeyKongJr tests.

IMPORTANT: SDL env vars must be set at module level, before pygame is imported
anywhere in the process. conftest.py is loaded first by pytest, so this works.
"""

import os
import sys

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
os.chdir(ROOT)

import pygame as pg
import pytest

from main import App
from scenario import load_scenario


@pytest.fixture()
def headless_app():
    """Fully initialised App with headless pygame. Fresh instance per test."""
    app = App()
    yield app
    pg.quit()


def advance_frame(
    app,
    move=None,
    *,
    expire_player=True,
    expire_threats=True,
    expire_nut=True,
    expire_key=True,
):
    """
    Selectively expire actor timers, set player_move, then call game.update().

    pg.time.get_ticks() advances only ~0-2 ms between sequential Python calls,
    which is below every cooldown threshold (125 ms player / 500 ms threats).
    Backdating last_time by 10 s guarantees can_update() returns True.

    Use expire_player=False when the player must stay put at a specific position
    (e.g. H2J) so that nut.mustFall() still sees the player there — player.update()
    runs before nut.update() in game.update(), so an expired player timer would
    advance the player away before the nut check fires.
    """
    game = app.game
    game.player_move = move
    far_past = pg.time.get_ticks() - 10_000
    if expire_player:
        game.player.last_time = far_past
        game.player.last_jump_time = far_past
    if expire_threats:
        for c in game.crocos:
            c.last_time = far_past
        for b in game.birds:
            b.last_time = far_past
    if expire_nut:
        game.nut.last_time = far_past
    if expire_key:
        game.key.last_time = far_past
    game.update()
