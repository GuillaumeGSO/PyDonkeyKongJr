# PyDonkeyKongJr — Project Guide

Python recreation of the classic Donkey Kong Jr arcade game using pure Pygame.

## Running the Game

```bash
pip install -r requirements.txt
python main.py
```

To run the sprite positioning calibration tool:
```bash
python positioning_tool.py
```

## Project Structure

```
main.py                  # Entry point and game loop (App class)
donkey_kong_jr.py        # Central game state manager (DonkeyKongJr class)
settings.py              # Configuration constants
positioning_tool.py      # Dev tool for calibrating sprite positions
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
  {Type}Positions        # Pickle files: position name → (x, y) coords
  FullScreen.png         # Reference arcade screenshot (for positioning tool)
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
| `INVINCIBLE` | False | Cheat mode toggle |

## Architecture

### Game Loop
`App.run()` → 30 FPS loop:
1. `check_events()` — keyboard input (arrows + SPACE = jump, ESC = quit)
2. `game.update()` — updates all actor groups in order
3. `game.draw()` — blits background then all sprite groups

### Sprite Groups (in DonkeyKongJr)
Draw order: `cage_group` → `weapon_group` → `threat_group` → `player_group` → `info_group`

### Position Graph System
Every actor navigates a graph of named `SpritePosition` objects. Each node holds:
- The sprite image loaded from `img/sprites/{Type}/{name}.png`
- Screen coordinates loaded from a pickle file in `positions/`
- Transition links: `next_move`, `left_move`, `right_move`, `up_move`, `down_move`, `jump_move`
- `eater_name` — the position name that can collide with a threat

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
- Bird: 10 pts, loops B00–B07
- Croco: 5–15 pts depending on position, loops C00–C12

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

## Positioning Tool (positioning_tool.py)

Developer utility to calibrate sprite (x, y) positions against the original arcade reference image. Run it when adding new sprites or adjusting positions:
- Arrow keys: move sprite
- Space: confirm and save position
- Saves to `positions/{Type}Positions` pickle file

