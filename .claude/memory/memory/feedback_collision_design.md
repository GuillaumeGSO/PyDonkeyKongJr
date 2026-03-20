---
name: collision detection design
description: How player-threat collision should be split between pre-move and post-move checks
type: feedback
---

Split `handle_threats()` into pre-move and post-move phases (`post_move=False/True` param).

**Pre-move** = threat arrived at player → start grace period; blink at that position; if timer expires and player is still at `_collision_position_name` → die.

**Post-move** = player just moved to new position:
- Collision at new position → instant kill (player moved INTO threat, regardless of direction)
- No collision + `_had_collision_pre_move=True` → safe, cancel timer (player escaped away)

**Why:** Two distinct game situations: (1) threat walks into standing/forward-moving player — deserves grace period + blink at correct spot; (2) player catches up to threat from behind or escapes toward threat — instant kill. Merging both into one check caused either missed kills or wrong blink positions.

**How to apply:** Always use this two-phase pattern for collision detection in this game. Track `_collision_position_name` and `_had_collision_pre_move` as instance state; reset both in `start_of_game()` and `Threat.do_kill()`.
