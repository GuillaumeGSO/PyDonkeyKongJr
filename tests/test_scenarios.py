"""
Integration tests for PyDonkeyKongJr using the scenario system.

Each test loads a JSON scenario, simulates one or more frames via advance_frame(),
then asserts on the resulting game state.

Key mechanics recap:
  - player.update() runs BEFORE nut.update() each frame.
  - mustFall() checks player.sprite_position at nut.update() time — so if the
    player timer is also expired, the player leaves H2J before nut sees it.
    Use expire_player=False for nut tests where the player must stay at H2J.
  - Nut checks threats at the position it *arrives* at (after advancing), not
    where it starts. Kill map: N01→Croco@C02, N02→Bird@B04, N03→Croco@C09.
  - After any kill: is_score_paused=True + nut._instant_mode=True.
  - Collision grace period: ~animation_delay - 1000/FPS ≈ 467 ms.
    Expire collision_start_time with -= 10_000 to skip the wait.
  - Death animation: 2000 ms. Expire death_start_time with -= 3_000.
"""

import json
import os

import pygame as pg
import pytest

from scenario import dump_state, load_scenario
from tests.conftest import advance_frame


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _load(app, filename):
    path = os.path.join("tests", "scenarios", filename)
    with open(path) as f:
        data = json.load(f)
    load_scenario(app.game, data)


def _player_pos(app):
    p = app.game.player
    return p.sprite_position.position_name if p.sprite_position else None


def _nut_pos(app):
    n = app.game.nut
    return n.spritePosition.position_name if n.spritePosition else None


# ---------------------------------------------------------------------------
# Player / Key tests
# ---------------------------------------------------------------------------

class TestGrabKey:
    def test_grab_key_success(self, headless_app):
        """H3G + UP → H4J, then None → handle_key grabs key, cage opens.

        expire_key=False keeps key at K03 (is_grabable=True). If the key timer
        expires, key advances K03→K02b and is_grabable becomes False before
        handle_key() fires.
        """
        _load(headless_app, "grab_key.json")
        game = headless_app.game

        advance_frame(headless_app, "UP", expire_key=False)
        assert _player_pos(headless_app) == "H4J"

        advance_frame(headless_app, None, expire_key=False)
        assert game.key.is_visible is False
        assert game.cage.remaining_cage == 3
        assert game.score._pending > 0

    def test_grab_key_miss(self, headless_app):
        """H3G + UP → H4J, key not grabable → handle_key returns H7F (falling)."""
        _load(headless_app, "grab_key_miss.json")

        advance_frame(headless_app, "UP", expire_key=False)
        assert _player_pos(headless_app) == "H4J"

        advance_frame(headless_app, None, expire_key=False)
        assert _player_pos(headless_app) == "H7F"

    def test_cage_last_open(self, headless_app):
        """Grab key when cage has 1 part left → cage fully_opened."""
        _load(headless_app, "cage_last_open.json")
        game = headless_app.game

        advance_frame(headless_app, "UP", expire_key=False)   # H3G → H4J
        advance_frame(headless_app, None, expire_key=False)   # handle_key → grab

        assert game.cage.fully_opened is True
        assert game.cage.remaining_cage == 0


# ---------------------------------------------------------------------------
# Collision / death tests
# ---------------------------------------------------------------------------

class TestCollision:
    def test_croco_starts_grace_period(self, headless_app):
        """Player at L1G with croco at C10 (eater): first frame sets collision timer.

        expire_threats=False keeps croco at C10 across frames so collision_start_time
        is not reset (it resets when eater_name no longer matches a threat position).
        """
        _load(headless_app, "croco_kills_player.json")
        game = headless_app.game

        advance_frame(headless_app, None, expire_threats=False)
        assert game.player.collision_start_time is not None
        assert game.player.is_dying is False

    def test_croco_kills_player_after_grace(self, headless_app):
        """After grace period expires, croco kills player."""
        _load(headless_app, "croco_kills_player.json")
        game = headless_app.game

        advance_frame(headless_app, None, expire_threats=False)
        game.player.collision_start_time -= 10_000  # expire grace period
        advance_frame(headless_app, None, expire_threats=False)

        assert game.player.is_dying is True

    def test_game_over(self, headless_app):
        """Third life lost → is_playing becomes False."""
        _load(headless_app, "game_over.json")
        game = headless_app.game

        advance_frame(headless_app, None, expire_threats=False)
        game.player.collision_start_time -= 10_000
        advance_frame(headless_app, None, expire_threats=False)
        assert game.player.is_dying is True

        # Fast-forward death animation (2000 ms)
        game.player.death_start_time -= 3_000
        game.player.last_blink_time -= 3_000
        advance_frame(headless_app, None, expire_threats=False)

        assert game.is_playing is False


# ---------------------------------------------------------------------------
# Nut tests — kills
# ---------------------------------------------------------------------------

class TestNutKills:
    def test_nut_kills_croco_at_n01(self, headless_app):
        """Nut N00 + player H2J + croco C02: mustFall→N01, handleThreats kills croco.

        expire_player=False: player must stay at H2J (player.update runs first;
        if its timer expires the player leaves H2J before nut.mustFall() checks).
        expire_threats=False: croco must stay at C02 until handleThreats() fires
        (croco.update runs before nut.update; if its timer expires it moves away).
        """
        _load(headless_app, "nut_kills_croco_n01.json")
        game = headless_app.game

        advance_frame(headless_app, None, expire_player=False, expire_threats=False)

        assert game.crocos[0].is_killed is True
        assert game.is_score_paused is True
        assert game.nut._instant_mode is True

    def test_nut_kills_bird_at_n02(self, headless_app):
        """Nut N01 + bird B04: nut advances N01→N02, handleThreats kills bird.

        expire_threats=False: bird must stay at B04 until handleThreats() fires.
        """
        _load(headless_app, "nut_kills_bird_n02.json")
        game = headless_app.game

        advance_frame(headless_app, None, expire_threats=False)

        assert game.birds[0].is_killed is True
        assert game.is_score_paused is True
        assert game.nut._instant_mode is True

    def test_nut_kills_croco_at_n03(self, headless_app):
        """Nut N02 + croco C09: nut advances N02→N03, handleThreats kills croco at bottom.

        expire_threats=False: croco must stay at C09 until handleThreats() fires.
        """
        _load(headless_app, "nut_kills_croco_n03.json")
        game = headless_app.game

        advance_frame(headless_app, None, expire_threats=False)

        assert game.crocos[0].is_killed is True
        assert game.nut._killed_at_bottom is True
        assert game.is_score_paused is True


# ---------------------------------------------------------------------------
# Nut tests — passes without kill
# ---------------------------------------------------------------------------

class TestNutPasses:
    def test_nut_passes_n01_no_enemy_at_n02(self, headless_app):
        """Nut N01, no bird at B04: nut advances to N02, no kill."""
        _load(headless_app, "nut_passes_no_enemy.json")
        game = headless_app.game

        advance_frame(headless_app, None)

        assert _nut_pos(headless_app) == "N02"
        assert game.is_score_paused is False
        assert game.nut._instant_mode is False

    def test_nut_passes_n02_no_enemy_at_n03(self, headless_app):
        """Nut N02, no croco at C09: nut advances to N03, no kill, waits at bottom."""
        _load(headless_app, "nut_kills_croco_n03.json")  # same setup, just no croco
        # Override: remove croco so no kill happens
        app = headless_app
        app.game.threat_group.empty()
        for c in app.game.crocos:
            if c.spritePosition:
                c.spritePosition.kill()
            c.is_killed = True
            c.spritePosition = None
        # Also put nut at N02 (already set by JSON)

        advance_frame(headless_app, None)

        assert _nut_pos(headless_app) == "N03"
        assert headless_app.game.nut.is_visible is True     # waiting one beat
        assert headless_app.game.nut._killed_at_bottom is False

    def test_nut_disappears_after_bottom_beat(self, headless_app):
        """Nut at N03 with bottom arrival time expired → nut disappears."""
        _load(headless_app, "nut_passes_no_enemy.json")
        game = headless_app.game

        # Advance nut to N03
        advance_frame(headless_app, None)   # N01 → N02
        advance_frame(headless_app, None)   # N02 → N03, _bottom_arrival_time set

        assert _nut_pos(headless_app) == "N03"
        assert game.nut.is_visible is True

        # Expire the bottom wait timer
        game.nut._bottom_arrival_time -= 10_000
        advance_frame(headless_app, None, expire_nut=True)

        assert game.nut.is_visible is False


# ---------------------------------------------------------------------------
# Nut trigger tests
# ---------------------------------------------------------------------------

class TestNutTrigger:
    def test_nut_triggered_by_player_at_h2j(self, headless_app):
        """Nut N00 + player H2J → mustFall fires, nut moves to N01."""
        _load(headless_app, "nut_trigger.json")

        advance_frame(headless_app, None, expire_player=False)

        assert _nut_pos(headless_app) == "N01"

    def test_nut_not_triggered_when_player_elsewhere(self, headless_app):
        """Nut N00 + player NOT at H2J → nut stays at N00."""
        _load(headless_app, "nut_trigger.json")
        # Override player to L0G (which has no next_move, so player won't move)
        game = headless_app.game
        game.player_group.empty()
        if game.player.sprite_position:
            game.player.sprite_position.kill()
        new_pos = game.player.all_positions["L0G"]
        game.player.sprite_position = new_pos
        game.player_group.add(new_pos)

        advance_frame(headless_app, None, expire_player=False)

        assert _nut_pos(headless_app) == "N00"
