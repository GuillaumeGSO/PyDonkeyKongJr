# PyDonkeyKongJr — Project Guide

Python recreation of the classic Donkey Kong Jr arcade game using pure Pygame.

## Running the Game

```bash
pip install -r requirements.txt
python main.py
```

To run the dev tools:
```bash
python tools/positioning_tool.py                              # calibrate sprite positions
python tools/sprite_viewer.py                                 # view all sprites at their positions
python tools/scenario_tool.py [scenario.json]                 # load a game state and play/step through it
```

To run the tests:
```bash
pip install pytest
python -m pytest tests/ -v
```

## Project Structure

```
main.py                  # Entry point and game loop (App class)
donkey_kong_jr.py        # Central game state manager (DonkeyKongJr class)
scenario.py              # load_scenario() / dump_state() — shared by tool and tests
settings.py              # Configuration constants
tools/
  positioning_tool.py    # Dev tool for calibrating sprite positions
  sprite_viewer.py       # Dev tool for viewing all sprites at their positions
  scenario_tool.py       # Dev tool for loading a scenario JSON and playing/stepping through it
  scenarios/             # JSON scenario files for the interactive tool
  img/FullScreen.png     # Reference arcade screenshot (for dev tools)
tests/
  conftest.py            # Headless pygame fixtures + advance_frame() helper
  test_scenarios.py      # Integration tests (14 scenarios)
  scenarios/             # JSON scenario files used by tests
actors/
  threat.py              # Abstract base class for enemies
  bird.py                # Bird enemy (B00–B07 path)
  croco.py               # Crocodile enemy (C00–C12 path)
  player.py              # Player character (40 positions)
  cage.py                # Cage + mom sprite (win condition)
  nut.py                 # Coconut weapon
  key.py                 # Collectible key
  missed.py              # Lives indicator display
  score.py               # Score tracker and renderer
positions/
  SpritePosition.py      # Base sprite class with position-graph support
  graph_loader.py        # Loads position graphs from JSON, builds SpritePosition objects
  {Type}Positions.json   # JSON files: position name → [x, y] coords
  graphs/{Type}.json     # JSON files: position graph topology (links between positions)
img/
  EmptyScreen.png        # Game background
  sprites/{Type}/*.png   # Sprite frames per actor type
fonts/
  Open 24 Display St.ttf # Score font
sounds/                  # WAV files (currently unused — playback is commented out)
```

## Settings (settings.py)

| Constant | Value | Description |
|---|---|---|
| `WIDTH` / `HEIGHT` | 700 / 480 | Window size |
| `FPS` | 30 | Frame rate |
| `ANIMATION_DELAY` | 500ms | Sprite update rate (threats) |
| `SCORE_DELAY` | 10ms | Points increment interval |
| `NUMBER_OF_LIFE` | 3 | Starting lives |
| `MIN_ANIMATION_DELAY` | 150ms | Fastest threat update rate |
| `DIFFICULTY_STEP` | 10 | Score threshold for speed increase |
| `MAX_CROCOS` | 3 | Max simultaneous crocodiles |
| `MAX_BIRDS` | 2 | Max simultaneous birds |
| `INVINCIBLE` | False | Cheat mode toggle |
| `DEATH_BLINK_INTERVAL` | 200ms | Blink rate during death animation |
| `DEATH_ANIMATION_DURATION` | 2000ms | Total death animation length |

## Architecture

### Game Loop
`App.run()` → 30 FPS loop:
1. `check_events()` — keyboard input (arrows + SPACE = jump, ESC = quit)
2. `game.update()` — updates all actor groups in order
3. `game.draw()` — blits background then all sprite groups

### Sprite Groups (in DonkeyKongJr)
Draw order: `player_group` → `info_group` → `threat_group` → `weapon_group` → `cage_group` → `score`

### Position Graph System
Every actor navigates a graph of named `SpritePosition` objects. Each node holds:
- The sprite image loaded from `img/sprites/{Type}/{name}.png`
- Screen coordinates loaded from JSON files in `positions/` (e.g. `positions/MonkeyPositions.json`)
- Transition links: `next_move`, `left_move`, `right_move`, `up_move`, `down_move`, `jump_move`
- `eater_name` — the position name that can collide with a threat

Graph topology (which positions link to which) is defined in JSON files under `positions/graphs/{ActorType}.json` and loaded by `positions/graph_loader.py`. Each actor's `generate_positions()` delegates to `load_position_graph()`.

Actors advance by setting `current_position = positions[current_position.next_move]`.

### Animation Rate Limiting
- Threats: update every `ANIMATION_DELAY` (500ms)
- Player: update every `ANIMATION_DELAY / 4` (125ms, 4× faster)
- Score: increments every `SCORE_DELAY` (10ms)

## Actors

### Player (actors/player.py)
- 40 named positions covering lower (L0–L5) and upper (H0–H7) platforms
- Key positions: `L0G` (start), `H2J` (drop nut), `H4J` (grab key), `H5O` (open cage), `H7F`/`H7L` (fall/lose life)
- Collision with threats is position-gated: only triggers if current position name matches threat's `eater_name`

### Threats (actors/threat.py + bird.py + croco.py)
- Follow predetermined cyclic paths
- `do_kill()` removes from group and awards points
- Bird: 6 pts, loops B00–B07
- Croco: 3 pts (C00–C04) or 9 pts (lower positions), loops C00–C12

### Nut (actors/nut.py)
- Spawned when player jumps at H2J
- Falls N00→N01→N02→N03, kills any threat it collides with

### Key (actors/key.py)
- Oscillates K00→K01→K02→K03→K02b→K01b→K00
- Only grabable (`is_grabable=True`) at K03

### Cage (actors/cage.py)
- 4 cage parts (C00–C03) + mom sprite (CSM)
- Each `open_cage()` call removes one part (+25 pts), final open shows mom (+50 pts)
- `fully_opened=True` triggers level reset

### Missed / Score (actors/missed.py, actors/score.py)
- Missed: shows M00/M01/M02 sprites tracking lives lost
- Score: renders with "Open 24 Display St.ttf", animates point increments

## Game Flow

**Win:** Grab key (at K03, position H4J) → cage opens 4× → level resets

**Lose life:** Collide with threat OR fall at H7L → respawn at L0G → `init_objects()` resets key, nut, threats

**Game over:** Lose `NUMBER_OF_LIFE` (3) lives → `is_playing = False`

## Dev Tools (tools/)

### Positioning Tool (`tools/positioning_tool.py`)
Calibrate sprite (x, y) positions against the original arcade reference image. Run it when adding new sprites or adjusting positions:
- Arrow keys: move sprite
- Space: confirm and save position
- Saves to `positions/{Type}Positions.json`

### Sprite Viewer (`tools/sprite_viewer.py`)
Shows all sprites placed at their calibrated positions on the empty game background. Useful for verifying the full layout at a glance:
- Space: toggle between sprite layout and `tools/img/FullScreen.png` arcade reference
- ESC: quit

### Scenario Tool (`tools/scenario_tool.py`)
Load any game state from a JSON file and play or step through it. Useful for reproducing specific situations without playing through the game:
```bash
python tools/scenario_tool.py tools/scenarios/grab_key.json
python tools/scenario_tool.py tools/scenarios/croco_gauntlet.json
```
- Arrow keys / Space: move player (normal mode) or queue next move (step mode)
- **T**: toggle step mode — Space advances exactly one frame at a time
- **R**: reload scenario from JSON
- **S**: save current state as a timestamped JSON snapshot
- **ESC**: quit (also saves snapshot if `--save-on-quit FILE` was specified)

A debug HUD overlays the current player position, live croco/bird positions, key/nut/cage state, score and frame count.

## Testing

Tests run headlessly (no window, no audio) via `SDL_VIDEODRIVER=dummy`:
```bash
python -m pytest tests/ -v
```

### Scenario system (`scenario.py`)
The shared foundation for both the interactive tool and tests:
- `load_scenario(game, data)` — teleports all actors to positions from a JSON dict, rebuilds sprite groups, resets timers
- `dump_state(game) → dict` — serializes current game state back to the same format

### JSON scenario format
```json
{
  "game":   { "number_of_life": 0, "level": 0, "is_playing": true },
  "player": { "position": "H3G", "is_new_turn": false, "is_dying": false },
  "crocos": [ { "position": "C06" } ],
  "birds":  [ { "position": "B03" } ],
  "nut":    { "position": "N00", "is_visible": true },
  "key":    { "position": "K03", "is_visible": true, "is_grabable": true },
  "cage":   { "remaining_cage": 4, "fully_opened": false },
  "score":  { "score": 0, "pending": 0 },
  "step_mode": false
}
```
`number_of_life` = lives **lost** so far (0 = none, 3 = game over). `null` or absent entries in `crocos`/`birds` disable that slot.

### `advance_frame()` helper (`tests/conftest.py`)
`pg.time.get_ticks()` advances ~2ms between Python calls — well below every cooldown threshold (125ms player, 500ms threats). The helper backdates actor `last_time` by 10s so `can_update()` always returns True. Selective expiry via kwargs matters:

| kwarg | When to set `False` |
|---|---|
| `expire_player` | Player must stay at a position (e.g. H2J for nut trigger tests) |
| `expire_threats` | Threat must stay at its kill position across frames |
| `expire_key` | Key must stay at K03 (grabable) for key-grab tests |

### Test coverage
| Category | Tests |
|---|---|
| Key grab / miss | grab succeeds, miss falls to H7F, cage last open → fully_opened |
| Collision | grace period starts, player dies after grace, game over on 3rd life |
| Nut kills | croco@C02 (via N01), bird@B04 (via N02), croco@C09 (via N03) |
| Nut passes | N01→N02 no bird, N02→N03 no croco, bottom wait, bottom disappear |
| Nut trigger | player@H2J starts fall, player elsewhere = no fall |

