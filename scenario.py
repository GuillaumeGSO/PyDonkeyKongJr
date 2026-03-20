"""
Scenario system for PyDonkeyKongJr.

Provides load_scenario() and dump_state() to snapshot and restore full game
state from a plain dict (JSON-compatible). Used by both the interactive
scenario tool (tools/scenario_tool.py) and the automated test suite (tests/).

JSON schema:
{
  "description": "...",
  "game":   { "number_of_life": 0, "level": 0, "is_playing": true },
  "player": { "position": "L0G", "is_new_turn": false, "is_dying": false },
  "crocos": [ { "position": "C06" }, { "position": "C00" } ],
  "birds":  [ { "position": "B03" }],
  "nut":    { "position": "N00", "is_visible": true },
  "key":    { "position": "K03", "is_visible": true, "is_grabable": true },
  "cage":   { "remaining_cage": 4, "fully_opened": false },
  "score":  { "score": 0, "pending": 0 },
  "step_mode": false
}
"""

from actors.bird import Bird
from actors.croco import Croco
from settings import ANIMATION_DELAY, DIFFICULTY_STEP, MIN_ANIMATION_DELAY


def load_scenario(game, data):
    """Apply a scenario dict to a live DonkeyKongJr instance."""

    # 1. Game-level state
    game.number_of_life = data["game"]["number_of_life"]
    game.is_playing = data["game"]["is_playing"]
    game.level = data["game"]["level"]
    game.animation_delay = max(
        MIN_ANIMATION_DELAY,
        ANIMATION_DELAY - game.level * DIFFICULTY_STEP,
    )
    game.player_move = None

    # 2. Score — bypass add_points() to avoid triggering is_score_paused
    game.score.score = data["score"]["score"]
    game.score._pending = data["score"]["pending"]
    game.score._last_time = 0

    # 3. Missed display — number_of_life lives lost → show M00…M0(N-1)
    game.info_group.empty()
    game.missed.spritePosition = None
    for i in range(data["game"]["number_of_life"]):
        sp = game.missed.allPositions.get(f"M0{i}")
        game.missed.spritePosition = sp
        game.info_group.add(sp)

    # 4. Player teleport
    #    Always force is_new_turn=False: if True, start_of_game() fires on the
    #    next update() and overrides the position back to L0G.
    p = game.player
    game.player_group.empty()
    if p.sprite_position is not None:
        p.sprite_position.kill()
    p.is_new_turn = False
    p.is_dying = data["player"]["is_dying"]
    p.collision_start_time = None
    p.h7f_entry_time = None
    p.jump_apex_time = None
    p.death_start_time = 0
    p.blink_visible = True
    new_pos = p.all_positions[data["player"]["position"]]
    p.sprite_position = new_pos
    if game.is_playing and not p.is_dying:
        game.player_group.add(new_pos)

    # 5. Threats: clear all, then re-enable requested slots
    game.threat_group.empty()
    game.crocos = []
    for croco_position in data["crocos"]:
        c = Croco(game)
        c.spritePosition = c.all_positions[croco_position["position"]]
        c.is_killed = False
        game.crocos.append(c)
        game.threat_group.add(c.spritePosition)

    game.birds = []
    for bird_position in data["birds"]:
        c = Bird(game)
        c.spritePosition = c.all_positions[bird_position["position"]]
        c.is_killed = False
        game.birds.append(c)
        game.threat_group.add(c.spritePosition)

    # 6. Nut
    n = game.nut
    game.weapon_group.empty()
    if n.spritePosition is not None:
        n.spritePosition.kill()
    n.is_visible = data["nut"]["is_visible"]
    n._instant_mode = False
    n._killed_at_bottom = False
    n._bottom_arrival_time = None
    pos = n.allPositions[data["nut"]["position"]]
    n.spritePosition = pos
    if n.is_visible:
        game.weapon_group.add(pos)

    # 7. Key
    k = game.key
    if k.spritePosition is not None:
        k.spritePosition.kill()
    k.is_visible = data["key"]["is_visible"]
    k.is_grabable = data["key"]["is_grabable"]
    if k.is_visible:
        pos = k.allPositions[data["key"]["position"]]
        k.spritePosition = pos
        game.cage_group.add(pos)
    else:
        k.spritePosition = None

    # 8. Cage reconstruction
    #    init_cage() builds [C03, C02, C01, C00]; open_cage() pops from the
    #    right (C00 first). After N opens, the first `remaining` entries remain.
    cage = game.cage
    game.cage_group.remove(cage.smile_postion)
    for sp in list(cage.sprite_positions):
        game.cage_group.remove(sp)
    remaining = data["cage"]["remaining_cage"]
    all_parts = ["C03", "C02", "C01", "C00"]
    cage.sprite_positions = [cage.all_positions[name] for name in all_parts[:remaining]]
    cage.remaining_cage = remaining
    cage.fully_opened = data["cage"]["fully_opened"]
    if remaining > 0:
        game.cage_group.add(cage.sprite_positions)
    if cage.fully_opened:
        game.cage_group.add(cage.smile_postion)

    # 9. Clear is_score_paused last — nothing above should have set it
    game.is_score_paused = False


def dump_state(game):
    """Serialize current game state to a scenario-compatible dict."""
    p = game.player

    crocos_state = []
    for croco in game.crocos:
        if croco.is_killed or croco.spritePosition is None:
            crocos_state.append(None)
        else:
            crocos_state.append({"position": croco.spritePosition.position_name})

    birds_state = []
    for bird in game.birds:
        if bird.is_killed or bird.spritePosition is None:
            birds_state.append(None)
        else:
            birds_state.append({"position": bird.spritePosition.position_name})

    n = game.nut
    k = game.key

    return {
        "game": {
            "number_of_life": game.number_of_life,
            "level": game.level,
            "is_playing": game.is_playing,
        },
        "player": {
            "position": p.sprite_position.position_name if p.sprite_position else "L0G",
            "is_new_turn": p.is_new_turn,
            "is_dying": p.is_dying,
        },
        "crocos": crocos_state,
        "birds": birds_state,
        "nut": {
            "position": n.spritePosition.position_name if n.spritePosition else "N00",
            "is_visible": n.is_visible,
        },
        "key": {
            "position": k.spritePosition.position_name if k.spritePosition else "K00",
            "is_visible": k.is_visible,
            "is_grabable": k.is_grabable,
        },
        "cage": {
            "remaining_cage": game.cage.remaining_cage,
            "fully_opened": game.cage.fully_opened,
        },
        "score": {
            "score": game.score.score,
            "pending": game.score._pending,
        },
        "step_mode": False,
    }
